import pytest

from gains import MATRICES
from selection import evoluer, matrice_scores
from strategies import AllD, TitForTat, population_cours


def test_les_parts_restent_de_somme_1():
    population = population_cours()
    scores_moyens = matrice_scores(population, 3, 50, 1, MATRICES["dilemme"])
    historique_parts = evoluer(scores_moyens, [1 / len(population)] * len(population), 30)
    for parts_generation in historique_parts:
        assert sum(parts_generation) == pytest.approx(1.0)
        assert all(part >= 0 for part in parts_generation)


def test_une_part_nulle_reste_nulle():
    scores_moyens = [[3, 0], [5, 2]]
    historique_parts = evoluer(scores_moyens, [1.0, 0.0], 10)
    assert all(parts_generation[1] == 0 for parts_generation in historique_parts)


def test_fitness_identique_population_inchangee():
    scores_moyens = [[2, 2], [2, 2]]
    historique_parts = evoluer(scores_moyens, [0.3, 0.7], 5)
    assert historique_parts[-1] == pytest.approx([0.3, 0.7])


def test_dominance_stricte_elimine_la_dominee():
    """Cas jouet : A rapporte toujours plus que B, quel que soit l'adversaire."""
    scores_moyens = [[5, 4], [3, 2]]
    historique_parts = evoluer(scores_moyens, [0.5, 0.5], 60)
    assert historique_parts[-1][0] > 0.99


def test_reproductible_avec_la_meme_graine():
    def lancer():
        population = population_cours()
        scores_moyens = matrice_scores(population, 3, 50, 7, MATRICES["dilemme"])
        return evoluer(scores_moyens, [0.2] * 5, 20)
    assert lancer() == lancer()


def test_gains_negatifs_refuses():
    with pytest.raises(ValueError):
        evoluer([[1, -1], [0, 1]], [0.5, 0.5], 1)


def test_matrice_scores_valeurs_connues():
    """TFT vs ALL-D sur 10 tours : 18 pour TFT, 23 pour ALL-D (diapo 67)."""
    population = [TitForTat(), AllD()]
    scores_moyens = matrice_scores(population, 1, 10, 0, MATRICES["dilemme"])
    assert scores_moyens[0][1] == 18
    assert scores_moyens[1][0] == 23
    assert scores_moyens[0][0] == 30          # TFT contre une copie : 3 x 10
    assert scores_moyens[1][1] == 20          # ALL-D contre une copie : 2 x 10


def test_matrice_dilemme_identique_a_celle_du_moteur():
    from moteur import gains as gains_moteur
    assert gains_moteur == MATRICES["dilemme"]