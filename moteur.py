gains = {("C", "C"): (3, 3),
    ("C","D"): (0, 5),
    ("D", "C"): (5, 0),
    ("D", "D"): (2, 2)}

NB_PARTIES = 5
NB_TOURS = 200
GRAINE = 42 

def jouer_partie(strat1, strat2, nb_tours, rng): 
    strat1.reset()
    strat2.reset()
    historique_strat1 = []
    historique_strat2 = []
    score1 = 0
    score2 = 0
    for _ in range (nb_tours): 
        coup1 = strat1.jouer(list(historique_strat1), list(historique_strat2), rng)
        coup2 = strat2.jouer(list(historique_strat2), list(historique_strat1), rng)
        if coup1 not in ("C", "D"):
            raise ValueError(f"[Erreur]: le coup {coup1} de la stratégie {strat1.nom} n'est pas valide (attendu C ou D).")
        if coup2 not in ("C", "D"):
            raise ValueError(f"[Erreur]: le coup {coup2} de la stratégie {strat2.nom} n'est pas valide (attendu C ou D).")
        historique_strat1.append(coup1)
        historique_strat2.append(coup2)
        gain1, gain2 = gains[(coup1, coup2)]
        score1 += gain1
        score2 += gain2
    return score1, score2