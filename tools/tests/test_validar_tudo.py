import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
import validar_tudo as vt  # noqa: E402

RAIZ = TOOLS.parent
CASO_OK = "# Caso\n\n## Entrada\n\nx\n\n## Esperado\n\ny\n\n## Não pode\n\nz\n"
ARQS = [f"tests/fake/caso-0{i}.md" for i in range(1, 9)]


def tabela_rastreabilidade(arqs, omitir=None):
    linhas = ["| Caso | Briefing (§9) | Arquivo | Modo | O que o caso exige |", "|---|---|---|---|---|"]
    for n, a in enumerate(arqs, 1):
        if n != omitir:
            linhas.append(f"| {n} | b | `{a}` | Revisar | x |")
    return "\n".join(linhas) + "\n"


def tabela_resultados(arqs, estados=None, datas=None):
    linhas = ["| Caso | Arquivo | Data | Resultado | Observação |", "|---|---|---|---|---|"]
    for n, a in enumerate(arqs, 1):
        est = (estados or {}).get(n, "pendente")
        data = (datas or {}).get(n, "-" if est == "pendente" else "2026-10-09")
        linhas.append(f"| {n} | `{a}` | {data} | {est} | |")
    return "\n".join(linhas) + "\n"


def montar(tmp, caso=CASO_OK):
    for a in ARQS:
        p = tmp / a
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(caso, encoding="utf-8")


class TestSecoes(unittest.TestCase):
    def test_completo(self):
        self.assertEqual(vt.secoes_do_caso(CASO_OK), [])

    def test_sem_nao_pode(self):
        t = "## Entrada\n## Esperado\n"
        self.assertEqual(vt.secoes_do_caso(t), ["## Não pode"])

    def test_secao_so_em_bloco_cercado(self):
        t = "## Entrada\n## Não pode\n```\n## Esperado\n```\n"
        self.assertEqual(vt.secoes_do_caso(t), ["## Esperado"])


class TestRastreabilidade(unittest.TestCase):
    def rodar(self, texto, caso=CASO_OK, criar=True):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            if criar:
                montar(tmp, caso)
            r = tmp / "RASTREABILIDADE.md"
            r.write_text(texto, encoding="utf-8")
            return vt.checar_rastreabilidade(r, tmp)

    def test_valida(self):
        mapa, erros = self.rodar(tabela_rastreabilidade(ARQS))
        self.assertEqual(erros, [])
        self.assertEqual(len(mapa), 8)
        self.assertEqual(mapa[3], ARQS[2])

    def test_falta_caso_5(self):
        _, erros = self.rodar(tabela_rastreabilidade(ARQS, omitir=5))
        self.assertTrue(any("5" in e for e in erros))

    def test_arquivo_inexistente(self):
        _, erros = self.rodar(tabela_rastreabilidade(ARQS), criar=False)
        self.assertTrue(erros)

    def test_arquivo_sem_esperado(self):
        _, erros = self.rodar(tabela_rastreabilidade(ARQS), caso="## Entrada\n## Não pode\n")
        self.assertTrue(any("## Esperado" in e for e in erros))


class TestResultados(unittest.TestCase):
    MAPA = {n: a for n, a in enumerate(ARQS, 1)}

    def rodar(self, texto, final=False):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "RESULTADOS.md"
            p.write_text(texto, encoding="utf-8")
            return vt.checar_resultados(p, self.MAPA, final=final)

    def test_pendentes(self):
        estados, erros = self.rodar(tabela_resultados(ARQS))
        self.assertEqual(erros, [])
        self.assertEqual(set(estados.values()), {"pendente"})

    def test_pendentes_final(self):
        _, erros = self.rodar(tabela_resultados(ARQS), final=True)
        self.assertEqual(len(erros), 8)

    def test_passou_sem_data(self):
        _, erros = self.rodar(tabela_resultados(ARQS, {1: "passou"}, {1: "-"}))
        self.assertTrue(erros)

    def test_resultado_invalido(self):
        _, erros = self.rodar(tabela_resultados(ARQS, {2: "ok"}))
        self.assertTrue(erros)

    def test_arquivo_diferente_do_mapa(self):
        outros = list(ARQS)
        outros[0] = "tests/fake/outro.md"
        _, erros = self.rodar(tabela_resultados(outros))
        self.assertTrue(erros)

    def test_oito_passou_final(self):
        estados = {n: "passou" for n in range(1, 9)}
        _, erros = self.rodar(tabela_resultados(ARQS, estados), final=True)
        self.assertEqual(erros, [])


class TestComparar(unittest.TestCase):
    CASO1 = RAIZ / "tests" / "checar" / "caso-01-margem-fonte.md"
    CASO4 = RAIZ / "tests" / "checar" / "caso-04-arquivo-inexistente.md"

    def test_caso_01_real(self):
        self.assertEqual(vt.comparar_checar(self.CASO1, RAIZ), [])

    def test_caso_01_adulterado(self):
        texto = self.CASO1.read_text(encoding="utf-8")
        trocado = texto.replace("| Margens (3/3/2/2 cm) | ✘ |", "| Margens (3/3/2/2 cm) | ✔ |")
        self.assertNotEqual(texto, trocado)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "caso-01-margem-fonte.md"
            p.write_text(trocado, encoding="utf-8")
            self.assertTrue(vt.comparar_checar(p, RAIZ))

    def test_caso_04_real(self):
        self.assertEqual(vt.comparar_checar(self.CASO4, RAIZ), [])


class TestMain(unittest.TestCase):
    def chamar(self, args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            codigo = vt.main(args)
        return codigo, buf.getvalue()

    def test_repositorio_real(self):
        codigo, saida = self.chamar(["--sem-verificadores"])
        self.assertEqual(codigo, 0, saida)
        self.assertIn("validacao ok", saida)

    def final_com(self, estados, datas=None):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "RESULTADOS.md"
            mapa = vt.checar_rastreabilidade(RAIZ / "tests" / "validacao" / "RASTREABILIDADE.md", RAIZ)[0]
            arqs = [mapa[n] for n in range(1, 9)]
            p.write_text(tabela_resultados(arqs, estados, datas), encoding="utf-8")
            return self.chamar(["--sem-verificadores", "--final", "--resultados", str(p)])[0]

    def test_final_pendentes(self):
        self.assertEqual(self.final_com({}), 1)

    def test_final_passou(self):
        self.assertEqual(self.final_com({n: "passou" for n in range(1, 9)}), 0)

    def test_final_uma_sem_data(self):
        estados = {n: "passou" for n in range(1, 9)}
        self.assertEqual(self.final_com(estados, {8: "-"}), 1)


if __name__ == "__main__":
    unittest.main()
