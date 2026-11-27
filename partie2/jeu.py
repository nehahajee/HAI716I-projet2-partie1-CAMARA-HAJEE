class Agent: 
    def __init__(self, couleur: str, regle) -> None:
        self.couleur: str = couleur
        self.memoire: list[tuple[str, str, int]] = []
        self.regle = regle

    def ajout_observation(self, obs): 
        self.memoire.append(obs)

    def mettre_a_jour(self, rng):
        self.couleur = self.regle(self.memoire, self.couleur, rng)