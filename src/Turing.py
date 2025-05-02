from typing import Dict, List, Tuple

class TuringMachine:
    """
    Implémente une machine de Turing :
    - alphabet : ensemble des symboles utilisés
    - transitions : dictionnaire {(état, symbole): (nouvel état, nouveau symbole, déplacement)}
    - initial_state : état initial
    - accept_states : ensemble des états d'acceptation
    - default : symbole par défaut pour les cases non initialisées du ruban
    """
    def __init__(self, alphabet: set,
                 transitions: Dict[Tuple[str, str], Tuple[str, str, str]],
                 initial_state: str, accept_states: set, default_symbol: str = "-"):
        self.alphabet = alphabet
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
            f"Alphabet: {', '.join(map(str, self.alphabet))}\n"
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
        symbol = self.tape[self.head] if 0 <= self.head < len(self.tape) else self.default

        if (self.state, symbol) not in machine.transitions:
            self.state = "REJECT"
            return self

        # Les changements
        new_state, new_symbol, move = machine.transitions[(self.state, symbol)]

        # Ecrire le nouveau symbole sur le ruban
        if 0 <= self.head < len(self.tape):
            tape_list = list(self.tape)
            tape_list[self.head] = new_symbol
            self.tape = ''.join(tape_list)
        else:
            if self.head < 0:
                self.tape.insert(0, new_symbol)
                self.head = 0
            else:
                self.tape.append(new_symbol)

        # Déplacer la tête de lecture
        if move == "R":
            self.head += 1
        elif move == "L":
            self.head -= 1

        # Gérer les débordements du ruban
        if self.head < 0:
            self.tape.insert(0, self.default)
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append(self.default)

        self.state = new_state

        return self
    
    def simulate_turing(self, word: str):
        """
        Simule la machine de Turing sur un mot donné.
        Affiche chaque configuration jusqu'à acceptation ou rejet.
        """
        tape = list(word)
        head = 0
        state = self.machine.initial_state

        print("Début de la simulation :")
        print(self)

        while self.state != "REJECT" and not self.machine.is_accepting(self.state):
            config = self.next_step()
            print(self)

        if self.state == "REJECT":
            print("Résultat : REJECT")
        else:
            print("Résultat : ACCEPT")

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

    return TuringMachine("", transitions, initial_state, accept_states)

def main(file: str, mot: str):
    """
    Exemple d'utilisation : lit une machine de Turing, simule sur un mot.
    """
    # Machine de Turing
    file = "turing/example.txt"
    machine = read_turing(file)
    mot = "01"
    config = ConfigurationTuring(mot, 0, machine.initial_state, machine)
    print("Simulation :")
    config.simulate_turing(mot)


import sys

if __name__ == "__main__":
    fichier = sys.argv[1]
    print(f"Lecture de la machine de Turing à partir de {fichier}")

    mot = sys.argv[2]
    
    main(fichier, mot)
