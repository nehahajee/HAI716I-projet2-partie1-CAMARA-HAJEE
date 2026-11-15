import random

import pytest

from strategies import (AllD, GenerousTitForTat, Joss, Random, Tester,
                        TitForTat, TitForTwoTats)

from moteur import jouer_partie


def jouer_contre_script(strategie, script_adverse, seed=0):
    """Fait jouer `strategie` face à une suite de coups imposée.
    Renvoie les coups de la stratégie. Teste la règle sans le moteur."""
    rng = random.Random(seed)
    strategie.reset()
    mes, adv = [], []
    for coup_adv in script_adverse:
        mes.append(strategie.jouer(list(mes), list(adv), rng))
        adv.append(coup_adv)
    return mes


# ---------------------------------------------------------------- valeurs du cours

def test_tft_contre_alld_10_tours():
    """Diapo 67 : 18 contre 23."""
    assert jouer_partie(TitForTat(), AllD(), 10, random.Random(0)) == (18, 23)


def test_mini_tournoi_diapo_68():
    """Diapo 68 : 2 TFT + 1 ALL-D, 10 tours
    Totaux attendus : 48 / 48 / 46."""
    tft1, tft2, alld = TitForTat(), TitForTat(), AllD()
    rng = random.Random(0)
    a, b = jouer_partie(tft1, tft2, 10, rng)      # 30 / 30
    c, d = jouer_partie(tft1, alld, 10, rng)      # 18 / 23
    e, f = jouer_partie(tft2, alld, 10, rng)      # 18 / 23
    assert (a, b) == (30, 30)
    assert (c, d) == (18, 23)
    assert (a + c, b + e, d + f) == (48, 48, 46)


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
    t, tft = Tester(), TitForTat()
    mes, adv = [], []
    for _ in range(6):
        a = t.jouer(list(mes), list(adv), rng)
        b = tft.jouer(list(adv), list(mes), rng)
        mes.append(a)
        adv.append(b)
    assert mes == list("DCDCDC")
    assert adv == list("CDCDCD")


def test_tit_for_two_tats():
    assert jouer_contre_script(TitForTwoTats(), "DDCDD") == list("CCDCC")


# ---------------------------------------------------------------- stratégies aléatoires

def test_random_environ_50_pourcent():
    coups = jouer_contre_script(Random(), "C" * 20000, seed=1)
    assert 0.48 < coups.count("D") / len(coups) < 0.52


def test_joss_defection_environ_10_pourcent():
    """Face à un adversaire toujours C, TFT jouerait toujours C :
    tous les D viennent de la déviation de JOSS."""
    coups = jouer_contre_script(Joss(), "C" * 20000, seed=2)
    assert 0.09 < coups.count("D") / len(coups) < 0.11


def test_joss_ne_devie_jamais_sur_un_d():
    """JOSS ne remplace que C par D : après un D adverse il joue D, toujours."""
    coups = jouer_contre_script(Joss(), "D" * 500, seed=3)
    assert coups[1:] == ["D"] * 499


def test_generous_tft_pardonne_environ_un_tiers():
    coups = jouer_contre_script(GenerousTitForTat(), "D" * 20001, seed=4)[1:]
    assert 0.32 < coups.count("C") / len(coups) < 0.35


def test_generous_tft_coopere_apres_c():
    assert jouer_contre_script(GenerousTitForTat(), "C" * 50) == ["C"] * 50


# ---------------------------------------------------------------- reproductibilité

@pytest.mark.parametrize("classe", [Random, Joss, GenerousTitForTat])
def test_graine_reproductible_et_rng_global_ignore(classe):
    """Même graine -> même partie, même si le `random` global est perturbé.
    Prouve que la stratégie tire bien dans le rng du moteur."""
    random.seed(111)
    r1 = jouer_partie(classe(), TitForTat(), 200, random.Random(42))
    random.seed(999)
    r2 = jouer_partie(classe(), TitForTat(), 200, random.Random(42))
    assert r1 == r2


def test_instance_peut_jouer_contre_une_copie_d_elle_meme():
    """Les stratégies sont sans état : TFT contre TFT = coopération totale."""
    assert jouer_partie(TitForTat(), TitForTat(), 200, random.Random(0)) == (600, 600)