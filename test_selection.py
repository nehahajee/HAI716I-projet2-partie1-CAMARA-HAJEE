import random

import pytest

from gains import MATRICES
from selection import evoluer, matrice_scores
from strategies import AllD, TitForTat, population_cours


def test_les_parts_restent_de_somme_1():
    pop = population_cours()
    M = matrice_scores(pop, 3, 50, 1, MATRICES["dilemme"])
    hist = evoluer(M, [1 / len(pop)] * len(pop), 30)
    for parts in hist:
        assert sum(parts) == pytest.approx(1.0)
        assert all(p >= 0 for p in parts)


def test_une_part_nulle_reste_nulle():
    M = [[3, 0], [5, 2]]
    hist = evoluer(M, [1.0, 0.0], 10)
    assert all(h[1] == 0 for h in hist)


def test_fitness_identique_population_inchangee():
    M = [[2, 2], [2, 2]]
    hist = evoluer(M, [0.3, 0.7], 5)
    assert hist[-1] == pytest.approx([0.3, 0.7])


def test_dominance_stricte_elimine_la_dominee():
    """Cas jouet : A rapporte toujours plus que B, quel que soit l'adversaire."""
    M = [[5, 4], [3, 2]]
    hist = evoluer(M, [0.5, 0.5], 60)
    assert hist[-1][0] > 0.99


def test_reproductible_avec_la_meme_graine():
    def lancer():
        pop = population_cours()
        M = matrice_scores(pop, 3, 50, 7, MATRICES["dilemme"])
        return evoluer(M, [0.2] * 5, 20)
    assert lancer() == lancer()


def test_gains_negatifs_refuses():
    with pytest.raises(ValueError):
        evoluer([[1, -1], [0, 1]], [0.5, 0.5], 1)


def test_matrice_scores_valeurs_connues():
    """TFT vs ALL-D sur 10 tours : 18 pour TFT, 23 pour ALL-D (diapo 67)."""
    pop = [TitForTat(), AllD()]
    M = matrice_scores(pop, 1, 10, 0, MATRICES["dilemme"])
    assert M[0][1] == 18
    assert M[1][0] == 23
    assert M[0][0] == 30          # TFT contre elle-même : 3 x 10
    assert M[1][1] == 20          # ALL-D contre elle-même : 2 x 10



def test_matrice_dilemme_identique_a_celle_du_moteur():
    from moteur import gains as gains_moteur
    assert gains_moteur == MATRICES["dilemme"]