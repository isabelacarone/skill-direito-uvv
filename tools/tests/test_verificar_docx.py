import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

RAIZ = Path(__file__).resolve().parent.parent.parent
SKILL = RAIZ / ".claude" / "skills" / "abnt-uvv-direito"
SCRIPT = SKILL / "scripts" / "verificar_docx.py"
GERADOR = RAIZ / "tests" / "checar" / "gerar_fixtures.py"


def carregar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vd = carregar("verificar_docx", SCRIPT)  # falha se o script nao existe
        cls.gf = carregar("gerar_fixtures", GERADOR)
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.tmp.name)
        cls.c01 = cls.dir / "caso-01.docx"
        cls.c03 = cls.dir / "caso-03.docx"
        cls.gf.gerar_caso01(cls.c01)
        cls.gf.gerar_caso03(cls.c03)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def itens(self, caminho):
        rel = self.vd.verificar(str(caminho))
        return {i["chave"]: i for i in rel["itens"]}

    def cli(self, caminho):
        r = subprocess.run([sys.executable, str(SCRIPT), str(caminho)], capture_output=True)
        return r.returncode, r.stdout.decode("utf-8"), r.stderr.decode("utf-8")


class TestOrigem(Base):
    def test_origem(self):
        self.assertEqual(self.vd.origem("GRA-09"), "Manual 3.2, p. 32")
        self.assertEqual(self.vd.origem("GRA-03"), "Manual 3.1, p. 32")

    def test_origem_ausente(self):
        with self.assertRaises(self.vd.RegraAusente):
            self.vd.origem("GRA-99")

    def test_trechos_dos_limiares(self):
        self.assertTrue(self.vd.LIMIARES)
        for rid, lim in self.vd.LIMIARES.items():
            bloco = self.vd.bloco_regra(rid)
            for trecho in lim["texto"]:
                self.assertIn(trecho, bloco, f"{rid}: {trecho!r}")


class TestArquivo(Base):
    def test_recusas(self):
        docm = self.dir / "a.docm"
        docm.write_bytes(b"PK\x03\x04")
        txt = self.dir / "a.txt"
        txt.write_text("x", encoding="utf-8")
        for p in (docm, txt, self.dir / "nao-existe.docx"):
            codigo, out, err = self.cli(p)
            self.assertEqual(codigo, 2, str(p))
            self.assertNotIn("Traceback", err)
            self.assertIn("Não foi possível ler o arquivo", err)

    def test_docx_falso(self):
        f = self.dir / "falso.docx"
        f.write_text("nao e zip", encoding="utf-8")
        codigo, _, err = self.cli(f)
        self.assertEqual(codigo, 2)
        self.assertNotIn("Traceback", err)


class TestCorpo(Base):
    def test_caso01(self):
        it = self.itens(self.c01)
        self.assertEqual(it["margens"]["resultado"], "✘")
        self.assertIn("2,5 cm", it["margens"]["detalhe"])
        self.assertIn("GRA-09", [r[0] for r in it["margens"]["regras"]])
        self.assertEqual(it["fonte_corpo"]["resultado"], "✘")
        self.assertIn("Times New Roman", it["fonte_corpo"]["detalhe"])
        self.assertIn("GRA-03", [r[0] for r in it["fonte_corpo"]["regras"]])
        for k in ("tamanho_corpo", "entrelinhas_corpo", "alinhamento_corpo"):
            self.assertEqual(it[k]["resultado"], "✔", k)

    def test_caso03(self):
        it = self.itens(self.c03)
        for k in ("fonte_corpo", "tamanho_corpo", "entrelinhas_corpo",
                  "alinhamento_corpo", "margens"):
            self.assertEqual(it[k]["resultado"], "✔", k)
        self.assertFalse([i for i in it.values() if i["resultado"] == "✘"])

    def test_fonte_mista(self):
        p = self.dir / "mista.docx"
        self.gf.gerar_caso03(p)
        d = Document(str(p))
        alvo = [x for x in d.paragraphs if x.text.startswith("Este paragrafo")][0]
        alvo.runs[0].font.name = "Times New Roman"
        d.save(str(p))
        it = self.itens(p)
        self.assertEqual(it["fonte_corpo"]["resultado"], "✘")
        self.assertIn("1 de", it["fonte_corpo"]["detalhe"])

    def test_mirror_margins(self):
        p = self.dir / "espelho.docx"
        self.gf.gerar_caso03(p)
        d = Document(str(p))
        d.settings.element.append(OxmlElement("w:mirrorMargins"))
        d.save(str(p))
        it = self.itens(p)
        self.assertEqual(it["margens"]["resultado"], "verificar manualmente")
        self.assertIn("GRA-10", [r[0] for r in it["margens"]["regras"]])


class TestCLI(Base):
    def test_caso01(self):
        codigo, out, _ = self.cli(self.c01)
        self.assertEqual(codigo, 1)
        self.assertIn("| # | Item | Resultado | Regra | Detalhe |", out)
        self.assertIn("✘", out)
        self.assertIn("GRA-09 (Manual 3.2, p. 32)", out)
        self.assertIn("GRA-03 (Manual 3.1, p. 32)", out)
        self.assertIn("## Verificar manualmente", out)
        self.assertRegex(out, r"Resumo: \d+ ✔, \d+ ✘, \d+ verificar manualmente")

    def test_caso03(self):
        codigo, out, _ = self.cli(self.c03)
        self.assertEqual(codigo, 0)
        self.assertNotIn("✘", out)

    def test_nao_escreve(self):
        antes = self.c03.read_bytes()
        self.cli(self.c03)
        self.assertEqual(antes, self.c03.read_bytes())
        self.assertEqual(sorted(x.name for x in self.dir.glob("~*")), [])


if __name__ == "__main__":
    unittest.main()
