# HAI716I-projet2-partie1-CAMARA-HAJEE

Tournoi de dilemme du prisonnier itéré (HAI716I, projet 2 partie 1).
Binôme : Zéinab CAMARA et Neha HAJEE.

## Prérequis

- Python 3
- pytest (tests) et matplotlib (graphiques de la sélection)

Installation dans un environnement virtuel, à la racine du projet :

```
python3 -m venv .venv
source .venv/bin/activate
pip install pytest matplotlib
```

La commande `source .venv/bin/activate` est à relancer dans chaque nouveau terminal.

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

Comparaison des classements avec et sans auto play :

```
python3 compare_auto_jeu.py
```

## Tests

```
python3 -m pytest
```

## Étape 2 : nouvelles stratégies

Quatre stratégies absentes du cours sont ajoutées dans `strategies.py` : GENEROUS-TFT, TIT-FOR-TWO-TATS, PAVLOV et GRADUAL.
La population étendue regroupe les cinq stratégies du cours et ces quatre stratégies.

Tournoi avec la population étendue (même format qu'à l'étape 1) :

```
python3 main.py --population etendue
python3 main.py --population etendue --auto-play
```

| Option | Rôle | Valeur par défaut |
|---|---|---|
| `--population cours\|etendue` | stratégies du tournoi | `cours` |

Le classement est exporté dans `classement_etendue_graine42.csv` (et `classement_etendue_graine42_autoplay.csv` avec auto play).
Toutes les options de l'étape 1 (`--graine`, `--tours`, `--parties`) restent utilisables.

## Étape 3 : modifications du tournoi

### Bruit

Chaque coup est inversé (C devient D, D devient C) avec la probabilité donnée par `--bruit` :

```
python3 main.py --population etendue --bruit 0.05
```

| Option | Rôle | Valeur par défaut |
|---|---|---|
| `--bruit P` | probabilité d'inverser chaque coup, entre 0 et 1 | 0 (sans bruit) |

Le classement est exporté dans `classement_etendue_graine42_bruit0.05.csv`. Avec `--bruit 0`, les résultats sont exactement
ceux des étapes 1 et 2.

### Sélection et autres gains

Tournoi évolutif : le tournoi est rejoué sur plusieurs générations et la part de chaque stratégie dans la population suit
son score. L'option `--gains` change la matrice des gains (définies dans `gains.py`) :

| Valeur de `--gains` | Jeu |
|---|---|
| `dilemme` | dilemme du prisonnier de l'énoncé (par défaut) |
| `dilemme_p1` | dilemme avec une punition plus sévère (1/1 si les deux trahissent) |
| `cerf` | chasse au cerf |
| `poule` | poule mouillée |

```
python3 selection.py --seed 42 --generations 100 --csv sel_cours.csv --png sel_cours.png
python3 selection.py --seed 42 --population etendue --gains cerf --png sel_cerf.png
```

Autres options : `--tours`, `--parties`, `--population cours|etendue`, `--csv` (export des parts par génération),
`--png` (graphique).

## Organisation des fichiers

- `strategie.py` : classe mère `Strategie`, contrat entre le moteur et les stratégies
- `strategies.py` : les stratégies du cours et les nouvelles stratégies
- `moteur.py` : une partie, un match, le tournoi tous contre tous et le classement
- `main.py` : lancement du tournoi en ligne de commande
- `gains.py` : matrices de gains (dilemme et autres jeux 2 × 2)
- `selection.py` : tournoi évolutif (sélection)
- `compare_auto_jeu.py` : comparaison des classements avec et sans auto play
- `test_moteur.py`, `test_strategies.py`, `test_selection.py`, `test_compare_auto_jeu.py` : tests
- `journal_HAJEE`, `journal_CAMARA` : journaux de bord
