from strategie import Strategie

C, D = "C", "D"

# --------------------------------------------------------------------------
# Les cinq stratégies du cours (diapositive 64)
# --------------------------------------------------------------------------

class AllD(Strategie):
    """Toujours D : la stratégie « rationnelle » de la récurrence à rebours."""
    nom = "ALL-D"

    def jouer(self, mes_coups, coups_adverses, rng):
        return D



# Random
class Random(Strategie):
    """C ou D au hasard (une chance sur deux). Sert de témoin."""
    nom = "RANDOM"

    def jouer(self, mes_coups, coups_adverses, rng):
        return C if rng.random() < 0.5 else D



# Tit-for-tat
class TitForTat(Strategie):
    """C au premier tour, puis rejoue le dernier coup de l'adversaire."""
    nom = "TIT-FOR-TAT"

    def jouer(self, mes_coups, coups_adverses, rng):
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

    def jouer(self, mes_coups, coups_adverses, rng):
        t = len(mes_coups)            # numéro du tour à jouer, en partant de 0
        if t == 0:
            return D
        if t >= 2 and coups_adverses[1] == D:      # l'adversaire a riposté
            return coups_adverses[-1]              # mode TIT-FOR-TAT
        # Motif C, C, D à partir du tour d'indice 1
        return D if (t - 1) % 3 == 2 else C




# JOSS

class Joss(Strategie):
    """TIT-FOR-TAT, mais remplace C par D avec probabilité 0,10."""
    nom = "JOSS"

    def __init__(self, p_defection=0.10):
        self.p = p_defection

    def jouer(self, mes_coups, coups_adverses, rng):
        coup = C if not coups_adverses else coups_adverses[-1]
        if coup == C and rng.random() < self.p:
            return D
        return coup




# --------------------------------------------------------------------------
# Stratégies absentes du cours (étape 2)
# --------------------------------------------------------------------------
# NEHA : LES 2 STRATEGIES  A AJOUTER

class GenerousTitForTat(Strategie):
    """TIT-FOR-TAT généreux (Nowak et Sigmund, 1992 ; diapositive 72).

    Après un C adverse : C. Après un D adverse : C avec probabilité g (elle
    « pardonne »), sinon D.

    Valeur de g : formule de Nowak et Sigmund,
        g = min( 1 - (T - R)/(R - S) , (R - P)/(T - P) )
    Avec T=5, R=3, P=2, S=0 : min(1 - 2/3, 1/3) = 1/3.
    C'est la plus grande générosité qui ne se laisse pas exploiter par ALL-D.
    """
    nom = "GENEROUS-TFT"

    def __init__(self, g=1 / 3):
        self.g = g

    def jouer(self, mes_coups, coups_adverses, rng):
        if not coups_adverses or coups_adverses[-1] == C:
            return C
        return C if rng.random() < self.g else D


    

class TitForTwoTats(Strategie):
    """Ne riposte que si l'adversaire a joué D deux fois de suite."""
    nom = "TIT-FOR-TWO-TATS"

    def jouer(self, mes_coups, coups_adverses, rng):
        if len(coups_adverses) >= 2 and coups_adverses[-1] == D and coups_adverses[-2] == D:
            return D
        return C



# --------------------------------------------------------------------------
# Populations
# --------------------------------------------------------------------------
def population_cours():
    """Population de base de l'étape 1 (nouvelles instances à chaque appel)."""
    return [AllD(), Random(), TitForTat(), Tester(), Joss()]



# A REMPLIR APRES AVOIR AJOUTE TES STRATEGIES
def population_etendue():
    """Étape 2. Neha ajoute sa stratégie (Grim Trigger / Pavlov...) ici."""
    return population_cours() + [GenerousTitForTat(), TitForTwoTats()]
