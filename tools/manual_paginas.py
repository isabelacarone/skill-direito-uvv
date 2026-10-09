#!/usr/bin/env python
"""Mapa pagina impressa <-> pagina do PDF e item -> intervalo de paginas do Manual UVV 2024.

Subcomandos: mapa | texto <impressa> | render <impressa> --saida DIR
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PDF = RAIZ / "docs" / "MANUAL ABNT 2024 uvv.pdf"
MAPA = Path(__file__).resolve().parent / "manual_mapa.json"
TOTAL_PDF = 72
TITULO = re.compile(r"^(\d+(?:\.\d+){0,4})\s+(\S.*)$")
SUMARIO = re.compile(r"^(\d+(?:\.\d+){0,4})\s+(.+?)\s*\.{2,}\s*(\d+|Erro!.*)$")


def pagina_pdf(p):
    r = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", "-f", str(p), "-l", str(p), str(PDF), "-"],
        capture_output=True, check=True,
    )
    return r.stdout.decode("utf-8")


def impressa_de(texto):
    for linha in texto.splitlines():
        if linha.strip():
            s = linha.strip()
            return int(s) if s.isdigit() else None
    return None


def chave(item):
    return tuple(int(x) for x in item.split("."))


def gerar():
    paginas, corpo, sumario = {}, [], {}
    for p in range(1, TOTAL_PDF + 1):
        texto = pagina_pdf(p)
        imp = impressa_de(texto)
        if imp is None:
            if 4 <= p <= 7:
                for linha in texto.splitlines():
                    m = SUMARIO.match(linha.strip())
                    if m:
                        pg = m.group(3)
                        sumario[m.group(1)] = int(pg) if pg.isdigit() else None
            continue
        paginas[str(imp)] = p
        for linha in texto.splitlines()[1:]:
            m = TITULO.match(linha.strip())
            if m and ("." in m.group(1) or m.group(2).isupper()):
                corpo.append((m.group(1), imp, m.group(2)))
    # primeira ocorrencia de cada item, mantendo so a ordem crescente do documento
    inicios, ordem, ultimo = {}, [], ()
    for item, imp, _ in corpo:
        if item in inicios:
            continue
        k = chave(item)
        if ultimo and k < ultimo:
            continue
        # evita falsos positivos (ex.: listas numeradas): item de nivel N exige o pai ja visto
        if "." in item and item.rsplit(".", 1)[0] not in inicios:
            continue
        inicios[item] = imp
        ordem.append(item)
        ultimo = k
    for item in ordem:
        s = sumario.get(item)
        if item in sumario and s is not None and s != inicios[item]:
            print(f"AVISO: item {item}: corpo p. {inicios[item]} x sumario p. {s} (vale o corpo)", file=sys.stderr)
        if item not in sumario:
            print(f"AVISO: item {item} (corpo p. {inicios[item]}) ausente do sumario", file=sys.stderr)
    for item in sumario:
        if item not in inicios:
            print(f"AVISO: item {item} do sumario (p. {sumario[item]}) nao achado no corpo", file=sys.stderr)
    so_sumario = sorted((i for i in sumario if i not in inicios), key=chave)
    ultima = max(int(k) for k in paginas)
    itens = {}
    for i, item in enumerate(ordem):
        fim = inicios[ordem[i + 1]] if i + 1 < len(ordem) else ultima
        itens[item] = {"inicio": inicios[item], "fim": max(fim, inicios[item])}
    dados = {"total_pdf": TOTAL_PDF, "paginas": dict(sorted(paginas.items(), key=lambda kv: int(kv[0]))), "itens": itens, "somente_sumario": so_sumario}
    MAPA.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(paginas)} paginas, {len(itens)} itens -> {MAPA}")


def carregar():
    return json.loads(MAPA.read_text(encoding="utf-8"))


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("mapa")
    t = sub.add_parser("texto")
    t.add_argument("impressa", type=int)
    r = sub.add_parser("render")
    r.add_argument("impressa", type=int)
    r.add_argument("--saida", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "mapa":
        gerar()
        return 0
    m = carregar()
    p = m["paginas"].get(str(a.impressa))
    if p is None:
        print(f"pagina impressa {a.impressa} inexistente", file=sys.stderr)
        return 1
    if a.cmd == "texto":
        print(pagina_pdf(p))
    else:
        base = Path(a.saida) / f"manual_p{a.impressa}"
        base.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-png", "-r", "70", "-f", str(p), "-l", str(p), "-singlefile", str(PDF), str(base)], check=True)
        print(str(base) + ".png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
