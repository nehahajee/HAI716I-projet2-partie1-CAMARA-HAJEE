import itertools
import copy

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

def jouer_match(strat1, strat2, nb_parties, nb_tours, rng): 
    score1 = 0 
    score2 = 0
    for _ in range (nb_parties): 
        points1, points2 = jouer_partie(strat1, strat2, nb_tours, rng)
        score1 += points1
        score2 += points2
    return score1, score2

def tournoi(strategies, nb_parties, nb_tours, rng, auto_play=False):
    scores = {}
    for strategie in strategies: 
        scores[strategie.nom] = 0
    matchs = {}
    if auto_play:
        paires = itertools.combinations_with_replacement(strategies, 2)
    else:
        paires = itertools.combinations(strategies, 2)
    for strat1, strat2 in paires:
        meme = strat1 is strat2
        if meme:
            strat2 = copy.deepcopy(strat1)
        score1, score2 = jouer_match(strat1, strat2, nb_parties, nb_tours, rng)
        matchs[(strat1.nom, strat2.nom)] = (score1, score2)
        scores[strat1.nom] += score1
        if not meme:
            scores[strat2.nom] += score2
    return scores, matchs

def classement(scores): 
    return sorted(scores.items(), key=lambda c: (-c[1], c[0]))