"""Verificador grafico do .docx (modo Checar documento).

Le o arquivo so para leitura e relata fonte, tamanho, entrelinhas e alinhamento do
corpo do texto e as margens, com a regra e a origem lidas de references/.

Uso: python verificar_docx.py <arquivo.docx>
Saida: 0 sem problemas, 1 com algum item reprovado, 2 em erro de leitura.
"""
import re
import sys
import zipfile
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.text.run import Run

REFERENCES = Path(__file__).resolve().parent.parent / "references"
LIMITE_BYTES = 50 * 1024 * 1024
TOL_CM = 0.05
TOL_ENTRELINHAS = 0.01
TWIPS_POR_CM = 1440 / 2.54


class RegraAusente(Exception):
    """ID de regra que nao existe em references/."""


class ErroLeitura(Exception):
    """Arquivo recusado ou ilegivel."""


# Limiares numericos por regra. O texto literal precisa aparecer no bloco da regra
# em references/ (o unittest confere).
LIMIARES = {
    "GRA-03": {"fonte": "Arial", "tamanho": 12.0, "texto": ["Arial 12"]},
    "GRA-05": {"entrelinhas": 1.5, "alinhamento": "justificado",
               "texto": ["justificado", "1,5"]},
    "GRA-09": {"superior": 3.0, "esquerda": 3.0, "direita": 2.0, "inferior": 2.0,
               "texto": ["superior e esquerda 3 cm", "direita e inferior 2 cm"]},
    "CIT-06": {"recuo": 4.0, "fonte": "Arial", "tamanho": 10.0, "entrelinhas": 1.0,
               "texto": ["4 cm", "Arial 10", "(1,0)"]},
    "CIT-07": {"texto": ["10 linhas"]},
    "GRA-11": {"texto": ["folha de rosto"]},
    "GRA-12": {"texto": ["canto superior direito", "algarismos arábicos"]},
    "GRA-13": {"fonte": "Arial", "tamanho": 10.0, "texto": ["Arial 10"]},
    "GRA-15": {"texto": ["consecutivamente"]},
    "GRA-16": {"texto": ["página nova", "negrito", "caixa alta", "esquerda"]},
    "GRA-18": {"texto": ["(maiúsculas e negrito)", "(maiúsculas)", "(negrito)", "(normal)",
                         "(itálico)"]},
}


# ---------------------------------------------------------------- origem

def bloco_regra(rid):
    """Linha da regra mais sub-linhas '  - ' logo abaixo."""
    padrao = f"- **{rid}**"
    for arq in sorted(REFERENCES.glob("*.md")):
        linhas = arq.read_text(encoding="utf-8").splitlines()
        for i, linha in enumerate(linhas):
            if linha.startswith(padrao):
                bloco = [linha]
                for prox in linhas[i + 1:]:
                    if prox.startswith("  - "):
                        bloco.append(prox)
                    else:
                        break
                return "\n".join(bloco)
    raise RegraAusente(rid)


def origem(rid):
    linha = bloco_regra(rid).splitlines()[0]
    if " — " not in linha:
        raise RegraAusente(f"{rid} (sem origem)")
    return linha.rsplit(" — ", 1)[1].strip()


def regra(rid):
    return (rid, origem(rid))


# ---------------------------------------------------------------- abertura

def abrir(caminho):
    p = Path(caminho)
    if p.suffix.lower() != ".docx":
        raise ErroLeitura("só arquivos .docx são aceitos")
    if not p.is_file():
        raise ErroLeitura("arquivo não encontrado")
    if p.stat().st_size > LIMITE_BYTES:
        raise ErroLeitura("arquivo maior que 50 MB")
    if not zipfile.is_zipfile(p):
        raise ErroLeitura("o arquivo não é um .docx válido")
    try:
        return Document(str(p))
    except Exception as e:  # python-docx levanta tipos variados
        raise ErroLeitura(str(e) or type(e).__name__)


# ---------------------------------------------------------------- heranca

def _cadeia_estilos(estilo):
    vistos = 0
    while estilo is not None and vistos < 30:
        yield estilo
        estilo = estilo.base_style
        vistos += 1


def _doc_defaults(par, tipo):
    """tipo: 'rPr' ou 'pPr'. Devolve o elemento dentro de docDefaults ou None."""
    parte = par.part
    if not hasattr(parte, "styles"):
        parte = parte._document_part
    estilos = parte.styles.element
    dd = estilos.find(qn("w:docDefaults"))
    if dd is None:
        return None
    pad = dd.find(qn(f"w:{tipo}Default"))
    if pad is None:
        return None
    return pad.find(qn(f"w:{tipo}"))


_TEMA = {}


def _fonte_do_tema(par, nome_tema):
    chave = id(par.part)
    if chave not in _TEMA:
        raiz = None
        for parte in par.part.package.iter_parts():
            if "/theme/" in str(parte.partname):
                from lxml import etree
                try:
                    raiz = etree.fromstring(parte.blob)
                except Exception:
                    raiz = None
                break
        _TEMA[chave] = raiz
    raiz = _TEMA[chave]
    if raiz is None:
        return None
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    tipo = "minorFont" if "minor" in nome_tema.lower() else "majorFont"
    el = raiz.find(f".//a:{tipo}/a:latin", ns)
    return el.get("typeface") if el is not None else None


def _fonte_de_rpr(rpr, par):
    if rpr is None:
        return None
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        return None
    for atr in ("w:ascii", "w:hAnsi"):
        v = rf.get(qn(atr))
        if v:
            return v
    for atr in ("w:asciiTheme", "w:hAnsiTheme"):
        v = rf.get(qn(atr))
        if v:
            return _fonte_do_tema(par, v)
    return None


def _tamanho_de_rpr(rpr):
    if rpr is None:
        return None
    sz = rpr.find(qn("w:sz"))
    if sz is None or sz.get(qn("w:val")) is None:
        return None
    try:
        return int(sz.get(qn("w:val"))) / 2
    except ValueError:
        return None


def _rprs_da_cadeia(run, par):
    """Elementos rPr em ordem de precedencia: run, estilo do run, estilo do paragrafo, defaults."""
    rpr = run._element.rPr
    yield rpr
    try:
        for est in _cadeia_estilos(run.style):
            yield est.element.rPr
    except Exception:
        pass
    for est in _cadeia_estilos(par.style):
        yield est.element.rPr
    yield _doc_defaults(par, "rPr")


def fonte_efetiva(run, par):
    for rpr in _rprs_da_cadeia(run, par):
        v = _fonte_de_rpr(rpr, par)
        if v:
            return v
    return None


def tamanho_efetivo(run, par):
    for rpr in _rprs_da_cadeia(run, par):
        v = _tamanho_de_rpr(rpr)
        if v is not None:
            return v
    return None


def _ppr_da_cadeia(par):
    yield par._p.pPr
    for est in _cadeia_estilos(par.style):
        yield est.element.pPr
    yield _doc_defaults(par, "pPr")


def entrelinhas_efetiva(par):
    """('auto', multiplo) | ('exact', pt) | ('atLeast', pt)."""
    for ppr in _ppr_da_cadeia(par):
        if ppr is None:
            continue
        sp = ppr.find(qn("w:spacing"))
        if sp is None or sp.get(qn("w:line")) is None:
            continue
        try:
            linha = int(sp.get(qn("w:line")))
        except ValueError:
            continue
        regra_ = sp.get(qn("w:lineRule")) or "auto"
        if regra_ == "auto":
            return ("auto", linha / 240)
        return (regra_, linha / 20)
    return ("auto", 1.0)


def alinhamento_efetivo(par):
    """Valor de w:jc ('both', 'left', 'center', 'right'...). Padrao OOXML: left."""
    for ppr in _ppr_da_cadeia(par):
        if ppr is None:
            continue
        jc = ppr.find(qn("w:jc"))
        if jc is not None and jc.get(qn("w:val")):
            return jc.get(qn("w:val"))
    return "left"


def recuo_esquerdo_efetivo(par):
    """Recuo esquerdo em cm."""
    for ppr in _ppr_da_cadeia(par):
        if ppr is None:
            continue
        ind = ppr.find(qn("w:ind"))
        if ind is None:
            continue
        for atr in ("w:left", "w:start"):
            v = ind.get(qn(atr))
            if v is not None:
                try:
                    return int(v) / TWIPS_POR_CM
                except ValueError:
                    return 0.0
    return 0.0


# ---------------------------------------------------------------- estrutura

RE_ESTILO_TITULO = re.compile(r"^(Heading|Título|Titulo) (\d)$", re.IGNORECASE)
RE_TITULO_NUM = re.compile(r"^(\d+(?:\.\d+){0,4})\.?\s+\S")
RE_LEGENDA = re.compile(r"^(Tabela|Figura|Quadro|Gráfico|Grafico)\s+\d|^Fonte:")
RE_SUMARIO = re.compile(r"\.{4,}|\t\s*\d+\s*$")
FIM_CORPO = ("REFERÊNCIAS", "REFERENCIAS")


def _nivel_outline(par):
    for ppr in _ppr_da_cadeia(par):
        if ppr is None:
            continue
        ol = ppr.find(qn("w:outlineLvl"))
        if ol is not None and ol.get(qn("w:val")) is not None:
            try:
                return int(ol.get(qn("w:val"))) + 1
            except ValueError:
                return None
    return None


def nivel_titulo(par):
    """Nivel do titulo (1 a 5) ou None se o paragrafo nao e titulo."""
    texto = par.text.strip()
    if not texto:
        return None
    nome = par.style.name if par.style is not None else ""
    if re.match(r"^(toc|sum[aá]rio)", nome, re.IGNORECASE) or RE_SUMARIO.search(par.text):
        return None
    m = RE_ESTILO_TITULO.match(nome)
    if m:
        return int(m.group(2))
    nivel = _nivel_outline(par)
    if nivel is not None and nivel <= 9:
        return nivel
    m = RE_TITULO_NUM.match(texto)
    if m and len(texto) <= 150 and texto[-1] not in ".;:":
        return len(m.group(1).split("."))
    return None


def _e_citacao(par):
    nome = par.style.name if par.style is not None else ""
    if "Cita" in nome or "Quote" in nome:
        return True
    if recuo_esquerdo_efetivo(par) >= 1.5:
        return True
    tams = [tamanho_efetivo(r, par) for r in par.runs if r.text.strip()]
    return bool(tams) and all(t is not None and t <= 11 for t in tams)


def partes_do_documento(doc):
    """Indices de titulos, corpo, legendas e candidatos a citacao longa."""
    pars = doc.paragraphs
    titulos = {i: nivel_titulo(p) for i, p in enumerate(pars)}
    titulos = {i: n for i, n in titulos.items() if n is not None}
    inicio = next((i for i, n in sorted(titulos.items()) if n == 1), None)
    sem_inicio = inicio is None
    if sem_inicio:
        inicio = 0
    fim = len(pars)
    for i in range(inicio, len(pars)):
        if pars[i].text.strip().upper() in FIM_CORPO:
            fim = i
            break
    corpo = list(range(inicio, fim))
    legendas = {i for i in corpo if RE_LEGENDA.match(pars[i].text.strip())}
    citacoes = {i for i in corpo
                if i not in titulos and i not in legendas and pars[i].text.strip()
                and _e_citacao(pars[i])}
    return {"titulos": titulos, "corpo": corpo, "legendas": legendas,
            "citacoes": citacoes, "sem_inicio": sem_inicio}


# ---------------------------------------------------------------- itens

def fmt(v):
    s = f"{v:.2f}"
    if s.endswith("0"):
        s = s[:-1]
    return s.replace(".", ",")


def _exemplo(i, par, valor):
    t = par.text.strip()
    if len(t) > 40:
        t = t[:40] + "…"
    return f"§{i} '{t}' ({valor})"


def _item(chave, nome, rids, falhas, total, nao_resolvidos, ok_texto=""):
    regras = [regra(r) for r in rids]
    if falhas:
        exs = "; ".join(_exemplo(i, p, v) for i, p, v in falhas[:3])
        return {"chave": chave, "item": nome, "resultado": "✘", "regras": regras,
                "detalhe": f"{len(falhas)} de {total} parágrafos: {exs}"}
    if nao_resolvidos:
        return {"chave": chave, "item": nome, "resultado": "verificar manualmente",
                "regras": regras,
                "detalhe": f"valor não resolvido em {len(nao_resolvidos)} parágrafo(s) (ex.: §{nao_resolvidos[0]})"}
    return {"chave": chave, "item": nome, "resultado": "✔", "regras": regras,
            "detalhe": ok_texto or f"{total} parágrafos conferidos"}


def _itens_texto(doc, partes):
    pars = doc.paragraphs
    titulos, legendas, citacoes = partes["titulos"], partes["legendas"], partes["citacoes"]
    base = [i for i in partes["corpo"]
            if pars[i].text.strip() and i not in legendas and i not in citacoes]
    corpo_puro = [i for i in base if i not in titulos]
    lim_f, lim_e, lim_a = LIMIARES["GRA-03"], LIMIARES["GRA-05"], LIMIARES["GRA-05"]

    f_falhas, f_nr, t_falhas, t_nr = [], [], [], []
    for i in base:
        p = pars[i]
        fontes, tams = [], []
        for r in p.runs:
            if not r.text.strip():
                continue
            fontes.append(fonte_efetiva(r, p))
            tams.append(tamanho_efetivo(r, p))
        ruins = [f for f in fontes if f is not None and f.lower() != lim_f["fonte"].lower()]
        if ruins:
            f_falhas.append((i, p, ruins[0]))
        elif any(f is None for f in fontes):
            f_nr.append(i)
        ruins = [t for t in tams if t is not None and abs(t - lim_f["tamanho"]) > 0.01]
        if ruins:
            t_falhas.append((i, p, fmt(ruins[0]) + " pt"))
        elif any(t is None for t in tams):
            t_nr.append(i)

    e_falhas = []
    a_falhas = []
    nomes_al = {"left": "à esquerda", "start": "à esquerda", "center": "centralizado",
                "right": "à direita", "end": "à direita", "distribute": "distribuído"}
    for i in corpo_puro:
        p = pars[i]
        tipo, v = entrelinhas_efetiva(p)
        if tipo == "auto":
            if abs(v - lim_e["entrelinhas"]) > TOL_ENTRELINHAS:
                e_falhas.append((i, p, f"entrelinhas {fmt(v)}"))
        else:
            rot = "exata" if tipo == "exact" else "mínima"
            e_falhas.append((i, p, f"entrelinhas {rot} de {fmt(v)} pt"))
        al = alinhamento_efetivo(p)
        if al != "both":
            a_falhas.append((i, p, nomes_al.get(al, al)))

    return [
        _item("fonte_corpo", "Fonte do corpo do texto (Arial)", ["GRA-03"],
              f_falhas, len(base), f_nr),
        _item("tamanho_corpo", "Tamanho da fonte do corpo do texto (12 pt)", ["GRA-03"],
              t_falhas, len(base), t_nr),
        _item("entrelinhas_corpo", "Entrelinhas do corpo do texto (1,5)", ["GRA-05"],
              e_falhas, len(corpo_puro), []),
        _item("alinhamento_corpo", "Alinhamento do corpo do texto (justificado)", ["GRA-05"],
              a_falhas, len(corpo_puro), []),
    ]


def _item_margens(doc):
    lim = LIMIARES["GRA-09"]
    settings = doc.settings.element
    gutter = any(
        (s._sectPr.find(qn("w:pgMar")) is not None
         and s._sectPr.find(qn("w:pgMar")).get(qn("w:gutter")) not in (None, "0"))
        for s in doc.sections)
    if settings.find(qn("w:mirrorMargins")) is not None or gutter:
        return {"chave": "margens", "item": "Margens", "resultado": "verificar manualmente",
                "regras": [regra("GRA-09"), regra("GRA-10")],
                "detalhe": "margens espelhadas ou com medianiz: conferir anverso e verso à mão"}
    lados = (("superior", "top_margin"), ("esquerda", "left_margin"),
             ("direita", "right_margin"), ("inferior", "bottom_margin"))
    secoes = []
    nao_lido = False
    for n, s in enumerate(doc.sections, 1):
        fora = []
        for nome, attr in lados:
            v = getattr(s, attr)
            if v is None:
                nao_lido = True
                continue
            cm = v.cm
            if abs(cm - lim[nome]) > TOL_CM:
                fora.append(f"{nome} {fmt(cm)} cm")
        if fora:
            secoes.append((n, fora))
    regras = [regra("GRA-09")]
    if secoes:
        multi = len(doc.sections) > 1
        det = "; ".join((f"seção {n}: " if multi else "") + ", ".join(f) for n, f in secoes)
        return {"chave": "margens", "item": "Margens (3/3/2/2 cm)", "resultado": "✘",
                "regras": regras, "detalhe": det + " (esperado: superior e esquerda 3 cm; direita e inferior 2 cm)"}
    if nao_lido:
        return {"chave": "margens", "item": "Margens (3/3/2/2 cm)",
                "resultado": "verificar manualmente", "regras": regras,
                "detalhe": "margem não definida no arquivo"}
    return {"chave": "margens", "item": "Margens (3/3/2/2 cm)", "resultado": "✔",
            "regras": regras, "detalhe": f"{len(doc.sections)} seção(ões) conferida(s)"}


# ---------------------------------------------------------------- citacao longa (P-26)

ABRE_ASPAS = ('"', "“", "«")
FECHA_ASPAS = ('"', "”", "»")
RE_CHAMADA_FINAL = re.compile(r"\s*\([^()]*\)\s*\.?\s*$")
RE_TRECHO_ASPAS = re.compile(r'[“"«]([^”"»]{226,})[”"»]')


def _manual(chave, nome, rids, detalhe):
    return {"chave": chave, "item": nome, "resultado": "verificar manualmente",
            "regras": [regra(r) for r in rids], "detalhe": detalhe}


def _tem_aspas(texto):
    t = texto.strip()
    if t.startswith(ABRE_ASPAS):
        return True
    m = RE_CHAMADA_FINAL.search(t)
    antes = (t[:m.start()] if m else t).rstrip().rstrip(".").rstrip()
    return antes.endswith(FECHA_ASPAS)


def itens_citacao(doc, partes):
    pars = doc.paragraphs
    lim = LIMIARES["CIT-06"]
    cands = sorted(partes["citacoes"])
    itens = []
    if not cands:
        itens.append(_manual("citacao_longa", "Citação longa (CIT-06)", ["CIT-06"],
                             "nenhuma citação longa identificada por recuo, fonte ou estilo"))
    else:
        r_falhas, f_falhas, f_nr, e_falhas, a_falhas = [], [], [], [], []
        for i in cands:
            p = pars[i]
            recuo = recuo_esquerdo_efetivo(p)
            if abs(recuo - lim["recuo"]) > TOL_CM:
                r_falhas.append((i, p, f"recuo {fmt(recuo)} cm"))
            fontes, tams = [], []
            for r in p.runs:
                if r.text.strip():
                    fontes.append(fonte_efetiva(r, p))
                    tams.append(tamanho_efetivo(r, p))
            ruim = [f"{f} {fmt(t)} pt" for f, t in zip(fontes, tams)
                    if (f is not None and f.lower() != lim["fonte"].lower())
                    or (t is not None and abs(t - lim["tamanho"]) > 0.01)]
            if ruim:
                f_falhas.append((i, p, ruim[0]))
            elif any(f is None for f in fontes) or any(t is None for t in tams):
                f_nr.append(i)
            tipo, v = entrelinhas_efetiva(p)
            if tipo == "auto":
                if abs(v - lim["entrelinhas"]) > TOL_ENTRELINHAS:
                    e_falhas.append((i, p, f"entrelinhas {fmt(v)}"))
            else:
                rot = "exata" if tipo == "exact" else "mínima"
                e_falhas.append((i, p, f"entrelinhas {rot} de {fmt(v)} pt"))
            if _tem_aspas(p.text):
                a_falhas.append((i, p, "com aspas"))
        n = len(cands)
        itens += [
            _item("citacao_recuo", "Recuo da citação longa (4 cm)", ["CIT-06"],
                  r_falhas, n, []),
            _item("citacao_fonte", "Fonte da citação longa (Arial 10)", ["CIT-06"],
                  f_falhas, n, f_nr),
            _item("citacao_entrelinhas", "Entrelinhas da citação longa (simples)", ["CIT-06"],
                  e_falhas, n, []),
            _item("citacao_aspas", "Citação longa sem aspas", ["CIT-06"],
                  a_falhas, n, []),
        ]
    itens.append(_manual(
        "citacao_extensao", "Extensão da citação (até 10 linhas)", ["CIT-07"],
        "o limite de 10 linhas depende da paginação do Word: conferir à mão"))
    excluidos = set(partes["titulos"]) | partes["legendas"] | partes["citacoes"]
    achados = [i for i in partes["corpo"]
               if i not in excluidos and RE_TRECHO_ASPAS.search(pars[i].text)]
    if achados:
        lista = ", ".join(f"§{i}" for i in achados[:3])
        det = (f"parágrafos do corpo com trecho entre aspas de mais de 225 caracteres: {lista}. "
               "É estimativa de apoio do SKILL.md, não regra do manual; confirmar se é "
               "citação direta longa sem recuo")
    else:
        det = ("citação longa sem recuo e sem aspas não é identificável pelo arquivo; "
               "nenhum trecho entre aspas com mais de 225 caracteres no corpo "
               "(estimativa de apoio do SKILL.md, não regra do manual)")
    itens.append(_manual("citacao_sem_recuo", "Citação longa sem recuo", ["CIT-06"], det))
    return itens


# ---------------------------------------------------------------- secoes

def _body_sectpr(doc):
    return doc.element.body.find(qn("w:sectPr"))


def _sectpr_que_encerra(doc, indice):
    """w:sectPr que ENCERRA a secao do paragrafo: o primeiro w:pPr/w:sectPr de um
    paragrafo igual ou posterior; senao, o do w:body."""
    pars = doc.paragraphs
    for p in pars[indice:]:
        ppr = p._p.pPr
        if ppr is not None and ppr.find(qn("w:sectPr")) is not None:
            return ppr.find(qn("w:sectPr"))
    return _body_sectpr(doc)


def tipo_secao_do_paragrafo(doc, indice):
    """Como comeca a secao do paragrafo (w:type do sectPr que a encerra)."""
    sp = _sectpr_que_encerra(doc, indice)
    if sp is None:
        return "nextPage"
    t = sp.find(qn("w:type"))
    v = t.get(qn("w:val")) if t is not None else None
    return v or "nextPage"


# ---------------------------------------------------------------- numeracao (P-27)

RE_CAMPO_PAGE = re.compile(r"\bPAGE\b")


def _campos_do_paragrafo(par, local):
    achados = []
    viu_tab = False
    cur = None
    for ch in par._p.iterchildren():
        if ch.tag == qn("w:fldSimple"):
            if RE_CAMPO_PAGE.search(ch.get(qn("w:instr")) or ""):
                runs = [Run(r, par) for r in ch.findall(qn("w:r"))]
                achados.append({"local": local, "par": par, "runs": runs, "tab_antes": viu_tab})
        elif ch.tag == qn("w:r"):
            fc = ch.find(qn("w:fldChar"))
            if fc is not None:
                tipo = fc.get(qn("w:fldCharType"))
                if tipo == "begin":
                    cur = {"instr": "", "instr_runs": [], "res": [], "fase": "instr",
                           "tab": viu_tab}
                elif tipo == "separate" and cur is not None:
                    cur["fase"] = "res"
                elif tipo == "end" and cur is not None:
                    if RE_CAMPO_PAGE.search(cur["instr"]):
                        els = cur["res"] or cur["instr_runs"]
                        achados.append({"local": local, "par": par,
                                        "runs": [Run(r, par) for r in els],
                                        "tab_antes": cur["tab"]})
                    cur = None
            elif cur is not None:
                if cur["fase"] == "instr" and ch.find(qn("w:instrText")) is not None:
                    cur["instr"] += ch.find(qn("w:instrText")).text or ""
                    cur["instr_runs"].append(ch)
                elif cur["fase"] == "res" and ch.find(qn("w:t")) is not None:
                    cur["res"].append(ch)
            if ch.find(qn("w:tab")) is not None:
                viu_tab = True
    return achados


def campos_pagina(doc):
    """Ocorrencias do campo PAGE em cabecalhos e rodapes de todas as secoes."""
    pares_aos = doc.settings.element.find(qn("w:evenAndOddHeaders")) is not None
    achados = []
    for s in doc.sections:
        for local, partes_ in (
                ("cabeçalho", [(s.header, True), (s.first_page_header, s.different_first_page_header_footer),
                               (s.even_page_header, pares_aos)]),
                ("rodapé", [(s.footer, True), (s.first_page_footer, s.different_first_page_header_footer),
                            (s.even_page_footer, pares_aos)])):
            for hf, usado in partes_:
                if not usado or hf.is_linked_to_previous:
                    continue
                for par in hf.paragraphs:
                    achados += _campos_do_paragrafo(par, local)
    return achados


def _alinhamento_explicito(par):
    for ppr in _ppr_da_cadeia(par):
        if ppr is None:
            continue
        jc = ppr.find(qn("w:jc"))
        if jc is not None and jc.get(qn("w:val")):
            return jc.get(qn("w:val"))
    return None


def itens_numeracao(doc, partes):
    campos = campos_pagina(doc)
    cab = [c for c in campos if c["local"] == "cabeçalho"]
    itens = []
    if cab:
        itens.append({"chave": "numeracao_posicao", "item": "Numeração de página no cabeçalho",
                      "resultado": "✔", "regras": [regra("GRA-12")],
                      "detalhe": f"campo de página em {len(cab)} cabeçalho(s)"})
    else:
        det = ("campo de página no rodapé; a regra pede o cabeçalho" if campos
               else "campo de página ausente (nenhum cabeçalho ou rodapé numera as folhas)")
        itens.append({"chave": "numeracao_posicao", "item": "Numeração de página no cabeçalho",
                      "resultado": "✘", "regras": [regra("GRA-12")], "detalhe": det})
    if campos:
        usados = cab or campos
        nomes = {"left": "à esquerda", "start": "à esquerda", "center": "centralizado",
                 "both": "justificado"}
        ruins, manual = [], False
        for c in usados:
            al = _alinhamento_explicito(c["par"])
            if al in ("right", "end"):
                continue
            if al is None and c["tab_antes"]:
                manual = True
            else:
                ruins.append(nomes.get(al, al or "à esquerda"))
        if ruins:
            itens.append({"chave": "numeracao_alinhamento", "item": "Número alinhado à direita",
                          "resultado": "✘", "regras": [regra("GRA-12")],
                          "detalhe": f"número {ruins[0]} (esperado: canto superior direito)"})
        elif manual:
            itens.append(_manual("numeracao_alinhamento", "Número alinhado à direita",
                                 ["GRA-12"], "alinhamento por tabulação: conferir à mão"))
        else:
            itens.append({"chave": "numeracao_alinhamento", "item": "Número alinhado à direita",
                          "resultado": "✔", "regras": [regra("GRA-12")],
                          "detalhe": f"{len(usados)} campo(s) conferido(s)"})
        lim = LIMIARES["GRA-13"]
        ruins, nr = [], False
        for c in usados:
            for r in c["runs"]:
                f, t = fonte_efetiva(r, c["par"]), tamanho_efetivo(r, c["par"])
                if f is None or t is None:
                    nr = True
                elif f.lower() != lim["fonte"].lower() or abs(t - lim["tamanho"]) > 0.01:
                    ruins.append(f"{f} {fmt(t)} pt")
        if ruins:
            itens.append({"chave": "numeracao_fonte", "item": "Fonte do número (Arial 10)",
                          "resultado": "✘", "regras": [regra("GRA-13")],
                          "detalhe": f"número em {ruins[0]} (esperado: Arial 10 pt)"})
        elif nr:
            itens.append(_manual("numeracao_fonte", "Fonte do número (Arial 10)", ["GRA-13"],
                                 "fonte ou tamanho do número não resolvido no arquivo"))
        else:
            itens.append({"chave": "numeracao_fonte", "item": "Fonte do número (Arial 10)",
                          "resultado": "✔", "regras": [regra("GRA-13")],
                          "detalhe": "Arial 10 pt"})
        ini = partes["corpo"][0] if partes["corpo"] else 0
        sp = _sectpr_que_encerra(doc, ini)
        pg = sp.find(qn("w:pgNumType")) if sp is not None else None
        formato = pg.get(qn("w:fmt")) if pg is not None else None
        if formato in (None, "decimal"):
            itens.append({"chave": "numeracao_formato", "item": "Algarismos arábicos",
                          "resultado": "✔", "regras": [regra("GRA-12")],
                          "detalhe": "formato decimal na seção do corpo"})
        else:
            itens.append({"chave": "numeracao_formato", "item": "Algarismos arábicos",
                          "resultado": "✘", "regras": [regra("GRA-12")],
                          "detalhe": f"formato '{formato}' na seção do corpo (esperado: decimal)"})
    itens.append(_manual(
        "numeracao_inicio", "Início da numeração (primeira folha de texto)",
        ["GRA-11", "GRA-12"],
        "a contagem parte da folha de rosto e o número aparece a partir da primeira folha "
        "de texto; em que folha isso ocorre depende de seções e da paginação: conferir à mão"))
    return itens


# ---------------------------------------------------------------- titulos (P-28)

def _flag_efetivo(run, par, tag):
    for rpr in _rprs_da_cadeia(run, par):
        if rpr is None:
            continue
        el = rpr.find(qn(f"w:{tag}"))
        if el is not None:
            return el.get(qn("w:val")) not in ("0", "false", "off")
    return False


def _runs_com_texto(par):
    return [r for r in par.runs if r.text.strip()]


def _todos(par, tag):
    runs = _runs_com_texto(par)
    return bool(runs) and all(_flag_efetivo(r, par, tag) for r in runs)


def _caixa_alta(par):
    letras = [c for c in par.text if c.isalpha()]
    return bool(letras) and (all(c.isupper() for c in letras) or _todos(par, "caps"))


def _page_break_before(par):
    for ppr in _ppr_da_cadeia(par):
        if ppr is None:
            continue
        el = ppr.find(qn("w:pageBreakBefore"))
        if el is not None:
            return el.get(qn("w:val")) not in ("0", "false", "off")
    return False


def tem_quebra_antes(doc, indice):
    pars = doc.paragraphs
    if indice == 0 or _page_break_before(pars[indice]):
        return True
    j = next((k for k in range(indice - 1, -1, -1) if pars[k].text.strip()), -1)
    if j == -1:
        return True
    for k in range(j, indice):
        for br in pars[k]._p.iter(qn("w:br")):
            if br.get(qn("w:type")) == "page":
                return True
    ultimo_sect = next((k for k in range(indice - 1, -1, -1)
                        if pars[k]._p.pPr is not None
                        and pars[k]._p.pPr.find(qn("w:sectPr")) is not None), None)
    if ultimo_sect is not None and ultimo_sect >= j:
        return tipo_secao_do_paragrafo(doc, indice) in ("nextPage", "oddPage", "evenPage")
    return False


GRAFIA = {
    2: ("maiúsculas sem negrito", lambda p: _caixa_alta(p) and not _todos(p, "b")),
    3: ("negrito sem caixa alta", lambda p: _todos(p, "b") and not _caixa_alta(p)),
    4: ("sem negrito, itálico nem caixa alta",
        lambda p: not _todos(p, "b") and not _todos(p, "i") and not _caixa_alta(p)),
    5: ("itálico", lambda p: _todos(p, "i")),
}


def itens_titulos(doc, partes):
    pars = doc.paragraphs
    titulos = {i: n for i, n in partes["titulos"].items() if i in set(partes["corpo"])}
    nomes = [("titulo_pagina_nova", "Seção primária em página nova", ["GRA-16"]),
             ("titulo_primaria_formato", "Seção primária em negrito, caixa alta e à esquerda",
              ["GRA-16"]),
             ("titulo_grafia_niveis", "Grafia dos títulos por nível", ["GRA-18"]),
             ("titulo_numeracao", "Numeração consecutiva das seções", ["GRA-15"])]
    if partes["sem_inicio"] or not titulos:
        return [_manual(c, n, r, "nenhum título identificado no corpo do texto")
                for c, n, r in nomes]
    itens = []
    prim = sorted(i for i, n in titulos.items() if n == 1)
    sem_quebra = [i for i in prim if not tem_quebra_antes(doc, i)]
    if sem_quebra:
        lista = "; ".join(f"sem quebra de página antes de: {pars[i].text.strip()[:40]}"
                          for i in sem_quebra[:3])
        itens.append({"chave": "titulo_pagina_nova", "item": nomes[0][1], "resultado": "✘",
                      "regras": [regra("GRA-16")],
                      "detalhe": f"{len(sem_quebra)} de {len(prim)} seções primárias: {lista} "
                                 "(se o título já cai no topo por acaso, insira a quebra mesmo assim)"})
    else:
        itens.append({"chave": "titulo_pagina_nova", "item": nomes[0][1], "resultado": "✔",
                      "regras": [regra("GRA-16")],
                      "detalhe": f"{len(prim)} seções primárias conferidas"})
    falhas = []
    for i in prim:
        p = pars[i]
        if not _todos(p, "b"):
            falhas.append((i, p, "sem negrito"))
        elif not _caixa_alta(p):
            falhas.append((i, p, "sem caixa alta"))
        elif alinhamento_efetivo(p) not in ("left", "start", "both"):
            falhas.append((i, p, f"alinhamento {alinhamento_efetivo(p)}"))
    itens.append(_item("titulo_primaria_formato", nomes[1][1], ["GRA-16"], falhas, len(prim), []))
    sub = sorted(i for i, n in titulos.items() if 2 <= n <= 5)
    if not sub:
        itens.append(_manual("titulo_grafia_niveis", nomes[2][1], ["GRA-18"],
                             "nenhum título de nível 2 a 5 no corpo do texto"))
    else:
        falhas = [(i, pars[i], f"nível {titulos[i]}: esperado {GRAFIA[titulos[i]][0]}")
                  for i in sub if not GRAFIA[titulos[i]][1](pars[i])]
        itens.append(_item("titulo_grafia_niveis", nomes[2][1], ["GRA-18"], falhas, len(sub), []))
    numeros = {}
    for i in titulos:
        m = RE_TITULO_NUM.match(pars[i].text.strip())
        if m:
            numeros[i] = tuple(int(x) for x in m.group(1).split("."))
    if len(numeros) < len(titulos):
        itens.append(_manual("titulo_numeracao", nomes[3][1], ["GRA-15"],
                             "títulos sem número no texto (numeração automática do Word): "
                             "conferir à mão"))
    else:
        saltos, contagem, vistos = [], {}, set()
        for i in sorted(numeros):
            nums = numeros[i]
            pai = nums[:-1]
            rotulo = ".".join(str(x) for x in nums)
            if pai and pai not in vistos:
                saltos.append(f"{rotulo} sem a seção {'.'.join(str(x) for x in pai)}")
            else:
                esperado = contagem.get(pai, 0) + 1
                if nums[-1] != esperado:
                    saltos.append(f"{rotulo} (esperado {'.'.join(str(x) for x in pai + (esperado,))})")
            contagem[pai] = nums[-1]
            vistos.add(nums)
        if saltos:
            itens.append({"chave": "titulo_numeracao", "item": nomes[3][1], "resultado": "✘",
                          "regras": [regra("GRA-15")],
                          "detalhe": "saltos: " + "; ".join(saltos[:3])})
        else:
            itens.append({"chave": "titulo_numeracao", "item": nomes[3][1], "resultado": "✔",
                          "regras": [regra("GRA-15")],
                          "detalhe": f"{len(numeros)} títulos numerados em sequência"})
    return itens


def verificar(caminho):
    doc = abrir(caminho)
    partes = partes_do_documento(doc)
    itens = _itens_texto(doc, partes)
    itens.append(_item_margens(doc))
    itens += itens_citacao(doc, partes)
    itens += itens_numeracao(doc, partes)
    itens += itens_titulos(doc, partes)
    if partes["sem_inicio"]:
        itens.append({"chave": "inicio_texto", "item": "Início do texto não identificado",
                      "resultado": "verificar manualmente", "regras": [regra("GRA-12")],
                      "detalhe": "nenhum título de nível 1; o documento inteiro foi tratado como corpo"})
    return {"arquivo": Path(caminho).name, "itens": itens}


def formatar(rel):
    linhas = [f"# Relatório de formatação: {rel['arquivo']}", "",
              "| # | Item | Resultado | Regra | Detalhe |", "|---|---|---|---|---|"]
    n = 0
    ok = ruim = 0
    manuais = []
    for it in rel["itens"]:
        regras = "; ".join(f"{rid} ({org})" for rid, org in it["regras"])
        if it["resultado"] == "verificar manualmente":
            manuais.append(f"- {it['item']}: {it['detalhe']} — {regras}")
            continue
        n += 1
        ok += it["resultado"] == "✔"
        ruim += it["resultado"] == "✘"
        det = it["detalhe"].replace("|", "\\|")
        linhas.append(f"| {n} | {it['item']} | {it['resultado']} | {regras} | {det} |")
    linhas += ["", "## Verificar manualmente", ""]
    linhas += manuais or ["- nenhum item"]
    linhas += ["", f"Resumo: {ok} ✔, {ruim} ✘, {len(manuais)} verificar manualmente"]
    return "\n".join(linhas)


# ---------------------------------------------------------------- saida

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    if len(argv) != 1:
        print("Uso: python verificar_docx.py <arquivo.docx>", file=sys.stderr)
        return 2
    try:
        rel = verificar(argv[0])
    except ErroLeitura as e:
        print(f"Não foi possível ler o arquivo: {e}", file=sys.stderr)
        return 2
    except RegraAusente as e:
        print(f"Regra ausente em references/: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Não foi possível ler o arquivo: {e}", file=sys.stderr)
        return 2
    print(formatar(rel))
    return 1 if any(i["resultado"] == "✘" for i in rel["itens"]) else 0


if __name__ == "__main__":
    sys.exit(main())
