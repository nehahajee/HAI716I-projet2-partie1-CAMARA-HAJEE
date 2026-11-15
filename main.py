import argparse
import csv
import random
from moteur import tournoi, classement, NB_PARTIES, NB_TOURS, GRAINE
from strategies import population_cours, population_etendue


def main():
    parser = argparse.ArgumentParser(description="Tournoi de dilemme du prisonnier itéré")
    parser.add_argument("--graine", type=int, default=GRAINE, help="graine aléatoire")
    parser.add_argument("--tours", type=int, default=NB_TOURS, help="nb de tours par partie")
    parser.add_argument("--parties", type=int, default=NB_PARTIES, help="nb de parties par match")
    parser.add_argument("--auto-play", action="store_true", help="Option de jouer contre soi même")
    parser.add_argument("--population", choices=["cours", "etendue"], default="cours",
                        help="cours : les 5 stratégies du cours, etendue : avec les stratégies ajoutées")
    parser.add_argument("--bruit", type=float, default=0.0,
                        help="probabilité d'inverser chaque coup (ex. 0.05), 0 = sans bruit")
    args = parser.parse_args()
    if not 0 <= args.bruit <= 1:
        parser.error("--bruit doit être compris entre 0 et 1")

    rng = random.Random(args.graine)
    population = population_etendue() if args.population == "etendue" else population_cours()
    scores, matchs = tournoi(population, args.parties, args.tours, rng, args.auto_play, bruit=args.bruit)
    resultat = classement(scores)

    print(f"Paramètres utilisés : population {args.population}, graine {args.graine}, {args.tours} tours, "
          f"{args.parties} parties, auto play {'oui' if args.auto_play else 'non'}, bruit {args.bruit}")
    nom_fichier = (f"classement{'_etendue' if args.population == 'etendue' else ''}_graine{args.graine}"
                   f"{'_autoplay' if args.auto_play else ''}{f'_bruit{args.bruit}' if args.bruit > 0 else ''}.csv")
    with open(nom_fichier, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rang", "strategie", "score"])
        for rang, (nom, score) in enumerate(resultat, start=1):
            print(f"{rang:>2}. {nom:<20}{score:>8}")
            writer.writerow([rang, nom, score])
    print(f"Classement exporté dans {nom_fichier}")


if __name__ == "__main__":
    main()
