from typing import Dict, List, Tuple, Set

class TuringMachine:
    """
    Implémente une machine de Turing :
    - transitions : dictionnaire {(état, symbole): (nouvel état, nouveau symbole, déplacement)}
    - initial_state : état initial
    - accept_states : ensemble des états d'acceptation
    - default : symbole par défaut pour les cases non initialisées du ruban
    """
    def __init__(self, transitions: Dict[Tuple[str, str], Tuple[str, str, str]],
                 initial_state: str, accept_states: Set[str], default_symbol: str = "-"):
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.default = default_symbol

    def __str__(self):
        transitions_str = "\n".join(
            f"({state}, {symbol}) -> ({new_state}, {new_symbol}, {move})"
            for (state, symbol), (new_state, new_symbol, move) in self.transitions.items()
        )
        return (
            f"Turing Machine:\n"
            f"Initial State: {self.initial_state}\n"
            f"Accept States: {', '.join(map(str, self.accept_states))}\n"
            f"Default Symbol: {self.default}\n"
            f"Transitions:\n{transitions_str}"
        )

    def is_accepting(self, state: str) -> bool:
        """Vérifie si l'état est dans un état d'acceptation."""
        return state in self.accept_states

class ConfigurationTuring:
    """
    Représente la configuration courante d'une machine de Turing :
    - tape : le ruban (liste de symboles)
    - head : position de la tête de lecture/écriture
    - state : état courant de la machine
    """
    def __init__(self, tape: List[str], head: int, state: str, machine: TuringMachine):
        self.tape = tape
        self.head = head
        self.state = state
        self.machine = machine

    def __str__(self):
        # Affiche le ruban, la position de la tête et l'état courant
        tape_str = ''.join(self.tape)
        pointer = ' ' * self.head + '^'
        return f"Tape: #{tape_str}#\n       {pointer}\nState: {self.state}"
    
    def next_step(self) -> 'ConfigurationTuring':
        """
        Effectue une transition de la machine de Turing :
        - Lit le symbole sous la tête
        - Applique la règle de transition (si elle existe)
        - Écrit le nouveau symbole
        - Déplace la tête (gauche/droite)
        - Met à jour l'état courant
        Retourne la nouvelle configuration.
        """
        machine = self.machine

        # Lire le symbole sous la tête
        # Si la tête est en dehors du ruban, on utilise le symbole par défaut
        symbol = self.tape[self.head] if 0 <= self.head < len(self.tape) else machine.default

        if (self.state, symbol) not in machine.transitions:
            self.state = "REJECT"
            return self

        # Les changements
        new_state, new_symbol, move = machine.transitions[(self.state, symbol)]

        # Extend tape if necessary
        if self.head < 0:
            self.tape.insert(0, machine.default)
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append(machine.default)

        self.tape[self.head] = new_symbol

        # Move head
        if move == "R":
            self.head += 1
        elif move == "L":
            self.head -= 1

        # Extend again if needed after move
        if self.head < 0:
            self.tape.insert(0, machine.default)
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append(machine.default)

        self.state = new_state

        return self
    
    def simulate_turing(self):
        """
        Simule la machine de Turing sur un mot donné.
        Affiche chaque configuration jusqu'à acceptation ou rejet.
        """
        print("Début de la simulation :")
        print(self)

        while self.state != "REJECT" and not self.machine.is_accepting(self.state):
            self.next_step()
            print(self)

        print("Résultat :", "ACCEPT" if self.machine.is_accepting(self.state) else "REJECT")

def read_turing(file: str):
    """
    Lit un fichier de transitions et construit une machine de Turing.
    Format attendu :
    - Lignes "état,symbole : nouvel_état,nouveau_symbole,direction"
    - Lignes "accept qf ..." pour les états d'acceptation
    - La première ligne est l'état initial
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

def main(file: str, mot: List[str]):
    """
    Lit une machine de Turing puis simule sur un mot.
    """
    machine = read_turing(file)
    config = ConfigurationTuring(mot, 0, machine.initial_state, machine)

    print("Simulation :")
    config.simulate_turing()


import sys

if __name__ == "__main__":
    fichier = sys.argv[1]
    print(f"Lecture de la machine de Turing à partir de {fichier}")

    mot = list(sys.argv[2]) if len(sys.argv) > 2 else list("")

    main(fichier, mot)
