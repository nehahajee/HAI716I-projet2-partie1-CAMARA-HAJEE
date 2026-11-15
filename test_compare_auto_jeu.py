from compare_auto_jeu import classement
from strategies import AllD, TitForTat, TitForTwoTats, population_cours


def test_mini_tournoi_sans_auto_jeu_diapo_68():
    """2 TFT + 1 ALL-D, 10 tours, 1 partie, sans auto-jeu : 48 / 48 / 46."""
    population = [TitForTat(), TitForTat(), AllD()]
    scores = sorted(score for _, score in classement(population, 1, 10, 0, auto_jeu=False))
    assert scores == [46, 48, 48]


def test_auto_jeu_ajoute_le_score_contre_une_copie():
    """TFT + ALL-D, 10 tours : sans auto-jeu 18 / 23 ; avec : +30 pour TFT, +20 pour ALL-D."""
    sans_auto_jeu = dict(classement([TitForTat(), AllD()], 1, 10, 0, auto_jeu=False))
    avec_auto_jeu = dict(classement([TitForTat(), AllD()], 1, 10, 0, auto_jeu=True))
    assert (sans_auto_jeu["TIT-FOR-TAT"], sans_auto_jeu["ALL-D"]) == (18, 23)
    assert (avec_auto_jeu["TIT-FOR-TAT"], avec_auto_jeu["ALL-D"]) == (48, 43)


def test_ex_aequo_classes_par_ordre_alphabetique():
    """TFT et TIT-FOR-TWO-TATS coopèrent toujours l'un avec l'autre : mêmes scores.
    Même placée en premier dans la population, TIT-FOR-TWO-TATS est classée après."""
    population = [TitForTwoTats(), TitForTat()]
    resultat = classement(population, 1, 10, 0, auto_jeu=False)
    assert resultat[0][1] == resultat[1][1]
    assert [nom for nom, _ in resultat] == ["TIT-FOR-TAT", "TIT-FOR-TWO-TATS"]


def test_classement_reproductible():
    premier_classement = classement(population_cours(), 3, 50, 5, auto_jeu=True)
    second_classement = classement(population_cours(), 3, 50, 5, auto_jeu=True)
    assert premier_classement == second_classement