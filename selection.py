"""Étape 3 : tournoi évolutif (sélection sur plusieurs générations).

Principe (dynamique de réplication) :
  1. On calcule M[i][j] = score moyen par partie de la stratégie i contre j.
  2. Chaque génération, la « fitness » de i est son score moyen face à la
     population actuelle :   f_i = somme_j  part_j * M[i][j]
  3. La part de i devient    part_i * f_i / (fitness moyenne de la population).
  Une stratégie qui score au-dessus de la moyenne gagne des parts, les autres en
  perdent. Les parts restent de somme 1. Une part à 0 reste à 0 (pas de mutation).

Choix de modélisation :
  - M est calculée UNE fois (parties jouées avec la graine) puis réutilisée : le
    résultat est reproductible et ne dépend que de la graine.
  - Règle d'équipe : une stratégie ne joue pas contre elle-même, mais contre une
    COPIE (un autre joueur de même stratégie). La diagonale M[i][i] est le score
    contre cette copie : dans une population, un joueur TFT rencontre d'autres
    joueurs TFT. Score = moyenne des deux « sièges » de la partie.
  - Les gains doivent être >= 0 (sinon la fitness peut devenir négative).

Exemples :
  python selection.py --seed 42 --generations 100 --csv sel_cours.csv --png sel_cours.png
  python selection.py --seed 42 --population etendue --gains cerf --png sel_cerf.png
"""
import argparse
import copy
import csv
import random

from gains import MATRICES
from strategies import population_cours, population_etendue

from moteur import jouer_partie


def matrice_scores(population, parties, tours, seed, gains):
    """M[i][j] : score moyen par partie de i contre j (j == i : contre une copie, pas contre soi-même)."""
    rng = random.Random(seed)
    n = len(population)
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            total_i = total_j = 0
            adversaire = population[j] if j != i else copy.deepcopy(population[i])
            for _ in range(parties):
                si, sj = jouer_partie(population[i], adversaire, tours, rng, gains=gains)
                total_i += si
                total_j += sj
            if i == j:
                M[i][i] = (total_i + total_j) / (2 * parties)
            else:
                M[i][j] = total_i / parties
                M[j][i] = total_j / parties
    return M


def evoluer(M, parts, generations):
    """Renvoie l'historique : liste de listes de parts, génération 0 comprise."""
    if any(x < 0 for ligne in M for x in ligne):
        raise ValueError("Les gains doivent être >= 0 pour la dynamique de réplication.")
    n = len(M)
    parts = list(parts)
    historique = [parts[:]]
    for _ in range(generations):
        fitness = [sum(M[i][j] * parts[j] for j in range(n)) for i in range(n)]
        moyenne = sum(parts[i] * fitness[i] for i in range(n))
        if moyenne == 0:
            break
        parts = [parts[i] * fitness[i] / moyenne for i in range(n)]
        historique.append(parts[:])
    return historique


def exporter_csv(noms, historique, chemin):
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["generation"] + noms)
        for g, parts in enumerate(historique):
            w.writerow([g] + [f"{p:.6f}" for p in parts])


def tracer(noms, historique, chemin, titre=""):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    for k, nom in enumerate(noms):
        ax.plot([h[k] for h in historique], label=nom)
    ax.set_xlabel("génération")
    ax.set_ylabel("part de la population")
    ax.set_ylim(0, 1)
    ax.set_title(titre)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(chemin, dpi=150)


def main():
    p = argparse.ArgumentParser(description="Tournoi évolutif (dynamique de réplication)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--tours", type=int, default=200)
    p.add_argument("--parties", type=int, default=5)
    p.add_argument("--generations", type=int, default=100)
    p.add_argument("--population", choices=["cours", "etendue"], default="cours")
    p.add_argument("--gains", choices=sorted(MATRICES), default="dilemme")
    p.add_argument("--csv")
    p.add_argument("--png")
    a = p.parse_args()

    pop = population_cours() if a.population == "cours" else population_etendue()
    noms = [s.nom for s in pop]
    M = matrice_scores(pop, a.parties, a.tours, a.seed, MATRICES[a.gains])
    hist = evoluer(M, [1 / len(pop)] * len(pop), a.generations)

    print(f"population={a.population} gains={a.gains} seed={a.seed} "
          f"parties={a.parties} tours={a.tours} générations={a.generations}")
    print(f"{'stratégie':<20}{'génération 0':>14}{'finale':>12}")
    for k in sorted(range(len(pop)), key=lambda k: -hist[-1][k]):
        print(f"{noms[k]:<20}{hist[0][k]:>14.3f}{hist[-1][k]:>12.3f}")
    if a.csv:
        exporter_csv(noms, hist, a.csv)
    if a.png:
        tracer(noms, hist, a.png, f"Sélection — gains={a.gains}, population={a.population}")


if __name__ == "__main__":
    main()