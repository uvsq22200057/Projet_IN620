from typing import Dict, List, Tuple


class Automaton:
    def __init__(self, transitions: Dict[tuple, int], default_state=-1):
        self.transitions = transitions
        self.default_state = default_state

    def transition(self, left, center, right):
        return self.transitions.get((left, center, right), self.default_state)


class ConfigurationAutomaton:
    def __init__(self, states: List[int], automaton: Automaton):
        default = automaton.default_state
        if states[0] != default:
            states = [default] + states
        if states[-1] != default:
            states = states + [default]
        self.states = states
        self.automaton = automaton

    def next_step(self) -> Tuple[List[int], bool, List[Tuple[int, int, int]]]:
        states = self.states
        automaton = self.automaton
        default = automaton.default_state

        states = [default] + states + [default]
        new = []
        used_transitions = []
        changed = False

        for i in range(len(states)):
            left = states[i - 1] if i - 1 >= 0 else default
            center = states[i]
            right = states[i + 1] if i + 1 < len(states) else default

            old = center
            new_state = automaton.transition(left, center, right)
            new.append(new_state)

            if new_state != center:
                changed = True

            if (left, center, right) in automaton.transitions:
                used_transitions.append((left, center, right))

        # On garde au maximum un seul 'default' à chaque bord
        while len(new) > 2 and new[0] == default and new[1] == default:
            new.pop(0)
        while len(new) > 2 and new[-1] == default and new[-2] == default:
            new.pop()

        self.states = new
        return new, changed, used_transitions

    def print_config(self):
        print(" ".join(str(s) for s in self.states))


def read_automaton(file: str) -> Automaton:
    transitions = {}
    with open(file, 'r') as f:
        for line in f:
            if ":" in line:
                left, new_state = line.strip().split(":")
                l, c, r = map(int, left.strip().split(","))
                transitions[(l, c, r)] = int(new_state.strip())
    return Automaton(transitions)


def simulate_automaton(config: ConfigurationAutomaton,
                       max_steps: int = 10,
                       stop_on_transition: Tuple[int, int, int] = None,
                       stop_on_stable: bool = False) -> None:

    for step in range(max_steps):
        print(f"Étape {step}:")
        config.print_config()

        _, changed, used_transitions = config.next_step()

        if stop_on_transition and stop_on_transition in used_transitions:
            print(f"Arrêt : transition {stop_on_transition} utilisée à l'étape {step}")
            break

        if stop_on_stable and not changed:
            print(f"Arrêt : configuration stable atteinte à l'étape {step}")
            break
    else:
        print("Arrêt : nombre maximal d'étapes atteint")



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


def simulate_turing(machine: TuringMachine, word: str):
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



def main():

    # Automate cellulaire
    config_init = [1, 0, 0, 0, 0, 0, 0]
    file = "automata/runner2.txt"
    automaton = read_automaton(file)
    config = ConfigurationAutomaton(config_init, automaton)
    print("Simulation :")
    simulate_automaton(config,
                       max_steps=20,
                       stop_on_transition=(1, 0, 0),
                       stop_on_stable=True)

    # Machine de Turing
    file = "turing/example.txt"
    machine = read_turing(file)
    simulate_turing(machine, "1010")


if __name__ == "__main__":
    main()
