from typing import Dict, List, Tuple


class Automata:
    def __init__(self, transitions: Dict[tuple, int], default_state=-1):
        self.transitions = transitions
        self.default_state = default_state

    def transition(self, left, center, right):
        return self.transitions.get((left, center, right), self.default_state)


class ConfigurationAutomata:
    def __init__(self, states: List[int], automata: Automata):
        default = automata.default_state
        if states[0] != default:
            states = [default] + states
        if states[-1] != default:
            states = states + [default]
        self.states = states
        self.automata = automata

    def next_step(self):
        states = self.states
        automata = self.automata
        default = automata.default_state

        states = [default] + states + [default]

        new = []
        for i in range(len(states)):
            left = states[i - 1] if i - 1 >= 0 else default
            center = states[i]
            right = states[i + 1] if i + 1 < len(states) else default
            new.append(automata.transition(left, center, right))

        # On garde au maximum un seul 'default' à chaque bord
        while len(new) > 2 and new[0] == default and new[1] == default:
            new.pop(0)
        while len(new) > 2 and new[-1] == default and new[-2] == default:
            new.pop()

        self.states = new

    def print_config(self):
        print(" ".join(str(s) for s in self.states))


def read_automata(file: str) -> Dict[tuple, int]:
    transitions = {}
    with open(file, 'r') as f:
        for line in f:
            if ":" in line:
                left, new_state = line.strip().split(":")
                l, c, r = map(int, left.strip().split(","))
                transitions[(l, c, r)] = int(new_state.strip())
    return transitions



class ConfigurationTuring:
    def __init__(self, tape: List[str], head: int, state: str):
        self.tape = tape
        self.head = head
        self.state = state

    def __str__(self):
        tape_str = ''.join(self.tape)
        pointer = ' ' * self.head + '^'
        return f"Tape: {tape_str}\n       {pointer}\nState: {self.state}"


class TuringMachine:
    def __init__(self, transitions: Dict[Tuple[str, str], Tuple[str, str, str]],
                 initial_state: str, accept_states: set, default_symbol: str = "-"):
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.default = default_symbol

    def step(self, config: ConfigurationTuring) -> ConfigurationTuring:
        symbol = config.tape[config.head] if 0 <= config.head < len(config.tape) else self.default

        if (config.state, symbol) not in self.transitions:
            config.state = "REJECT"
            return config

        new_state, new_symbol, move = self.transitions[(config.state, symbol)]

        # Ecrire le nouveau symbole
        if 0 <= config.head < len(config.tape):
            config.tape[config.head] = new_symbol
        else:
            if config.head < 0:
                config.tape.insert(0, new_symbol)
                config.head = 0
            else:
                config.tape.append(new_symbol)

        # Se déplacer sur le ruban
        if move == "R":
            config.head += 1
        elif move == "L":
            config.head -= 1

        if config.head < 0:
            config.tape.insert(0, self.default)
            config.head = 0
        elif config.head >= len(config.tape):
            config.tape.append(self.default)

        config.state = new_state

        return config

    def is_accepting(self, config: ConfigurationTuring) -> bool:
        return config.state in self.accept_states


def read_turing(file: str):
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

            # Le premier état est l'état initial
            if initial_state is None:
                initial_state = state

            transitions[(state, symbol)] = (new_state, new_symbol, move)

    return TuringMachine(transitions, initial_state, accept_states)




def main():
    # Exemple : configuration initiale (liste d'entiers)
    config_init = [1, 0, 0, 0, 0, 0, 0]
    steps = 10

    # Exemple avec le fichier
    file = "automata/runner2.txt"
    transitions = read_automata(file)

    automata = Automata(transitions)
    config = ConfigurationAutomata(config_init, automata)

    print("Simulation :")
    for _ in range(steps):
        config.print_config()
        config.next_step()


if __name__ == "__main__":
    main()
