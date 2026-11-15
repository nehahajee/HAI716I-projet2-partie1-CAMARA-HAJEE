import random

from moteur import jouer_partie, tournoi
from strategies import AllD, TitForTat, population_etendue


def test_bruit_total_inverse_tous_les_coups():
    """Avec bruit = 1, tous les D d'ALL-D deviennent des C : 3 x 200 = 600 points chacun."""
    assert jouer_partie(AllD(), AllD(), 200, random.Random(0), bruit=1.0) == (600, 600)


def test_bruit_nul_ne_change_pas_les_resultats():
    """bruit = 0 ne tire pas dans rng : mêmes scores que sans le paramètre."""
    sans = tournoi(population_etendue(), 5, 200, random.Random(42))
    avec = tournoi(population_etendue(), 5, 200, random.Random(42), bruit=0.0)
    assert sans == avec


def test_bruit_reproductible_avec_la_meme_graine():
    def lancer():
        return jouer_partie(TitForTat(), TitForTat(), 200, random.Random(42), bruit=0.05)
    assert lancer() == lancer()


def test_bruit_casse_la_cooperation_entre_deux_tft():
    """Sans bruit, deux TFT font 600 - 600 ; avec 5 % de bruit, l'écho fait baisser les scores."""
    score1, score2 = jouer_partie(TitForTat(), TitForTat(), 200, random.Random(42), bruit=0.05)
    assert score1 < 600 and score2 < 600
