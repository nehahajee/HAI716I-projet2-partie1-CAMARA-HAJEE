import argparse
import csv
import random
from moteur import tournoi, classement, NB_PARTIES, NB_TOURS, GRAINE
from strategies import population_cours


def main():
    parser = argparse.ArgumentParser(description="Tournoi de dilemme du prisonnier itéré")
    parser.add_argument("--graine", type=int, default=GRAINE, help="graine aléatoire")
    parser.add_argument("--tours", type=int, default=NB_TOURS, help="nb de tours par partie")
    parser.add_argument("--parties", type=int, default=NB_PARTIES, help="nb de parties par match")
    parser.add_argument("--auto-play", action="store_true", help="Option de jouer contre soi même")
    args = parser.parse_args()

    rng = random.Random(args.graine)
    scores, matchs = tournoi(population_cours(), args.parties, args.tours, rng, args.auto_play)
    resultat = classement(scores)

    print(f"Paramètres utilisés : graine {args.graine}, {args.tours} tours, {args.parties} parties, "
          f"auto play {'oui' if args.auto_play else 'non'}")
    nom_fichier = f"classement_graine{args.graine}{'_autoplay' if args.auto_play else ''}.csv"
    with open(nom_fichier, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rang", "strategie", "score"])
        for rang, (nom, score) in enumerate(resultat, start=1):
            print(f"{rang:>2}. {nom:<20}{score:>8}")
            writer.writerow([rang, nom, score])
    print(f"Classement exporté dans {nom_fichier}")


if __name__ == "__main__":
    main()
