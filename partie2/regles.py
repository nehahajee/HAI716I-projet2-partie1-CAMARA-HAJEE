"""
Règles de mise à jour des agents pour le jeu du tee-shirt.
"""

from interface import RegleMiseAJour, ROUGE, BLEU


# --------------------------------------------------
# REGLES ETUDIEES EN COURS
# --------------------------------------------------

class RegleMajoriteSimple(RegleMiseAJour):
    """
    L'agent adopte la couleur qu'il a observée
    le plus souvent chez ses partenaires.
    """

    def choisir_couleur(self, memoire, couleur_actuelle, rng):
        nombre_rouge = 0
        nombre_bleu = 0

        for observation in memoire:
            if observation.couleur_partenaire == ROUGE:
                nombre_rouge += 1
            elif observation.couleur_partenaire == BLEU:
                nombre_bleu += 1

        if nombre_rouge > nombre_bleu:
            return ROUGE

        if nombre_bleu > nombre_rouge:
            return BLEU

        return couleur_actuelle


class RegleHCR(RegleMiseAJour):
    """
    Highest Cumulative Reward.

    L'agent choisit la couleur qui lui a rapporté
    le plus de gains depuis le début de la simulation.
    """

    def choisir_couleur(self, memoire, couleur_actuelle, rng):
        gains_rouge = 0
        gains_bleu = 0

        for observation in memoire:
            if observation.couleur_personnelle == ROUGE:
                gains_rouge += observation.gain

            elif observation.couleur_personnelle == BLEU:
                gains_bleu += observation.gain

        if gains_rouge > gains_bleu:
            return ROUGE

        if gains_bleu > gains_rouge:
            return BLEU

        return couleur_actuelle


# --------------------------------------------------
# REGLES SUPPLEMENTAIRES
# --------------------------------------------------

class RegleCopiePartenaire(RegleMiseAJour):
    """
    L'agent adopte la dernière couleur observée
    chez son partenaire.
    """

    def choisir_couleur(self, memoire, couleur_actuelle, rng):
        if not memoire:
            return couleur_actuelle

        derniere_observation = memoire[-1]

        return derniere_observation.couleur_partenaire


class RegleMajoriteRecente(RegleMiseAJour):
    """
    L'agent adopte la couleur observée le plus souvent
    au cours de ses trois dernières rencontres.
    """

    def choisir_couleur(self, memoire, couleur_actuelle, rng):
        observations_recentes = memoire[-3:]

        nombre_rouge = 0
        nombre_bleu = 0

        for observation in observations_recentes:
            if observation.couleur_partenaire == ROUGE:
                nombre_rouge += 1

            elif observation.couleur_partenaire == BLEU:
                nombre_bleu += 1

        if nombre_rouge > nombre_bleu:
            return ROUGE

        if nombre_bleu > nombre_rouge:
            return BLEU

        return couleur_actuelle
