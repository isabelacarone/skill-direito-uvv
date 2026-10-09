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
    estilos = par.part.styles.element
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


def verificar(caminho):
    doc = abrir(caminho)
    partes = partes_do_documento(doc)
    itens = _itens_texto(doc, partes)
    itens.append(_item_margens(doc))
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
