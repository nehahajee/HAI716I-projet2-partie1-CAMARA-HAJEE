"""
Contrat commun du jeu du tee-shirt (HAI716I, projet 2, partie 2).

Ce fichier définit les éléments partagés entre le moteur
de simulation et les règles de mise à jour.
"""

from random import Random


# --------------------------------------------------
# COULEURS
# --------------------------------------------------

ROUGE = "rouge"
BLEU = "bleu"


# --------------------------------------------------
# OBSERVATION
# --------------------------------------------------

class Observation:
    """
    Représente une rencontre entre deux agents.

    Attributs :
    - couleur_personnelle : couleur portée par l'agent.
    - couleur_partenaire : couleur portée par son partenaire.
    - gain : gain obtenu lors de la rencontre.
    """

    def __init__(self, couleur_personnelle, couleur_partenaire, gain):
        self.couleur_personnelle = couleur_personnelle
        self.couleur_partenaire = couleur_partenaire
        self.gain = gain


# --------------------------------------------------
# REGLE DE MISE A JOUR
# --------------------------------------------------

class RegleMiseAJour:
    """
    Classe mère de toutes les règles de mise à jour.

    Chaque règle doit hériter de cette classe et implémenter
    choisir_couleur().
    """

    def reset(self):
        """
        Réinitialise les éventuelles données internes de la règle.
        Par défaut, ne fait rien.
        """
        pass

    def choisir_couleur(self, memoire, couleur_actuelle, rng: Random):
        """
        Détermine la nouvelle couleur d'un agent.

        Paramètres :
        - memoire : liste des observations précédentes de l'agent.
        - couleur_actuelle : couleur actuelle de l'agent.
        - rng : générateur aléatoire fourni par le moteur.

        Retour :
        - la nouvelle couleur : ROUGE ou BLEU.

        Chaque règle doit implémenter cette méthode.
        """
        raise NotImplementedError(
            "Chaque règle doit implémenter choisir_couleur()."
        )


# --------------------------------------------------
# PARAMETRES DE SIMULATION
# --------------------------------------------------

class ParametresSimulation:
    """
    Regroupe les paramètres nécessaires à une simulation.

    Attributs :
    - nombre_agents : nombre d'agents participants.
    - max_tours : nombre maximal de tours.
    - graine : graine utilisée pour les tirages aléatoires.
    """

    def __init__(self, nombre_agents, max_tours, graine=None):
        self.nombre_agents = nombre_agents
        self.max_tours = max_tours
        self.graine = graine
