from strategie import Strategie

C, D = "C", "D"

# --------------------------------------------------------------------------
# Les cinq stratégies du cours (diapositive 64)
# --------------------------------------------------------------------------

class AllD(Strategie):
    """Toujours D : la stratégie « rationnelle » de la récurrence à rebours."""
    nom = "ALL-D"

    def jouer(self, coups_personnels, coups_adverses, rng):
        return D


# Random
class Random(Strategie):
    """C ou D au hasard (une chance sur deux). Sert de témoin."""
    nom = "RANDOM"

    def jouer(self, coups_personnels, coups_adverses, rng):
        return C if rng.random() < 0.5 else D


# Tit-for-tat
class TitForTat(Strategie):
    """C au premier tour, puis rejoue le dernier coup de l'adversaire."""
    nom = "TIT-FOR-TAT"

    def jouer(self, coups_personnels, coups_adverses, rng):
        if not coups_adverses:
            return C
        return coups_adverses[-1]


# TESTER

class Tester(Strategie):
    """D au premier tour, pour tester l'adversaire.

    - Si l'adversaire riposte (il joue D au tour 2), Tester joue TIT-FOR-TAT
      pour le reste de la partie.
    - Sinon, il répète le motif C, C, D à partir du tour 2 :
      tours 2, 3 = C ; tour 4 = D ; tours 5, 6 = C ; tour 7 = D ; etc.

    Remarque : au tour 2, Tester ne peut pas encore savoir si l'adversaire
    riposte (les coups sont simultanés). Il joue donc C ; la décision est prise
    au tour 3, quand il voit le coup de l'adversaire au tour 2.
    """
    nom = "TESTER"

    def jouer(self, coups_personnels, coups_adverses, rng):
        numero_tour = len(coups_personnels)   # numéro du tour à jouer, en partant de 0
        if numero_tour == 0:
            return D
        if numero_tour >= 2 and coups_adverses[1] == D:   # l'adversaire a riposté au tour 2
            return coups_adverses[-1]                     # mode TIT-FOR-TAT
        # Motif C, C, D à partir du tour d'indice 1
        position_dans_le_motif = (numero_tour - 1) % 3
        return D if position_dans_le_motif == 2 else C


# JOSS

class Joss(Strategie):
    """TIT-FOR-TAT, mais remplace C par D avec probabilité 0,10."""
    nom = "JOSS"

    def __init__(self, probabilite_defection=0.10):
        self.probabilite_defection = probabilite_defection

    def jouer(self, coups_personnels, coups_adverses, rng):
        coup_tit_for_tat = C if not coups_adverses else coups_adverses[-1]
        if coup_tit_for_tat == C and rng.random() < self.probabilite_defection:
            return D
        return coup_tit_for_tat


# --------------------------------------------------------------------------
# Stratégies absentes du cours (étape 2)
# --------------------------------------------------------------------------

class GenerousTitForTat(Strategie):
    """TIT-FOR-TAT généreux (Nowak et Sigmund, 1992 ; diapositive 72).

    Après un C adverse : C. Après un D adverse : C avec probabilité
    probabilite_pardon (elle « pardonne »), sinon D.

    Valeur de probabilite_pardon (notée g dans la formule) : Nowak et Sigmund,
        g = min( 1 - (T - R)/(R - S) , (R - P)/(T - P) )
    Avec T=5, R=3, P=2, S=0 : min(1 - 2/3, 1/3) = 1/3.
    C'est la plus grande générosité qui ne se laisse pas exploiter par ALL-D.
    """
    nom = "GENEROUS-TFT"

    def __init__(self, probabilite_pardon=1 / 3):
        self.probabilite_pardon = probabilite_pardon

    def jouer(self, coups_personnels, coups_adverses, rng):
        if not coups_adverses or coups_adverses[-1] == C:
            return C
        return C if rng.random() < self.probabilite_pardon else D



class TitForTwoTats(Strategie):
    """Ne riposte que si l'adversaire a joué D deux fois de suite."""
    nom = "TIT-FOR-TWO-TATS"

    def jouer(self, coups_personnels, coups_adverses, rng):
        if len(coups_adverses) >= 2 and coups_adverses[-1] == D and coups_adverses[-2] == D:
            return D
        return C


# --------------------------------------------------------------------------
# Populations
# --------------------------------------------------------------------------
def population_cours():
    """Population de base de l'étape 1 (nouvelles instances à chaque appel)."""
    return [AllD(), Random(), TitForTat(), Tester(), Joss()]


def population_etendue():
    """Étape 2 : population du cours + les stratégies ajoutées.
    Neha y ajoutera sa stratégie (Grim Trigger, Pavlov...)."""
    return population_cours() + [GenerousTitForTat(), TitForTwoTats()]