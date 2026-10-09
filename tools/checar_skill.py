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
CASOS_FORMATAR = RAIZ / "tests" / "formatar"
MIN_FORMATAR = 2
PROIBIDAS_SKILL = ["Fase 2", "ainda não gera"]
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
    "Origem da regra", "## Fluxo do modo Formatar", "Regra aplicada:",
]
SECOES_CASO = ["## Entrada", "## Esperado", "## Não pode"]
CITACAO = re.compile(r"Manual (\d+(?:\.\d+)*), p\. (\d+)(?:[–-](\d+))?")


def checar(skill=SKILL, casos=CASOS, mapa=None, casos_formatar=CASOS_FORMATAR):
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
    for s in PROIBIDAS_SKILL:
        if s in texto:
            erros.append(f"SKILL.md contem texto proibido: {s}")
    # modo Formatar: casos fixos, origem copiada de references/, link e data de acesso
    linhas_ref = []
    if ref.exists():
        for a in sorted(ref.glob("*.md")):
            linhas_ref += a.read_text(encoding="utf-8").splitlines()
            for n, l in enumerate(a.read_text(encoding="utf-8").splitlines(), 1):
                erros += _erros_acesso(l, f"references/{a.name}:{n}")
    arqs_f = sorted(Path(casos_formatar).glob("caso-*.md")) if Path(casos_formatar).exists() else []
    if len(arqs_f) < MIN_FORMATAR:
        erros.append(f"apenas {len(arqs_f)} casos em tests/formatar (min {MIN_FORMATAR})")
    for a in arqs_f:
        t = a.read_text(encoding="utf-8")
        for s in SECOES_CASO:
            if s not in t:
                erros.append(f"{a.name}: falta '{s}'")
        for m in CITACAO.finditer(t):
            if not any(m.group(0) in l for l in linhas_ref):
                erros.append(f"{a.name}: origem '{m.group(0)}' nao aparece em nenhuma linha de references/")
        esperado = re.search(r"^## Esperado\n(.*?)(?=^## |\Z)", t, re.S | re.M)
        corpo = esperado.group(1) if esperado else ""
        if "<http" in corpo:
            erros.append(f"{a.name}: link com < > em Esperado")
        for l in corpo.splitlines():
            erros += _erros_acesso(l, a.name)
    return erros


ACESSO = re.compile(r"Acesso em: (?=\d)")
ACESSO_OK = re.compile(r"Acesso em: \d{1,2} (jan\.|fev\.|mar\.|abr\.|maio|jun\.|jul\.|ago\.|set\.|out\.|nov\.|dez\.) \d{4}")


def _erros_acesso(linha, onde):
    erros = []
    for m in ACESSO.finditer(linha):
        if not ACESSO_OK.match(linha, m.start()):
            erros.append(f"{onde}: data de acesso fora do padrao (mes abreviado)")
    return erros


def base_controle():
    """SKILL.md real sem as marcas da Fase 1 e com o minimo do modo Formatar."""
    linhas = SKILL.joinpath("SKILL.md").read_text(encoding="utf-8").splitlines()
    linhas = [l for l in linhas if not any(p in l for p in PROIBIDAS_SKILL)]
    texto = "\n".join(linhas)
    if "## Fluxo do modo Formatar" not in texto:
        texto += "\n## Fluxo do modo Formatar"
    if "Regra aplicada:" not in texto:
        texto += "\nRegra aplicada: Manual 4.1.1, p. 36"
    return texto + "\n"


CASO_NEUTRO = "## Entrada\n## Esperado\nsaida neutra\n## Não pode\n"


def autoteste():
    """Cada defeito simulado precisa gerar erro; a skill minima sem defeito, nao."""
    ok = True
    mapa = json.loads((cr.TOOLS / "manual_mapa.json").read_text(encoding="utf-8"))
    base = base_controle()

    def montar(tmp, texto, remover=None, casos=6, formatar=2, caso_f=CASO_NEUTRO):
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
        cf = tmp / "formatar"
        cf.mkdir()
        for i in range(formatar):
            (cf / f"caso-0{i}.md").write_text(caso_f, encoding="utf-8")
        return sk, cs, cf

    def caso(esperado):
        return f"## Entrada\n## Esperado\n{esperado}\n## Não pode\n"

    # nome: (skill, references removido, casos revisar, casos formatar, texto do caso formatar, erro esperado)
    defeitos = {
        "controle (sem defeito)": (base, None, 6, 2, CASO_NEUTRO, False),
        "references ausente": (base, "citacoes", 6, 2, CASO_NEUTRO, True),
        "SKILL.md longo": (base + "\nx" * 200, None, 6, 2, CASO_NEUTRO, True),
        "sem name": (base.replace("name: abnt-uvv-direito", "name: outra", 1), None, 6, 2, CASO_NEUTRO, True),
        "string obrigatoria": (base.replace("[Inserir autor, ano, p.]", "[x]"), None, 6, 2, CASO_NEUTRO, True),
        "pagina fora do mapa": (base + "\nManual 4.1.3, p. 9\n", None, 6, 2, CASO_NEUTRO, True),
        "poucos casos": (base, None, 3, 2, CASO_NEUTRO, True),
        "formatar sem Esperado": (base, None, 6, 2, "## Entrada\n## Não pode\n", True),
        "origem fabricada no caso": (base, None, 6, 2, caso("Regra aplicada: Manual 4.1.2, p. 37"), True),
        "link com < >": (base, None, 6, 2, caso("Disponível em: <http://x.br>."), True),
        "mes por extenso": (base, None, 6, 2, caso("Acesso em: 26 de junho de 2019."), True),
        "mes abreviado": (base, None, 6, 2, caso("Acesso em: 26 jun. 2019."), False),
        "maio sem ponto": (base, None, 6, 2, caso("Acesso em: 3 maio 2020."), False),
        "Fase 2 no SKILL": (base + "\nFase 2\n", None, 6, 2, CASO_NEUTRO, True),
        "sem fluxo Formatar": (base.replace("## Fluxo do modo Formatar", "## X"), None, 6, 2, CASO_NEUTRO, True),
        "poucos casos formatar": (base, None, 6, 1, CASO_NEUTRO, True),
    }
    for nome, (texto, remover, casos, formatar, caso_f, esperado_erro) in defeitos.items():
        with tempfile.TemporaryDirectory() as t:
            sk, cs, cf = montar(Path(t), texto, remover, casos, formatar, caso_f)
            erros = checar(sk, cs, mapa, casos_formatar=cf)
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
