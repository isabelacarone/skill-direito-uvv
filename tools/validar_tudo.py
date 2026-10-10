#!/usr/bin/env python
"""Entrypoint unico da validacao dos 8 casos do briefing da skill abnt-uvv-direito."""
import os
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SECOES_CASO = ["## Entrada", "## Esperado", "## Não pode"]
RESULTADOS_VALIDOS = {"pendente", "passou", "falhou"}
DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINHA_CASO = re.compile(r"^\| *([1-8]) *\|")
CERCA = re.compile(r"^```.*?^```[ \t]*$", re.S | re.M)
SCRIPT_DOCX = Path(".claude") / "skills" / "abnt-uvv-direito" / "scripts" / "verificar_docx.py"


def _fora_de_blocos(texto):
    return CERCA.sub("", texto)


def secoes_do_caso(texto):
    fora = _fora_de_blocos(texto)
    return [s for s in SECOES_CASO if not re.search(r"^" + re.escape(s) + r"\s*$", fora, re.M)]


def _celulas(linha):
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def _caminho_da_celula(celula):
    m = re.search(r"`([^`]+)`", celula)
    return m.group(1) if m else celula.strip()


def _linhas_tabela(caminho):
    for linha in Path(caminho).read_text(encoding="utf-8").splitlines():
        m = LINHA_CASO.match(linha)
        if m:
            yield int(m.group(1)), _celulas(linha)


def checar_rastreabilidade(caminho, raiz):
    mapa, erros = {}, []
    for n, cel in _linhas_tabela(caminho):
        if n in mapa:
            erros.append(f"caso {n}: repetido em RASTREABILIDADE.md")
            continue
        if len(cel) < 3:
            erros.append(f"caso {n}: linha sem coluna Arquivo")
            continue
        mapa[n] = _caminho_da_celula(cel[2])
    for n in range(1, 9):
        if n not in mapa:
            erros.append(f"caso {n}: ausente em RASTREABILIDADE.md")
    for n, rel in sorted(mapa.items()):
        arq = Path(raiz) / rel
        if not arq.is_file():
            erros.append(f"caso {n}: arquivo nao existe: {rel}")
            continue
        for s in secoes_do_caso(arq.read_text(encoding="utf-8")):
            erros.append(f"caso {n}: {rel} sem '{s}'")
    return mapa, erros


def checar_resultados(caminho, mapa, final=False):
    estados, erros = {}, []
    for n, cel in _linhas_tabela(caminho):
        if n in estados:
            erros.append(f"caso {n}: repetido em RESULTADOS.md")
            continue
        if len(cel) < 4:
            erros.append(f"caso {n}: linha incompleta em RESULTADOS.md")
            continue
        arq, data, res = _caminho_da_celula(cel[1]), cel[2], cel[3]
        estados[n] = res
        if n in mapa and arq != mapa[n]:
            erros.append(f"caso {n}: arquivo {arq} diverge de RASTREABILIDADE.md ({mapa[n]})")
        if res not in RESULTADOS_VALIDOS:
            erros.append(f"caso {n}: resultado invalido '{res}'")
        elif res != "pendente" and not DATA.match(data):
            erros.append(f"caso {n}: resultado '{res}' sem data AAAA-MM-DD")
        if final and res != "passou":
            erros.append(f"caso {n}: nao esta 'passou' (estado: {res})")
    for n in range(1, 9):
        if n not in estados:
            erros.append(f"caso {n}: ausente em RESULTADOS.md")
    return estados, erros


def _secao(texto, titulo):
    """Corpo da secao `titulo`, ignorando '## ' dentro de blocos cercados."""
    linhas, dentro, cerca, corpo = texto.splitlines(), False, False, []
    for l in linhas:
        if l.startswith("```"):
            cerca = not cerca
        if not cerca and not l.startswith("```") and re.match(r"^## ", l):
            if dentro:
                break
            dentro = l.strip() == titulo
            continue
        if dentro:
            corpo.append(l)
    return "\n".join(corpo)


def _rodar(args, raiz):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable] + args, cwd=str(raiz), env=env, capture_output=True)
    return (p.returncode, p.stdout.decode("utf-8", errors="replace"),
            p.stderr.decode("utf-8", errors="replace"))


def comparar_checar(caso_md, raiz):
    texto = Path(caso_md).read_text(encoding="utf-8")
    nome = Path(caso_md).name
    entrada = _secao(texto, "## Entrada")
    esperado = _secao(texto, "## Esperado")
    bloco = None
    for m in re.finditer(r"^```[^\n]*\n(.*?)^```[ \t]*$", esperado, re.S | re.M):
        if m.group(1).lstrip().startswith("# Relatório de formatação:"):
            bloco = m.group(1)
            break
    if bloco is not None:
        m = re.search(r"tests/checar/[\w.-]+\.docx", entrada)
        if not m:
            return [f"{nome}: Entrada sem caminho tests/checar/*.docx"]
        docx = Path(raiz) / m.group(0)
        cod, saida, _ = _rodar([str(SCRIPT_DOCX), m.group(0)], raiz)
        if not docx.is_file():
            return [f"{nome}: {m.group(0)} nao existe"]
        resumo = re.search(r"^Resumo:.*?(\d+) ✘", bloco, re.M)
        cod_esperado = 1 if resumo and int(resumo.group(1)) != 0 else 0
        erros = []
        if cod != cod_esperado:
            erros.append(f"{nome}: codigo de saida {cod}, esperado {cod_esperado}")
        real = [l.rstrip() for l in saida.strip().splitlines()]
        fixo = [l.rstrip() for l in bloco.strip().splitlines()]
        for i in range(max(len(real), len(fixo))):
            a = real[i] if i < len(real) else "(fim da saida)"
            b = fixo[i] if i < len(fixo) else "(fim do bloco)"
            if a != b:
                erros.append(f"{nome}: linha {i + 1} diverge\n  real:   {a}\n  fixado: {b}")
                break
        return erros
    m = re.search(r"[^\s\"']+\.docx", entrada)
    if not m:
        return []
    cod, _, err = _rodar([str(SCRIPT_DOCX), m.group(0)], raiz)
    erros = []
    if cod != 2:
        erros.append(f"{nome}: codigo de saida {cod}, esperado 2")
    msg = next((t for t in re.findall(r"`([^`]+)`", esperado)
                if t.startswith("Não foi possível ler o arquivo")), None)
    if msg is None:
        erros.append(f"{nome}: Esperado sem a mensagem de erro entre crases")
    elif msg not in err:
        erros.append(f"{nome}: stderr sem a mensagem '{msg}'")
    return erros


def rodar_verificadores(raiz):
    passos = [
        ("checar_references", ["tools/checar_references.py"]),
        ("checar_skill", ["tools/checar_skill.py"]),
        ("checar_skill --autoteste", ["tools/checar_skill.py", "--autoteste"]),
        ("unittest", ["-m", "unittest", "discover", "-s", "tools/tests"]),
    ]
    res = []
    for nome, args in passos:
        cod, out, err = _rodar(args, raiz)
        res.append((nome, cod == 0, (out + err).strip()))
    return res


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = list(sys.argv[1:] if argv is None else argv)
    final = "--final" in args

    def valor(flag, padrao):
        return Path(args[args.index(flag) + 1]) if flag in args else padrao

    raiz = valor("--raiz", RAIZ)
    resultados = valor("--resultados", raiz / "tests" / "validacao" / "RESULTADOS.md")
    erros = []

    if "--sem-verificadores" not in args:
        for nome, ok, saida in rodar_verificadores(raiz):
            print(f"{nome}: {'ok' if ok else 'FALHOU'}")
            if not ok:
                erros.append(f"verificador {nome} falhou")
                for l in saida.splitlines()[-10:]:
                    print(f"  {l}")

    mapa, e_rast = checar_rastreabilidade(raiz / "tests" / "validacao" / "RASTREABILIDADE.md", raiz)
    estados, e_res = checar_resultados(resultados, mapa, final=final)

    e_checar = {}
    for caso in sorted((raiz / "tests" / "checar").glob("caso-*.md")):
        e = comparar_checar(caso, raiz)
        if e:
            e_checar[caso.name] = e
    mapeados = {Path(rel).name for rel in mapa.values() if rel.startswith("tests/checar/")}
    soltos = [n for n in e_checar if n not in mapeados]

    print()
    print("| Caso | Arquivo | Automático | Autora |")
    print("|---|---|---|---|")
    for n in range(1, 9):
        rel = mapa.get(n, "-")
        falhou = any(e.startswith(f"caso {n}:") for e in e_rast) or Path(rel).name in e_checar
        print(f"| {n} | {rel} | {'FALHOU' if falhou else 'ok'} | {estados.get(n, '-')} |")
    print()

    todos = e_rast + e_res + [e for n in e_checar for e in e_checar[n]]
    for e in todos:
        print(e)
    if soltos:
        print("casos de tests/checar fora do mapa com erro: " + ", ".join(soltos))
    erros += todos
    ok = not erros
    print("validacao ok" if ok else "validacao falhou")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
