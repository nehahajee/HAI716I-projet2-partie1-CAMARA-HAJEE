"""
Tests des règles de mise à jour du jeu du tee-shirt
"""

import unittest

from interface import Observation, ROUGE, BLEU
from regles import (
    RegleMajoriteSimple,
    RegleHCR,
    RegleCopiePartenaire,
    RegleMajoriteRecente
)


class TestRegleMajoriteSimple(unittest.TestCase):

    def setUp(self):
        self.regle = RegleMajoriteSimple()

    def test_majorite_rouge(self):
        memoire = [
            Observation(ROUGE, ROUGE, 1),
            Observation(BLEU, ROUGE, 1),
            Observation(ROUGE, BLEU, 0)
        ]

        resultat = self.regle.choisir_couleur(memoire, BLEU, None)

        self.assertEqual(resultat, ROUGE)

    def test_egalite_conserve_couleur(self):
        memoire = [
            Observation(ROUGE, ROUGE, 1),
            Observation(BLEU, BLEU, 1)
        ]

        resultat = self.regle.choisir_couleur(memoire, BLEU, None)

        self.assertEqual(resultat, BLEU)

    def test_memoire_vide(self):
        resultat = self.regle.choisir_couleur([], ROUGE, None)

        self.assertEqual(resultat, ROUGE)


class TestRegleHCR(unittest.TestCase):

    def setUp(self):
        self.regle = RegleHCR()

    def test_choisit_couleur_plus_rentable(self):
        memoire = [
            Observation(ROUGE, ROUGE, 1),
            Observation(ROUGE, BLEU, 0),
            Observation(BLEU, BLEU, 1)
        ]

        resultat = self.regle.choisir_couleur(memoire, BLEU, None)

        self.assertEqual(resultat, ROUGE)

    def test_egalite_conserve_couleur(self):
        memoire = [
            Observation(ROUGE, ROUGE, 1),
            Observation(BLEU, BLEU, 1)
        ]

        resultat = self.regle.choisir_couleur(memoire, BLEU, None)

        self.assertEqual(resultat, BLEU)

    def test_memoire_vide(self):
        resultat = self.regle.choisir_couleur([], ROUGE, None)

        self.assertEqual(resultat, ROUGE)


class TestRegleCopiePartenaire(unittest.TestCase):

    def setUp(self):
        self.regle = RegleCopiePartenaire()

    def test_copie_derniere_couleur_observee(self):
        memoire = [
            Observation(ROUGE, ROUGE, 1),
            Observation(BLEU, ROUGE, 0),
            Observation(ROUGE, BLEU, 0)
        ]

        resultat = self.regle.choisir_couleur(memoire, ROUGE, None)

        self.assertEqual(resultat, BLEU)

    def test_memoire_vide(self):
        resultat = self.regle.choisir_couleur([], ROUGE, None)

        self.assertEqual(resultat, ROUGE)


class TestRegleMajoriteRecente(unittest.TestCase):

    def setUp(self):
        self.regle = RegleMajoriteRecente()

    def test_prend_en_compte_trois_dernieres_observations(self):
        memoire = [
            Observation(ROUGE, ROUGE, 1),
            Observation(ROUGE, ROUGE, 1),
            Observation(ROUGE, BLEU, 0),
            Observation(BLEU, BLEU, 1),
            Observation(ROUGE, BLEU, 0)
        ]

        resultat = self.regle.choisir_couleur(memoire, ROUGE, None)

        self.assertEqual(resultat, BLEU)

    def test_egalite_conserve_couleur(self):
        memoire = [
            Observation(ROUGE, ROUGE, 1),
            Observation(BLEU, BLEU, 1)
        ]

        resultat = self.regle.choisir_couleur(memoire, ROUGE, None)

        self.assertEqual(resultat, ROUGE)

    def test_memoire_vide(self):
        resultat = self.regle.choisir_couleur([], BLEU, None)

        self.assertEqual(resultat, BLEU)


if __name__ == "__main__":
    unittest.main()
