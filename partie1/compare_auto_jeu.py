"""Compare le classement du tournoi avec et sans auto-jeu.

auto_jeu=False : chaque stratégie affronte les AUTRES joueurs (règle d'équipe).
auto_jeu=True  : elle affronte aussi une copie d'elle-même (format Axelrod 1980) ;
                 le score de cette partie compte une fois (celui d'un « siège »).

                  

Exemple : python compare_auto_jeu.py --seed 42 --population etendue
"""
import argparse
import copy
import random

from strategies import population_cours, population_etendue

from moteur import jouer_partie


def classement(population, nb_parties, nb_tours, graine, auto_jeu):
    """Renvoie [(nom, score_total)] trié par score décroissant, puis par nom."""
    rng = random.Random(graine)
    scores_totaux = [0] * len(population)
    for indice_strategie in range(len(population)):
        for indice_adversaire in range(indice_strategie, len(population)):
            joue_contre_une_copie = indice_strategie == indice_adversaire
            if joue_contre_une_copie and not auto_jeu:
                continue
            if joue_contre_une_copie:
                adversaire = copy.deepcopy(population[indice_strategie])
            else:
                adversaire = population[indice_adversaire]
            for _ in range(nb_parties):
                score_strategie, score_adversaire = jouer_partie(
                    population[indice_strategie], adversaire, nb_tours, rng)
                scores_totaux[indice_strategie] += score_strategie
                if not joue_contre_une_copie:
                    scores_totaux[indice_adversaire] += score_adversaire
    noms_et_scores = [(population[indice].nom, scores_totaux[indice]) for indice in range(len(population))]
    return sorted(noms_et_scores, key=lambda nom_et_score: (-nom_et_score[1], nom_et_score[0]))


def main():
    analyseur_arguments = argparse.ArgumentParser(description="Classement avec / sans auto-jeu")
    analyseur_arguments.add_argument("--seed", type=int, default=42)
    analyseur_arguments.add_argument("--tours", type=int, default=200)
    analyseur_arguments.add_argument("--parties", type=int, default=5)
    analyseur_arguments.add_argument("--population", choices=["cours", "etendue"], default="cours")
    arguments = analyseur_arguments.parse_args()
    if arguments.population == "cours":
        creer_population = population_cours
    else:
        creer_population = population_etendue

    classement_sans_auto_jeu = classement(creer_population(), arguments.parties, arguments.tours,
                                          arguments.seed, auto_jeu=False)
    classement_avec_auto_jeu = classement(creer_population(), arguments.parties, arguments.tours,
                                          arguments.seed, auto_jeu=True)
    rang_sans = {nom: rang for rang, (nom, _) in enumerate(classement_sans_auto_jeu, 1)}
    rang_avec = {nom: rang for rang, (nom, _) in enumerate(classement_avec_auto_jeu, 1)}
    score_sans = dict(classement_sans_auto_jeu)
    score_avec = dict(classement_avec_auto_jeu)

    print(f"population={arguments.population} seed={arguments.seed} "
          f"parties={arguments.parties} tours={arguments.tours}")
    print(f"{'stratégie':<20}{'sans: rang':>11}{'score':>8}{'avec: rang':>12}{'score':>8}")
    for nom, _ in classement_sans_auto_jeu:
        print(f"{nom:<20}{rang_sans[nom]:>11}{score_sans[nom]:>8}"
              f"{rang_avec[nom]:>12}{score_avec[nom]:>8}")


if __name__ == "__main__":
    main()