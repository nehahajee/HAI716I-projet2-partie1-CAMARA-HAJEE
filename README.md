# HAI716I-projet2-partie1-CAMARA-HAJEE

Tournoi de dilemme du prisonnier itéré (HAI716I, projet 2 partie 1).
Binôme : Zéinab CAMARA et Neha HAJEE.

## Prérequis

- Python 3
- pytest, pour lancer les tests :

```
pip install pytest
```

## Étape 1 : tournoi de base

Lance le tournoi des cinq stratégies du cours (ALL-D, RANDOM, TIT-FOR-TAT, TESTER, JOSS) au format d'Axelrod :
chaque stratégie affronte chaque autre sur 5 parties de 200 tours, avec la graine 42.

```
python3 main.py
```

Même tournoi, mais chaque stratégie joue aussi contre sa propre copie (comme dans le tournoi d'Axelrod de 1980) :

```
python3 main.py --auto-play
```

### Options

| Option | Rôle | Valeur par défaut |
|---|---|---|
| `--graine N` | graine aléatoire | 42 |
| `--tours N` | nombre de tours par partie | 200 |
| `--parties N` | nombre de parties par match | 5 |
| `--auto-play` | une stratégie joue aussi contre sa copie | désactivé |

Exemple : `python3 main.py --graine 7 --tours 100`

`python3 main.py --help` affiche la liste des options.

### Résultats

Le classement s'affiche dans le terminal et est exporté dans un fichier CSV (`rang,strategie,score`) :

- `classement_graine42.csv` sans auto play ;
- `classement_graine42_autoplay.csv` avec auto play.

Avec la même graine, deux lancements donnent exactement le même classement.

## Tests

```
python3 -m pytest
```

## Étape 2 : nouvelles stratégies

À compléter.

## Étape 3 : modifications du tournoi

À compléter.

## Organisation des fichiers

- `strategie.py` : classe mère `Strategie`, contrat entre le moteur et les stratégies
- `strategies.py` : les stratégies du cours et les nouvelles stratégies
- `moteur.py` : une partie, un match, le tournoi tous contre tous et le classement
- `main.py` : lancement du tournoi en ligne de commande
- `test_strategies.py` : tests des stratégies
- `journal_HAJEE`, `journal_CAMARA` : journaux de bord
