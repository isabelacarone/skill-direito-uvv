import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
import checar_references as cr  # noqa: E402

MAPA = json.loads((TOOLS / "manual_mapa.json").read_text(encoding="utf-8"))
CAB = "# Titulo\n\n> Fonte: Manual UVV 2024. Páginas = numeração impressa do Manual UVV 2024.\n\n## Secao\n\n"


class Base(unittest.TestCase):
    def checar(self, corpo, nome="citacoes.md", ids=None, cab=CAB):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / nome
            p.write_text(cab + corpo, encoding="utf-8")
            return cr.checar_arquivo(p, MAPA, ids if ids is not None else {})


class TestChecar(Base):
    def test_linha_valida(self):
        self.assertEqual(self.checar("- **CIT-01** Página obrigatória na citação direta. — Manual 4.1.1, p. 36\n"), [])

    def test_pagina_fora_do_intervalo(self):
        e = self.checar("- **CIT-01** Regra. — Manual 4.1.1, p. 50\n")
        self.assertEqual(len(e), 1)
        self.assertIn("4.1.1", e[0])
        self.assertIn("36", e[0])

    def test_sem_origem(self):
        e = self.checar("- **CIT-01** Regra sem origem.\n")
        self.assertTrue(any("sem origem" in x for x in e))

    def test_regra_do_curso_com_parenteses(self):
        self.assertEqual(self.checar("- **CIT-01** R. — Regra do curso (Projeto de Pesquisa, Orientações Gerais)\n"), [])
        self.assertEqual(self.checar("- **CIT-01** R. — Regra do curso (Estudo Dirigido I, item 7)\n"), [])

    def test_regra_do_curso_sem_parenteses(self):
        self.assertTrue(self.checar("- **CIT-01** R. — Regra do curso\n"))

    def test_item_inexistente(self):
        e = self.checar("- **CIT-01** R. — Manual 9.9.9, p. 10\n")
        self.assertTrue(any("9.9.9" in x for x in e))

    def test_item_somente_sumario(self):
        self.assertTrue(self.checar("- **CIT-01** R. — Manual 4.1.9, p. 39\n"))

    def test_id_repetido(self):
        ids = {}
        self.assertEqual(self.checar("- **CIT-01** R. — Manual 4.1.1, p. 36\n", ids=ids), [])
        e = self.checar("- **CIT-01** R. — Manual 4.1.1, p. 36\n", nome="citacoes.md", ids=ids)
        self.assertTrue(any("repetido" in x for x in e))

    def test_prefixo_errado(self):
        e = self.checar("- **REF-01** R. — Manual 4.1.1, p. 36\n")
        self.assertTrue(any("prefixo" in x for x in e))

    def test_prefixo_certo_em_referencias(self):
        self.assertEqual(self.checar("- **REF-01** R. — Manual 4.1.1, p. 36\n", nome="referencias-direito.md"), [])

    def test_subbullet_exemplo_sem_origem(self):
        self.assertEqual(self.checar("- **CIT-01** R. — Manual 4.1.1, p. 36\n  - Ex.: (SILVA, 2020, p. 3)\n"), [])

    def test_marcadores_de_pendencia(self):
        for m in ["p. ?", "p. X", "TODO", "[conferir]"]:
            with self.subTest(m=m):
                self.assertTrue(self.checar(f"- **CIT-01** R {m}. — Manual 4.1.1, p. 36\n"))

    def test_manual_sem_item(self):
        self.assertEqual(self.checar("- **CIT-01** R. — Manual, p. 7\n"), [])
        self.assertTrue(self.checar("- **CIT-01** R. — Manual, p. 500\n"))

    def test_decisao_da_autora(self):
        self.assertTrue(self.checar("- **CIT-01** R. — Decisão da autora\n"))
        self.assertEqual(self.checar("- **CIT-01** R. — Manual 4.1.1, p. 36; Decisão da autora\n"), [])

    def test_nbr(self):
        self.assertEqual(self.checar("- **CIT-01** R. — NBR 6023:2020\n"), [])
        self.assertEqual(self.checar("- **CIT-01** R. — NBR geral\n"), [])

    def test_intervalo_com_meia_risca_e_hifen(self):
        self.assertEqual(self.checar("- **CIT-01** R. — Manual 4.1.2, p. 36–37\n"), [])
        self.assertEqual(self.checar("- **CIT-01** R. — Manual 4.1.2, p. 36-37\n"), [])
        self.assertTrue(self.checar("- **CIT-01** R. — Manual 4.1.2, p. 36–50\n"))

    def test_cabecalho_obrigatorio(self):
        e = self.checar("- **CIT-01** R. — Manual 4.1.1, p. 36\n", cab="## Secao\n\n")
        self.assertTrue(any("# " in x for x in e) and any("Fonte" in x for x in e))

    def test_travessao_no_meio_usa_ultimo(self):
        self.assertEqual(self.checar("- **CIT-01** A — B. — Manual 4.1.1, p. 36\n"), [])


class TestMain(Base):
    def test_main_codigos_de_saida(self):
        with tempfile.TemporaryDirectory() as d:
            ok = Path(d) / "citacoes.md"
            ok.write_text(CAB + "- **CIT-01** R. — Manual 4.1.1, p. 36\n", encoding="utf-8")
            self.assertEqual(cr.main([str(ok)]), 0)
            ruim = Path(d) / "tabelas-ilustracoes.md"
            ruim.write_text(CAB + "- **TAB-01** R. — Manual 4.1.1, p. 50\n", encoding="utf-8")
            self.assertEqual(cr.main([str(ruim)]), 1)
            self.assertEqual(cr.main([d]), 1)


if __name__ == "__main__":
    unittest.main()
