"""Étape 3 : tournoi évolutif (sélection sur plusieurs générations).

Principe (dynamique de réplication) :
  1. On calcule scores_moyens[i][j] = score moyen par partie de la stratégie i
     contre la stratégie j.
  2. À chaque génération, la « fitness » de i est son score moyen face à la
     population actuelle :
         fitness_i = somme sur j de (part_j * scores_moyens[i][j])
  3. La nouvelle part de i est : part_i * fitness_i / fitness_moyenne.
  Une stratégie qui score au-dessus de la moyenne gagne des parts, les autres en
  perdent. Les parts restent de somme 1. Une part à 0 reste à 0 (pas de mutation).

Choix de modélisation :
  - scores_moyens est calculée UNE fois (parties jouées avec la graine) puis
    réutilisée : le résultat est reproductible et ne dépend que de la graine.
  - Règle d'équipe : une stratégie ne joue pas contre elle-même, mais contre une
    COPIE (un autre joueur de même stratégie). La diagonale scores_moyens[i][i]
    est le score contre cette copie : dans une population, un joueur TFT
    rencontre d'autres joueurs TFT. Score = moyenne des deux « sièges » de la partie.
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


def matrice_scores(population, nb_parties, nb_tours, graine, matrice_gains):
    """scores_moyens[i][j] : score moyen par partie de la stratégie i contre la
    stratégie j. Pour i == j : score contre une copie (pas contre soi-même)."""
    rng = random.Random(graine)
    nb_strategies = len(population)
    scores_moyens = [[0.0] * nb_strategies for _ in range(nb_strategies)]
    for indice_strategie in range(nb_strategies):
        for indice_adversaire in range(indice_strategie, nb_strategies):
            total_strategie = 0
            total_adversaire = 0
            if indice_adversaire == indice_strategie:
                adversaire = copy.deepcopy(population[indice_strategie])
            else:
                adversaire = population[indice_adversaire]
            for _ in range(nb_parties):
                score_strategie, score_adversaire = jouer_partie(
                    population[indice_strategie], adversaire, nb_tours, rng, gains=matrice_gains)
                total_strategie += score_strategie
                total_adversaire += score_adversaire
            if indice_adversaire == indice_strategie:
                scores_moyens[indice_strategie][indice_strategie] = (
                    (total_strategie + total_adversaire) / (2 * nb_parties))
            else:
                scores_moyens[indice_strategie][indice_adversaire] = total_strategie / nb_parties
                scores_moyens[indice_adversaire][indice_strategie] = total_adversaire / nb_parties
    return scores_moyens


def evoluer(scores_moyens, parts_initiales, nb_generations):
    """Renvoie l'historique des parts : une liste par génération, génération 0 comprise."""
    if any(score < 0 for ligne_scores in scores_moyens for score in ligne_scores):
        raise ValueError("Les gains doivent être >= 0 pour la dynamique de réplication.")
    nb_strategies = len(scores_moyens)
    parts_population = list(parts_initiales)
    historique_parts = [parts_population[:]]
    for _ in range(nb_generations):
        fitness_par_strategie = [
            sum(scores_moyens[indice_strategie][indice_adversaire] * parts_population[indice_adversaire]
                for indice_adversaire in range(nb_strategies))
            for indice_strategie in range(nb_strategies)]
        fitness_moyenne = sum(parts_population[indice_strategie] * fitness_par_strategie[indice_strategie]
                              for indice_strategie in range(nb_strategies))
        if fitness_moyenne == 0:
            break
        parts_population = [
            parts_population[indice_strategie] * fitness_par_strategie[indice_strategie] / fitness_moyenne
            for indice_strategie in range(nb_strategies)]
        historique_parts.append(parts_population[:])
    return historique_parts


def exporter_csv(noms_strategies, historique_parts, chemin_fichier):
    with open(chemin_fichier, "w", newline="", encoding="utf-8") as fichier_csv:
        ecrivain_csv = csv.writer(fichier_csv)
        ecrivain_csv.writerow(["generation"] + noms_strategies)
        for numero_generation, parts_generation in enumerate(historique_parts):
            ecrivain_csv.writerow([numero_generation] + [f"{part:.6f}" for part in parts_generation])


def tracer(noms_strategies, historique_parts, chemin_fichier, titre=""):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(figsize=(8, 5))
    for indice_strategie, nom_strategie in enumerate(noms_strategies):
        parts_de_la_strategie = [parts_generation[indice_strategie] for parts_generation in historique_parts]
        axes.plot(parts_de_la_strategie, label=nom_strategie)
    axes.set_xlabel("génération")
    axes.set_ylabel("part de la population")
    axes.set_ylim(0, 1)
    axes.set_title(titre)
    axes.legend(fontsize=8)
    figure.tight_layout()
    figure.savefig(chemin_fichier, dpi=150)


def main():
    analyseur_arguments = argparse.ArgumentParser(description="Tournoi évolutif (dynamique de réplication)")
    analyseur_arguments.add_argument("--seed", type=int, default=42)
    analyseur_arguments.add_argument("--tours", type=int, default=200)
    analyseur_arguments.add_argument("--parties", type=int, default=5)
    analyseur_arguments.add_argument("--generations", type=int, default=100)
    analyseur_arguments.add_argument("--population", choices=["cours", "etendue"], default="cours")
    analyseur_arguments.add_argument("--gains", choices=sorted(MATRICES), default="dilemme")
    analyseur_arguments.add_argument("--csv")
    analyseur_arguments.add_argument("--png")
    arguments = analyseur_arguments.parse_args()

    if arguments.population == "cours":
        population = population_cours()
    else:
        population = population_etendue()
    noms_strategies = [strategie.nom for strategie in population]
    nb_strategies = len(population)
    scores_moyens = matrice_scores(population, arguments.parties, arguments.tours,
                                   arguments.seed, MATRICES[arguments.gains])
    historique_parts = evoluer(scores_moyens, [1 / nb_strategies] * nb_strategies, arguments.generations)

    print(f"population={arguments.population} gains={arguments.gains} seed={arguments.seed} "
          f"parties={arguments.parties} tours={arguments.tours} générations={arguments.generations}")
    print(f"{'stratégie':<20}{'génération 0':>14}{'finale':>12}")
    indices_tries = sorted(range(nb_strategies), key=lambda indice: -historique_parts[-1][indice])
    for indice_strategie in indices_tries:
        print(f"{noms_strategies[indice_strategie]:<20}"
              f"{historique_parts[0][indice_strategie]:>14.3f}"
              f"{historique_parts[-1][indice_strategie]:>12.3f}")
    if arguments.csv:
        exporter_csv(noms_strategies, historique_parts, arguments.csv)
    if arguments.png:
        tracer(noms_strategies, historique_parts, arguments.png,
               f"Sélection — gains={arguments.gains}, population={arguments.population}")


if __name__ == "__main__":
    main()