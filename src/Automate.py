import sys
from typing import Dict, List, Tuple

class Automaton:
    """ 
    Automate cellulaire : stocke les règles de transition et l'état par défaut.
    transitions : dictionnaire {(gauche, centre, droite): nouvel_etat}
    alphabet : liste des états possibles (peut être None dans le cas de la simulation d'une Machine de Turing)
    default_state : état utilisé pour les bords
    """
    def __init__(self, transitions: Dict[tuple, str], alphabet: List[str]= None, default_state="-1"):
        self.transitions = transitions
        self.default_state = default_state
        self.alphabet = alphabet

    def transition(self, left, center, right):
        """
        Retourne le nouvel état selon la règle (left, center, right).
        Si la règle n'existe pas, retourne l'état du centre.
        """
        return self.transitions.get((left, center, right), center)
    
class ConfigurationAutomaton:
    """
    Représente la configuration courante d'un automate cellulaire.
    - states : liste des états des cellules
    - automaton : instance de Automaton contenant les règles
    """
    def __init__(self, states: List[str], automaton: Automaton):
        default = automaton.default_state
        # Ajoute les bords si besoin
        if states[0] != default:
            states = [default] + states
        if states[-1] != default:
            states = states + [default]
        self.states = states
        self.automaton = automaton

    def __str__(self):
        """ Affiche la configuration courante sous forme de chaîne d'états. """
        return " ".join(str(s) for s in self.states)

    def next_step(self) -> Tuple[List[str], bool, List[Tuple[str, str, str]]]:
        """
        Calcule la configuration suivante.
        Retourne :
        - la nouvelle liste d'états,
        - un booléen indiquant si la configuration a changé,
        - la liste des transitions utilisées.
        """
        states = self.states
        automaton = self.automaton
        default = automaton.default_state

        states = [default] + states + [default]

        new = []
        used_transitions = []
        changed = False

        for i in range(len(states)):
            # Vérifier si la cellule est dans l'alphabet
            if automaton.alphabet is not None:
                if states[i] not in automaton.alphabet:
                    raise ValueError(f"L'état {states[i]} n'est pas dans l'alphabet {automaton.alphabet}")

            # Récupère les états (gauche, centre, droite)
            left = states[i - 1] if i - 1 >= 0 else default
            center = states[i]
            right = states[i + 1] if i + 1 < len(states) else default

            # Applique la règle de transition
            new_state = automaton.transition(left, center, right)
            new.append(new_state)

            # Vérifie si la cellule a changé d'état
            if new_state != center:
                changed = True

            # Enregistre la transition utilisée si elle existe
            if (left, center, right) in automaton.transitions:
                used_transitions.append((left, center, right))

        # On garde au maximum un seul 'default' à chaque bord
        while len(new) > 2 and new[0] == default and new[1] == default:
            new.pop(0)
        while len(new) > 2 and new[-1] == default and new[-2] == default:
            new.pop()

        self.states = new
        return new, changed, used_transitions

    def simulate_automaton(self, max_steps: int = 1000,
                       stop_on_transition: Tuple[str, str, str] = None,
                       stop_on_stable: bool = False) -> None:
        """
        Simule l'automate cellulaire pendant max_steps étapes.
        - stop_on_transition : arrête si une transition spécifique est utilisée.
        - stop_on_stable : arrête si la configuration devient stable.
        """
        for step in range(max_steps):
            if step == 0:
                print("Configuration initiale :")
            else:    
                print(f"Étape {step}:")

            print(self)

            _, changed, used_transitions = self.next_step()

            if stop_on_transition and stop_on_transition in used_transitions:
                print(f"Arrêt : transition {stop_on_transition} utilisée à l'étape {step}")
                break

            if stop_on_stable and not changed:
                print(f"Arrêt : configuration stable atteinte à l'étape {step}")
                break
        else:
            print("Arrêt : nombre maximal d'étapes atteint")

def read_automaton(file: str) -> Automaton:
    """
    Lit un fichier de transitions et construit un Automaton.
    Format attendu par ligne : "gauche,centre,droite: nouvel_etat"
    """
    transitions = {}
    with open(file, 'r') as f:
        for line in f:
            if ":" in line:
                left, new_state = line.strip().split(":")
                l, c, r = map(str, left.strip().split(","))
                transitions[(l, c, r)] = str(new_state.strip())
    alphabet = list(set([l for l, c, r in transitions.keys()] + [c for l, c, r in transitions.keys()] + [r for l, c, r in transitions.keys()]))
    return Automaton(transitions, alphabet)

def main(file: str, step: int = None, transition: Tuple[str, str, str] = None,
         stable: bool = False, config_init: List[str] = None) -> None:
    """
    Exemple d'utilisation: lit un automate, initialise une configuration,
    puis lance la simulation.
    """
    # Automate cellulaire
    config_init = ["1", "0", "0", "0", "0", "0", "0"] if config_init is None else config_init
    automaton = read_automaton(file)
    config = ConfigurationAutomaton(config_init, automaton)
    print("Simulation :")
    config.simulate_automaton(step, transition, stable)


if __name__ == "__main__":
    fichier = sys.argv[1]
    print(f"Lecture de l'automate cellulaire à partir de {fichier}")

    step = sys.argv[2] if len(sys.argv) > 2 else None

    transition = sys.argv[3] if len(sys.argv) > 3 else None
    if transition:
        transition = tuple(transition.split(","))

    stable = sys.argv[4] if len(sys.argv) > 4 else None
    stable = False if stable == "0" else True

    config_init = sys.argv[5] if len(sys.argv) > 5 else None
    config_init = [str(c) for c in config_init]
    
    main(fichier, int(step), transition, stable, config_init)