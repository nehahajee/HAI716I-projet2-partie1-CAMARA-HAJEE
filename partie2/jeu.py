from interface import Observation, RegleMiseAJour, ROUGE, BLEU


class Agent: 
    def __init__(self, couleur: str, regle: RegleMiseAJour) -> None:
        self.couleur: str = couleur
        self.memoire: list[Observation] = []
        self.regle = regle

    def ajout_observation(self, obs): 
        self.memoire.append(obs)

    def mettre_a_jour(self, rng):
        self.couleur = self.regle.choisir_couleur(self.memoire, self.couleur, rng)