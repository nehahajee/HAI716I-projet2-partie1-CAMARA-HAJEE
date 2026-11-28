import random
import unittest
from interface import RegleMiseAJour, Observation, ROUGE, BLEU
from jeu import Agent, creer_population, former_paires, jouer_tour, est_converge, proportion_rouges, jouer_partie


class CopierPartenaire(RegleMiseAJour):
    def choisir_couleur(self, memoire, couleur_actuelle, rng):
        if memoire:
            return memoire[-1].couleur_partenaire
        return couleur_actuelle


class TestMoteur(unittest.TestCase):
    def test_taille_population(self):
        agents = creer_population(10, CopierPartenaire(), random.Random(1))
        self.assertEqual(len(agents), 10)
        for a in agents:
            self.assertIn(a.couleur, [ROUGE, BLEU])
            self.assertEqual(a.memoire, [])

    def test_memoires_independantes(self):
        agents = creer_population(3, CopierPartenaire(), random.Random(1))
        agents[0].ajout_observation(Observation(ROUGE, BLEU, 0))
        self.assertEqual(len(agents[0].memoire), 1)
        self.assertEqual(len(agents[1].memoire), 0)
        self.assertEqual(len(agents[2].memoire), 0)

    def test_paires_n_pair(self):
        agents = creer_population(10, CopierPartenaire(), random.Random(1))
        paires = former_paires(agents, random.Random(1))
        self.assertEqual(len(paires), 5)
        dans_paires = [x for p in paires for x in p]
        self.assertEqual(len(set(dans_paires)), 10)

    def test_paires_n_impair(self):
        agents = creer_population(11, CopierPartenaire(), random.Random(1))
        paires = former_paires(agents, random.Random(1))
        self.assertEqual(len(paires), 5)
        dans_paires = [x for p in paires for x in p]
        self.assertEqual(len(set(dans_paires)), 10)

    def test_gain_meme_couleur(self):
        a = Agent(ROUGE, CopierPartenaire())
        b = Agent(ROUGE, CopierPartenaire())
        jouer_tour([a, b], random.Random(1))
        self.assertEqual(a.memoire[-1].gain, 1)
        self.assertEqual(b.memoire[-1].gain, 1)
        self.assertEqual(a.memoire[-1].couleur_partenaire, ROUGE)

    def test_gain_couleurs_differentes(self):
        a = Agent(ROUGE, CopierPartenaire())
        b = Agent(BLEU, CopierPartenaire())
        jouer_tour([a, b], random.Random(1))
        self.assertEqual(a.memoire[-1].gain, 0)
        self.assertEqual(b.memoire[-1].gain, 0)
        self.assertEqual(a.memoire[-1].couleur_personnelle, ROUGE)
        self.assertEqual(a.memoire[-1].couleur_partenaire, BLEU)

    def test_mise_a_jour_simultanee(self):
        # En simultané, chacun copie la couleur que l'autre avait avant le tour : ils échangent.
        # En séquentiel, les deux finiraient avec la même couleur.
        a = Agent(ROUGE, CopierPartenaire())
        b = Agent(BLEU, CopierPartenaire())
        jouer_tour([a, b], random.Random(1))
        self.assertEqual(a.couleur, BLEU)
        self.assertEqual(b.couleur, ROUGE)

    def test_agent_seul_ne_joue_pas(self):
        agents = [Agent(ROUGE, CopierPartenaire()) for _ in range(3)]
        jouer_tour(agents, random.Random(1))
        tailles = sorted(len(a.memoire) for a in agents)
        self.assertEqual(tailles, [0, 1, 1])

    def test_est_converge(self):
        tous_rouges = [Agent(ROUGE, CopierPartenaire()) for _ in range(3)]
        melange = [Agent(ROUGE, CopierPartenaire()), Agent(ROUGE, CopierPartenaire()), Agent(BLEU, CopierPartenaire())]
        self.assertTrue(est_converge(tous_rouges))
        self.assertFalse(est_converge(melange))

    def test_proportion_rouges(self):
        agents = [Agent(ROUGE, CopierPartenaire()) for _ in range(3)] + [Agent(BLEU, CopierPartenaire())]
        self.assertAlmostEqual(proportion_rouges(agents), 0.75)

    def test_reproductibilite(self):
        r1 = jouer_partie(20, CopierPartenaire(), 50, 42)
        r2 = jouer_partie(20, CopierPartenaire(), 50, 42)
        self.assertEqual(r1, r2)

    def test_deja_converge(self):
        r = jouer_partie(1, CopierPartenaire(), 50, 1)
        self.assertTrue(r["converge"])
        self.assertEqual(r["tours"], 0)
        self.assertEqual(r["historique"], [r["historique"][0]])

    def test_historique_longueur(self):
        r = jouer_partie(20, CopierPartenaire(), 50, 42)
        self.assertEqual(len(r["historique"]), r["tours"] + 1)


if __name__ == "__main__":
    unittest.main()
