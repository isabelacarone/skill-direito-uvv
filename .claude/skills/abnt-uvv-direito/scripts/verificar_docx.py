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
