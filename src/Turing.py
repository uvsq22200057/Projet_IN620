from typing import Dict, List, Tuple

class ConfigurationTuring:
    """
    Représente la configuration courante d'une machine de Turing :
    - tape : le ruban (liste de symboles)
    - head : position de la tête de lecture/écriture
    - state : état courant de la machine
    """
    def __init__(self, tape: List[str], head: int, state: str):
        self.tape = tape
        self.head = head
        self.state = state

    def __str__(self):
        # Affiche le ruban, la position de la tête et l'état courant
        tape_str = ''.join(self.tape)
        pointer = ' ' * self.head + '^'
        return f"Tape: {tape_str}\n       {pointer}\nState: {self.state}"


class TuringMachine:
    """
    Implémente une machine de Turing :
    - transitions : dictionnaire {(état, symbole): (nouvel état, nouveau symbole, déplacement)}
    - initial_state : état initial
    - accept_states : ensemble des états d'acceptation
    - default : symbole par défaut pour les cases non initialisées du ruban
    """
    def __init__(self, transitions: Dict[Tuple[str, str], Tuple[str, str, str]],
                 initial_state: str, accept_states: set, default_symbol: str = "-"):
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.default = default_symbol

    def step(self, config: ConfigurationTuring) -> ConfigurationTuring:
        """
        Effectue une transition de la machine de Turing :
        - Lit le symbole sous la tête
        - Applique la règle de transition (si elle existe)
        - Écrit le nouveau symbole
        - Déplace la tête (gauche/droite)
        - Met à jour l'état courant
        Retourne la nouvelle configuration.
        """
        symbol = config.tape[config.head] if 0 <= config.head < len(config.tape) else self.default

        if (config.state, symbol) not in self.transitions:
            config.state = "REJECT"
            return config

        new_state, new_symbol, move = self.transitions[(config.state, symbol)]

        # Ecrire le nouveau symbole sur le ruban
        if 0 <= config.head < len(config.tape):
            config.tape[config.head] = new_symbol
        else:
            if config.head < 0:
                config.tape.insert(0, new_symbol)
                config.head = 0
            else:
                config.tape.append(new_symbol)

        # Déplacer la tête de lecture
        if move == "R":
            config.head += 1
        elif move == "L":
            config.head -= 1

        # Gérer les débordements du ruban
        if config.head < 0:
            config.tape.insert(0, self.default)
            config.head = 0
        elif config.head >= len(config.tape):
            config.tape.append(self.default)

        config.state = new_state

        return config

    def is_accepting(self, config: ConfigurationTuring) -> bool:
        """Vérifie si la configuration est dans un état d'acceptation."""
        return config.state in self.accept_states


def read_turing(file: str):
    """
    Lit un fichier de transitions et construit une machine de Turing.
    Format attendu :
    - Lignes "accept qf ..." pour les états d'acceptation
    - Lignes "état,symbole : nouvel_état,nouveau_symbole,direction"
    """
    transitions = {}
    initial_state = None
    accept_states = set()

    with open(file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        if line.startswith("accept"):
            accept_states.update(line.split()[1:])
        else:
            left, right = [part.strip() for part in line.split(":")]
            state, symbol = [x.strip() for x in left.split(",")]
            new_state, new_symbol, move = [x.strip() for x in right.split(",")]

            # Le premier état rencontré est l'état initial
            if initial_state is None:
                initial_state = state

            transitions[(state, symbol)] = (new_state, new_symbol, move)

    return TuringMachine(transitions, initial_state, accept_states)


def simulate_turing(machine: TuringMachine, word: str):
    """
    Simule la machine de Turing sur un mot donné.
    Affiche chaque configuration jusqu'à acceptation ou rejet.
    """
    tape = list(word)
    head = 0
    state = machine.initial_state
    config = ConfigurationTuring(tape, head, state)

    print("Début de la simulation :")
    print(config)

    while config.state != "REJECT" and not machine.is_accepting(config):
        config = machine.step(config)
        print(config)

    if config.state == "REJECT":
        print("Résultat : REJECT")
    else:
        print("Résultat : ACCEPT")

def main(file: str):
    """
    Exemple d'utilisation : lit une machine de Turing, simule sur un mot.
    """
    # Machine de Turing
    machine = read_turing(file)
    simulate_turing(machine, "1010")

import sys

if __name__ == "__main__":
    fichier = sys.argv[1]
    print(f"Lecture de la machine de Turing à partir de {fichier}")
    main(fichier)
