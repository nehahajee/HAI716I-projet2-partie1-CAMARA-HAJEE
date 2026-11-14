class Strategie:
    """Classe mère de toutes les stratégies. Elle sert de modèle et n'est jamais utilisée
    directement dans un tournoi.

    Pour créer une stratégie :
    - hériter de Strategie ;
    - définir l'attribut nom (obligatoire, utilisé dans le classement) ;
    - redéfinir jouer (obligatoire) ;
    - redéfinir reset seulement si la stratégie a une mémoire interne (facultatif)."""
    nom: str

    def reset(self):
        """Appelée par le moteur au début de chaque partie, ne renvoie rien.
        Elle sert aux stratégies qui ont une mémoire interne (ex : TESTER, JOSS) : elle efface
        cette mémoire afin que la partie précédente ne fausse pas la suivante.
        Par défaut elle ne fait rien, les stratégies sans mémoire n'ont pas à la redéfinir."""
        pass

    def jouer(self, coups_personnels, coups_adverses, rng):
        """Appelée par le moteur à chaque tour pour obtenir le coup de la stratégie.

        Prend en entrée :
        - coups_personnels : liste des coups déjà joués par cette stratégie dans la partie ;
        - coups_adverses : liste des coups déjà joués par l'adversaire dans la partie ;
          chaque coup est la chaîne "C" ou "D", du plus ancien au plus récent
          (le dernier coup adverse est donc coups_adverses[-1]) ;
          au premier tour, les deux listes sont vides ;
          ces listes appartiennent au moteur, la stratégie ne doit pas les modifier ;
        - rng : générateur aléatoire (random.Random) fourni par le moteur, créé à partir
          de la graine. Une stratégie qui a besoin de hasard utilise uniquement rng,
          jamais le module random, sinon les résultats ne sont plus reproductibles.

        Renvoie en sortie : la chaîne "C" (coopérer) ou "D" (trahir), rien d'autre.

        Exemple : au 3e tour contre ALL-D, coups_adverses vaut ["D", "D"]."""
        raise NotImplementedError("Chaque stratégie doit implémenter son jeu")
