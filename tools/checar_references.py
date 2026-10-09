#!/usr/bin/env python
"""Verificador do contrato de linha de regra dos arquivos references/*.md."""
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
RAIZ = TOOLS.parent
PADRAO = RAIZ / ".claude" / "skills" / "abnt-uvv-direito" / "references"

PREFIXOS = {
    "formatacao-grafica": "GRA",
    "pre-textuais": "PRE",
    "citacoes": "CIT",
    "tabelas-ilustracoes": "TAB",
    "referencias-direito": "REF",
    "regras-curso-direito": "CUR",
}
REGRA = re.compile(r"^- \*\*([A-Z]+)-(\d+)\*\*\s+(.*)$")
MANUAL_ITEM = re.compile(r"^Manual (\d+(?:\.\d+)*), p\. (\d+)(?:[–-](\d+))?$")
MANUAL_SEM_ITEM = re.compile(r"^Manual, p\. (\d+)$")
CURSO = re.compile(r"^Regra do curso \((?:Projeto de Pesquisa|Estudo Dirigido I), [^)]+\)$")
NBR = re.compile(r"^(?:NBR \d+:\d{4}|NBR geral)$")
AUTORA = "Decisão da autora"
PENDENCIA = re.compile(r"p\. \?|p\. X\b|\bTODO\b|\[conferir\]")


def checar_origem(parte, mapa):
    """Retorna None se valida, ou mensagem de erro."""
    if CURSO.match(parte) or NBR.match(parte):
        return None
    m = MANUAL_ITEM.match(parte)
    if m:
        item = m.group(1)
        info = mapa["itens"].get(item)
        if info is None:
            return f"item {item} inexistente no mapa do manual"
        for n in (m.group(2), m.group(3)):
            if n is not None and not info["inicio"] <= int(n) <= info["fim"]:
                return f"p. {n} fora do intervalo do item {item} (permitido {info['inicio']}–{info['fim']})"
        if m.group(3) is not None and int(m.group(3)) < int(m.group(2)):
            return f"intervalo invertido em '{parte}'"
        return None
    m = MANUAL_SEM_ITEM.match(parte)
    if m:
        if m.group(1) not in mapa["paginas"]:
            return f"p. {m.group(1)} nao e pagina impressa existente no manual"
        return None
    return f"origem invalida: '{parte}'"


def checar_arquivo(caminho, mapa, ids_vistos):
    caminho = Path(caminho)
    nome = caminho.name
    erros = []

    def erro(n, msg):
        erros.append(f"{nome}:{n}: {msg}")

    linhas = caminho.read_text(encoding="utf-8").splitlines()
    if not linhas or not linhas[0].startswith("# "):
        erro(1, "arquivo deve comecar com '# <Titulo>'")
    if not any(l.startswith("> Fonte:") for l in linhas):
        erro(1, "falta a linha '> Fonte: ...'")
    prefixo = PREFIXOS.get(caminho.stem)
    for n, linha in enumerate(linhas, 1):
        if PENDENCIA.search(linha):
            erro(n, "marcador de pendencia (p. ?, p. X, TODO, [conferir])")
        if not linha.startswith("- "):
            continue
        m = REGRA.match(linha)
        if not m:
            erro(n, "bullet de regra sem ID no formato '- **XXX-NN** ...'")
            continue
        pref, num = m.group(1), m.group(2)
        rid = f"{pref}-{num}"
        if prefixo is not None and pref != prefixo:
            erro(n, f"prefixo {pref} incorreto para {nome} (esperado {prefixo})")
        if rid in ids_vistos:
            erro(n, f"ID {rid} repetido (ja usado em {ids_vistos[rid]})")
        else:
            ids_vistos[rid] = f"{nome}:{n}"
        corpo = m.group(3)
        if " — " not in corpo:
            erro(n, f"{rid}: regra sem origem")
            continue
        origem = corpo.rsplit(" — ", 1)[1].strip()
        partes = [p.strip() for p in origem.split("; ") if p.strip()]
        if not partes:
            erro(n, f"{rid}: regra sem origem")
            continue
        validas = [p for p in partes if p != AUTORA]
        if not validas:
            erro(n, f"{rid}: '{AUTORA}' so vale junto de outra origem")
        for p in validas:
            msg = checar_origem(p, mapa)
            if msg:
                erro(n, f"{rid}: {msg}")
    return erros


def contar_regras(caminho):
    return sum(1 for l in Path(caminho).read_text(encoding="utf-8").splitlines() if REGRA.match(l))


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = list(sys.argv[1:] if argv is None else argv)
    alvos = []
    for a in args or [str(PADRAO)]:
        p = Path(a)
        alvos += sorted(p.glob("*.md")) if p.is_dir() else [p]
    mapa = json.loads((TOOLS / "manual_mapa.json").read_text(encoding="utf-8"))
    ids, erros, regras = {}, [], 0
    for a in alvos:
        erros += checar_arquivo(a, mapa, ids)
        regras += contar_regras(a)
    for e in erros:
        print(e)
    print(f"{regras} regras, {len(erros)} erros")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
