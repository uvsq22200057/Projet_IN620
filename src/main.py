from typing import Dict, List


class Automata:
    def __init__(self, transitions: Dict[tuple, int], default_state=-1):
        self.transitions = transitions
        self.default_state = default_state

    def transition(self, left, center, right):
        return self.transitions.get((left, center, right), self.default_state)


class Configuration:
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


def read_transitions(file: str) -> Dict[tuple, int]:
    transitions = {}
    with open(file, 'r') as f:
        for line in f:
            if ":" in line:
                left, new_state = line.strip().split(":")
                l, c, r = map(int, left.strip().split(","))
                transitions[(l, c, r)] = int(new_state.strip())
    return transitions


def main():
    # Exemple : configuration initiale (liste d'entiers)
    config_init = [0, 0, 0, 1, 0, 0, 0]
    steps = 10

    # Exemple avec le fichier
    file = "runner.txt"
    transitions = read_transitions(file)

    automata = Automata(transitions)
    config = Configuration(config_init, automata)

    print("Simulation :")
    for _ in range(steps):
        config.print_config()
        config.next_step()


if __name__ == "__main__":
    main()
