import random

import pytest

from strategies import (AllD, GenerousTitForTat, Gradual, Joss, Pavlov, Random,
                        Tester, TitForTat, TitForTwoTats)

from moteur import jouer_partie


def jouer_contre_script(strategie, script_adverse, graine=0):
    """Fait jouer `strategie` face à une suite de coups imposée.
    Renvoie les coups de la stratégie. Teste la règle sans le moteur."""
    rng = random.Random(graine)
    strategie.reset()
    coups_personnels, coups_adverses = [], []
    for coup_adverse in script_adverse:
        coup = strategie.jouer(list(coups_personnels), list(coups_adverses), rng)
        coups_personnels.append(coup)
        coups_adverses.append(coup_adverse)
    return coups_personnels


# ---------------------------------------------------------------- valeurs du cours

def test_tft_contre_alld_10_tours():
    """Diapo 67 : 18 contre 23."""
    assert jouer_partie(TitForTat(), AllD(), 10, random.Random(0)) == (18, 23)


def test_mini_tournoi_diapo_68():
    """Diapo 68 : 2 TFT + 1 ALL-D, 10 tours, SANS jeu contre soi-même.
    Totaux attendus : 48 / 48 / 46."""
    premier_tft, second_tft, all_d = TitForTat(), TitForTat(), AllD()
    rng = random.Random(0)
    score_premier_tft_contre_second, score_second_tft_contre_premier = jouer_partie(
        premier_tft, second_tft, 10, rng)                                    # 30 / 30
    score_premier_tft_contre_all_d, score_all_d_contre_premier_tft = jouer_partie(
        premier_tft, all_d, 10, rng)                                         # 18 / 23
    score_second_tft_contre_all_d, score_all_d_contre_second_tft = jouer_partie(
        second_tft, all_d, 10, rng)                                          # 18 / 23
    assert (score_premier_tft_contre_second, score_second_tft_contre_premier) == (30, 30)
    assert (score_premier_tft_contre_all_d, score_all_d_contre_premier_tft) == (18, 23)
    total_premier_tft = score_premier_tft_contre_second + score_premier_tft_contre_all_d
    total_second_tft = score_second_tft_contre_premier + score_second_tft_contre_all_d
    total_all_d = score_all_d_contre_premier_tft + score_all_d_contre_second_tft
    assert (total_premier_tft, total_second_tft, total_all_d) == (48, 48, 46)


# ---------------------------------------------------------------- coups attendus

def test_alld_joue_toujours_d():
    assert jouer_contre_script(AllD(), "CCDCD") == list("DDDDD")


def test_tft_rejoue_le_dernier_coup():
    assert jouer_contre_script(TitForTat(), "CDDCD") == list("CCDDC")


def test_tester_contre_cooperateur_pur():
    """Pas de riposte : D, puis le motif C, C, D répété."""
    assert jouer_contre_script(Tester(), "C" * 10) == list("DCCDCCDCCD")


def test_tester_contre_alld_passe_en_tft():
    """ALL-D joue D au tour 2 : riposte, donc Tester joue TFT (copie D)."""
    assert jouer_contre_script(Tester(), "D" * 6) == list("DCDDDD")


def test_tester_contre_tft_ecrit_en_miroir():
    rng = random.Random(0)
    strategie_tester, strategie_tit_for_tat = Tester(), TitForTat()
    coups_du_tester, coups_du_tit_for_tat = [], []
    for _ in range(6):
        coup_tester = strategie_tester.jouer(list(coups_du_tester), list(coups_du_tit_for_tat), rng)
        coup_tit_for_tat = strategie_tit_for_tat.jouer(list(coups_du_tit_for_tat), list(coups_du_tester), rng)
        coups_du_tester.append(coup_tester)
        coups_du_tit_for_tat.append(coup_tit_for_tat)
    assert coups_du_tester == list("DCDCDC")
    assert coups_du_tit_for_tat == list("CDCDCD")


def test_tit_for_two_tats():
    assert jouer_contre_script(TitForTwoTats(), "DDCDD") == list("CCDCC")


# ---------------------------------------------------------------- stratégies aléatoires

def test_random_environ_50_pourcent():
    coups = jouer_contre_script(Random(), "C" * 20000, graine=1)
    assert 0.48 < coups.count("D") / len(coups) < 0.52


def test_joss_defection_environ_10_pourcent():
    """Face à un adversaire toujours C, TFT jouerait toujours C :
    tous les D viennent de la déviation de JOSS."""
    coups = jouer_contre_script(Joss(), "C" * 20000, graine=2)
    assert 0.09 < coups.count("D") / len(coups) < 0.11


def test_joss_ne_devie_jamais_sur_un_d():
    """JOSS ne remplace que C par D : après un D adverse il joue D, toujours."""
    coups = jouer_contre_script(Joss(), "D" * 500, graine=3)
    assert coups[1:] == ["D"] * 499


def test_generous_tft_pardonne_environ_un_tiers():
    coups = jouer_contre_script(GenerousTitForTat(), "D" * 20001, graine=4)[1:]
    assert 0.32 < coups.count("C") / len(coups) < 0.35


def test_generous_tft_coopere_apres_c():
    assert jouer_contre_script(GenerousTitForTat(), "C" * 50) == ["C"] * 50


# ---------------------------------------------------------------- reproductibilité

@pytest.mark.parametrize("classe_strategie", [Random, Joss, GenerousTitForTat])
def test_graine_reproductible_et_rng_global_ignore(classe_strategie):
    """Même graine -> même partie, même si le `random` global est perturbé.
    Prouve que la stratégie tire bien dans le rng du moteur."""
    random.seed(111)
    resultat_premier_lancement = jouer_partie(classe_strategie(), TitForTat(), 200, random.Random(42))
    random.seed(999)
    resultat_second_lancement = jouer_partie(classe_strategie(), TitForTat(), 200, random.Random(42))
    assert resultat_premier_lancement == resultat_second_lancement


def test_deux_instances_de_tft_cooperent_a_chaque_tour():
    """TFT contre une copie : C, C à chaque tour, soit 3 x 200 = 600 points."""
    assert jouer_partie(TitForTat(), TitForTat(), 200, random.Random(0)) == (600, 600)


# ---------------------------------------------------------------- PAVLOV et GRADUAL (étape 2)

def test_pavlov_contre_alld_alterne():
    """(C, D) : mauvais, changer -> D ; (D, D) : mauvais, changer -> C."""
    assert jouer_contre_script(Pavlov(), "DDDDDD") == list("CDCDCD")


def test_pavlov_exploite_un_cooperateur_apres_une_trahison():
    """Après (C, D) PAVLOV passe à D ; (D, C) rapporte 5, donc PAVLOV garde D."""
    assert jouer_contre_script(Pavlov(), "CCDCCC") == list("CCCDDD")


def test_deux_pavlov_cooperent_a_chaque_tour():
    assert jouer_partie(Pavlov(), Pavlov(), 200, random.Random(0)) == (600, 600)


def test_gradual_contre_alld_punitions_croissantes():
    """Punitions de 1 puis 4 D, chacune suivie de deux C d'apaisement."""
    assert jouer_contre_script(Gradual(), "D" * 14) == list("CDCCDDDDCCDDDD")


def test_gradual_une_seule_trahison():
    """Une trahison : un D de punition, deux C d'apaisement, puis retour à C."""
    assert jouer_contre_script(Gradual(), "CDCCCCCC") == list("CCDCCCCC")


def test_gradual_reset_efface_la_punition_en_cours():
    gradual = Gradual()
    jouer_contre_script(gradual, "CDC")       # D au tour 2 -> punition en cours au tour 3
    assert gradual.plan != []
    gradual.reset()
    assert gradual.plan == []


@pytest.mark.parametrize("classe_strategie", [Pavlov, Gradual])
def test_pavlov_et_gradual_cooperent_avec_tft(classe_strategie):
    assert jouer_partie(classe_strategie(), TitForTat(), 200, random.Random(0)) == (600, 600)
