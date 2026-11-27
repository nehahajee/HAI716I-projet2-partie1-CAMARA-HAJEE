"""Matrices de gains (étape 3, modification « Autres gains »).

Format : {(coup_i, coup_j): (gain_i, gain_j)}, comme dans le moteur.
Notation : T = tentation (D,C), R = récompense (C,C), P = punition (D,D),
           S = gain du pigeon (C,D).
"""

# Dilemme du prisonnier du cours : T=5, R=3, P=2, S=0
#   ordre de i : D,C > C,C > D,D > C,D        (jeu n°14 de la table 6.1)
DILEMME = {
    ("C", "C"): (3, 3), ("C", "D"): (0, 5),
    ("D", "C"): (5, 0), ("D", "D"): (2, 2),
}

# Dilemme avec une punition plus sévère : T=5, R=3, P=1, S=0.
# Reste un dilemme (T > R > P > S, et 2R > T + S). Pour la comparer au cours.
DILEMME_P1 = {
    ("C", "C"): (3, 3), ("C", "D"): (0, 5),
    ("D", "C"): (5, 0), ("D", "D"): (1, 1),
}

# Chasse au cerf (diapo 76) : ordre de i : C,C > D,C > D,D > C,D   (jeu n°4)
#   deux équilibres de Nash : (C,C) et (D,D) ; tout repose sur la confiance.
CERF = {
    ("C", "C"): (4, 4), ("C", "D"): (0, 3),
    ("D", "C"): (3, 0), ("D", "D"): (1, 1),
}

# Poule mouillée (chicken) : ordre de i : D,C > C,C > C,D > D,D   (jeu n°13)
#   Les valeurs ne sont pas données dans le cours : elles sont choisies ici
#   pour respecter l'ordre. (D,D) est le pire résultat pour les deux.
POULE = {
    ("C", "C"): (3, 3), ("C", "D"): (1, 4),
    ("D", "C"): (4, 1), ("D", "D"): (0, 0),
}

MATRICES = {
    "dilemme": DILEMME,
    "dilemme_p1": DILEMME_P1,
    "cerf": CERF,
    "poule": POULE,
}
