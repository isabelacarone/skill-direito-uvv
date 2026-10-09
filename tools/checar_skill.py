#!/usr/bin/env python
"""Verificacao estrutural da skill abnt-uvv-direito (SKILL.md, references/, casos)."""
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import checar_references as cr  # noqa: E402

RAIZ = cr.RAIZ
SKILL = RAIZ / ".claude" / "skills" / "abnt-uvv-direito"
CASOS = RAIZ / "tests" / "revisar"
ARQUIVOS = [
    "formatacao-grafica", "pre-textuais", "citacoes",
    "tabelas-ilustracoes", "referencias-direito", "regras-curso-direito",
]
MAX_LINHAS = 150
OBRIGATORIAS = [
    "Conforme", "Ajustes necessários", "Crítico",
    "| # | Trecho original | Origem da regra | Problema | Correção |",
    "[Inserir autor, ano, p.]", "não consta no manual UVV",
    "Regra do curso", "NBR geral", "12 pt", "sem `< >`",
    "https://repositorio.uvv.br/handle/123456789/88",
    "Origem da regra",
]
SECOES_CASO = ["## Entrada", "## Esperado", "## Não pode"]
CITACAO = re.compile(r"Manual (\d+(?:\.\d+)*), p\. (\d+)(?:[–-](\d+))?")


def checar(skill=SKILL, casos=CASOS, mapa=None):
    erros = []
    if mapa is None:
        mapa = json.loads((cr.TOOLS / "manual_mapa.json").read_text(encoding="utf-8"))
    sk = Path(skill) / "SKILL.md"
    if not sk.exists():
        return ["SKILL.md ausente"]
    texto = sk.read_text(encoding="utf-8")
    linhas = texto.splitlines()
    if len(linhas) > MAX_LINHAS:
        erros.append(f"SKILL.md tem {len(linhas)} linhas (max {MAX_LINHAS})")
    fm = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    if not fm:
        erros.append("frontmatter ausente")
    else:
        if not re.search(r"^name: abnt-uvv-direito$", fm.group(1), re.M):
            erros.append("falta 'name: abnt-uvv-direito'")
        if not re.search(r"^description: \S", fm.group(1), re.M):
            erros.append("description vazio")
    for nome in ARQUIVOS:
        if not (Path(skill) / "references" / f"{nome}.md").exists():
            erros.append(f"references/{nome}.md ausente")
        if f"references/{nome}.md" not in texto:
            erros.append(f"SKILL.md nao cita references/{nome}.md")
    for s in OBRIGATORIAS:
        if s not in texto:
            erros.append(f"string obrigatoria ausente: {s}")
    for m in CITACAO.finditer(texto):
        parte = m.group(0)
        msg = cr.checar_origem(parte, mapa)
        if msg:
            erros.append(f"SKILL.md: {msg}")
    ids = {}
    ref = Path(skill) / "references"
    if ref.exists():
        for a in sorted(ref.glob("*.md")):
            erros += cr.checar_arquivo(a, mapa, ids)
    arqs = sorted(Path(casos).glob("caso-*.md")) if Path(casos).exists() else []
    if len(arqs) < 6:
        erros.append(f"apenas {len(arqs)} casos em tests/revisar (min 6)")
    for a in arqs:
        t = a.read_text(encoding="utf-8")
        for s in SECOES_CASO:
            if s not in t:
                erros.append(f"{a.name}: falta '{s}'")
    return erros


def autoteste():
    """Cada defeito simulado precisa gerar erro; a skill minima sem defeito, nao."""
    ok = True
    mapa = json.loads((cr.TOOLS / "manual_mapa.json").read_text(encoding="utf-8"))
    base = SKILL.joinpath("SKILL.md").read_text(encoding="utf-8")

    def montar(tmp, texto, remover=None, casos=6):
        sk = tmp / "skill"
        (sk / "references").mkdir(parents=True)
        for a in ARQUIVOS:
            if a != remover:
                (sk / "references" / f"{a}.md").write_text(
                    (SKILL / "references" / f"{a}.md").read_text(encoding="utf-8"), encoding="utf-8")
        (sk / "SKILL.md").write_text(texto, encoding="utf-8")
        cs = tmp / "casos"
        cs.mkdir()
        for i in range(casos):
            (cs / f"caso-0{i}.md").write_text("## Entrada\n## Esperado\n## Não pode\n", encoding="utf-8")
        return sk, cs

    defeitos = {
        "controle (sem defeito)": (base, None, 6, False),
        "references ausente": (base, "citacoes", 6, True),
        "SKILL.md longo": (base + "\nx" * 200, None, 6, True),
        "sem name": (base.replace("name: abnt-uvv-direito", "name: outra", 1), None, 6, True),
        "string obrigatoria": (base.replace("[Inserir autor, ano, p.]", "[x]"), None, 6, True),
        "pagina fora do mapa": (base + "\nManual 4.1.3, p. 9\n", None, 6, True),
        "poucos casos": (base, None, 3, True),
    }
    for nome, (texto, remover, casos, esperado_erro) in defeitos.items():
        with tempfile.TemporaryDirectory() as t:
            sk, cs = montar(Path(t), texto, remover, casos)
            erros = checar(sk, cs, mapa)
        if bool(erros) != esperado_erro:
            print(f"FALHA no autoteste: {nome} (erros={erros[:2]})")
            ok = False
    print("autoteste ok" if ok else "autoteste falhou")
    return 0 if ok else 1


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = list(sys.argv[1:] if argv is None else argv)
    if "--autoteste" in args:
        return autoteste()
    erros = checar()
    for e in erros:
        print(e)
    if erros:
        return 1
    print("skill ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
