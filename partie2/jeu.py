from interface import Observation, RegleMiseAJour, ROUGE, BLEU
import random


class Agent:
    def __init__(self, couleur: str, regle: RegleMiseAJour) -> None:
        self.couleur: str = couleur
        self.memoire: list[Observation] = []
        self.regle = regle

    def ajout_observation(self, obs):
        self.memoire.append(obs)

    def mettre_a_jour(self, rng):
        self.couleur = self.regle.choisir_couleur(self.memoire, self.couleur, rng)


def creer_population(n, regle, rng):
    population = []
    for _ in range(n):
        couleur = rng.choice([ROUGE, BLEU])
        population.append(Agent(couleur, regle))
    return population


def former_paires(agents, rng):
    melange = list(agents)
    rng.shuffle(melange)
    couples = []
    for i in range(0, len(melange) - 1, 2):
        couples.append((melange[i], melange[i + 1]))
    return couples


def jouer_tour(agents, rng):
    paires = former_paires(agents, rng)
    for a, b in paires:
        if a.couleur == b.couleur:
            gain = 1
        else:
            gain = 0
        a.ajout_observation(Observation(a.couleur, b.couleur, gain))
        b.ajout_observation(Observation(b.couleur, a.couleur, gain))

    for a, b in paires:
        a.mettre_a_jour(rng)
        b.mettre_a_jour(rng)


def est_converge(agents):
    return len({a.couleur for a in agents}) == 1


def proportion_rouges(agents):
    return sum(1 for a in agents if a.couleur == ROUGE) / len(agents)


def jouer_partie(n, regle, max_tours, graine):
    rng = random.Random(graine)
    agents = creer_population(n, regle, rng)
    historique = [proportion_rouges(agents)]

    if est_converge(agents):
        return {"converge": True, "tours": 0, "couleur": agents[0].couleur, "historique": historique}

    for tour in range(1, max_tours + 1):
        jouer_tour(agents, rng)
        historique.append(proportion_rouges(agents))
        if est_converge(agents):
            return {"converge": True, "tours": tour, "couleur": agents[0].couleur, "historique": historique}

    return {"converge": False, "tours": max_tours, "couleur": None, "historique": historique}
