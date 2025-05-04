import Automate as A
import Turing as T

def turing_to_automaton(file) -> A.Automaton:
    with open(file, 'r') as f:
        transitions = {}

        lines = [line.strip() for line in f if line.strip()]
        for line in lines:
            if line.startswith("accept"):
                continue
            left, right = [part.strip() for part in line.split(":")]
            state, symbol = [x.strip() for x in left.split(",")]
            new_state, new_symbol, move = [x.strip() for x in right.split(",")]

            if move == "S":
                values = ["*0", "*1", "-1"]
                for left in values:
                    for right in values:
                        transitions[(left, state + symbol, right)] = str(new_state) + str(new_symbol)
            elif move == "R":
                values = ["*0", "*1", "-1"]
                center_values = ["*0", "*1"]
                for left in values:
                    for center in center_values:
                        for right in values:
                            transitions[(left, state + symbol, right)] = "*" + new_symbol
                            transitions[(state + symbol, center, right)] = new_state + new_symbol
            elif move == "L":
                values = ["*0", "*1", "-1"]
                center_values = ["*0", "*1"]
                for left in values:
                    for center in center_values:
                        for right in values:
                            transitions[(left, state + symbol, right)] = "*" + new_symbol
                            transitions[(left, center, state + symbol)] = new_state + new_symbol

    return A.Automaton(transitions)

def main():
    automaton = turing_to_automaton("./turing/test.txt")
    for key, val in automaton.transitions.items():
        print(f"{key} → {val}")

    A.ConfigurationAutomaton(["*0", "q10", "*1", "*1"], automaton).simulate_automaton(10, stop_on_stable=True)
    T.ConfigurationTuring(["0", "0", "1", "1"], machine = T.read_turing("./turing/test.txt"), state = "q1", head = 1).simulate_turing()
