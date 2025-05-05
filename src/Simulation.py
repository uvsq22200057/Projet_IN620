import sys
from typing import List

import Automate as A
import Turing as T

def read_word(word: str, initial_state: str) -> (List[str], List[str]):
    """
    Lit un mot et le convertit en une liste de caractères avec une * devant.
    Le premier caractère est précédé de l'état initial.
    """
    word_list_automate = []
    word_list_turing = []
    for i in range(len(word)):
        if i == 0:
            word_list_automate.append("-")
            word_list_automate.append(initial_state + word[i])
            word_list_turing.append(word[i])
        elif i == len(word) - 1:
            word_list_automate.append("*" + word[i])
            word_list_automate.append("-")
            word_list_turing.append(word[i])
        else:
            word_list_automate.append("*" + word[i])
            word_list_turing.append(word[i])
    return word_list_automate, word_list_turing

def turing_to_automaton(file) -> (A.Automaton, str):
    """
    Lit un fichier de transitions Turing et construit un automate cellulaire.
    Format attendu : chaque ligne doit être au format "état,symbole : nouvel_état,nouveau_symbole,mouvement"
    """
    with open(file, 'r') as f:
        transitions = {}
        initial_state = None
        final = []

        lines = [line.strip() for line in f if line.strip()]
        for line in lines:
            if line.startswith("accept"):
                final.append(line.split(maxsplit=1)[1].strip())
                continue
            left, right = [part.strip() for part in line.split(":")]
            state, symbol = [x.strip() for x in left.split(",")]
            new_state, new_symbol, move = [x.strip() for x in right.split(",")]

            if initial_state is None:
                initial_state = state

            values = ["*0", "*1", "-", "*-"]
            center_values = ["*0", "*1"]

            if move == "S":
                for left in values:
                    for right in values:
                        if str(new_state) in final:
                            transitions[(left, state + symbol, right)] = "*" + new_symbol
                        else:
                            transitions[(left, state + symbol, right)] = new_state + new_symbol

            elif move == "R":
                for left in values:
                    for center in center_values:
                        for right in values:
                            transitions[(left, state + symbol, right)] = "*" + new_symbol
                            transitions[(state + symbol, center, right)] = new_state + center[1]
                            transitions[(state + symbol, "-", "-1")] = new_state + "-"
                            transitions[(left, state + symbol, "-1")] = "*" + new_symbol
                            transitions[("-1", state + symbol, right)] = "*" + new_symbol

            elif move == "L":
                for left in values:
                    for center in center_values:
                        for right in values:
                            transitions[(left, state + symbol, right)] = "*" + new_symbol
                            transitions[(left, center, state + symbol)] = new_state + center[1]
                            transitions[("-1", "-", state + symbol)] = new_state + "-"
                            transitions[("-1", state + symbol, right)] = "*" + new_symbol
                            transitions[(left, state + symbol, "-1")] = "*" + new_symbol


    return A.Automaton(transitions), initial_state


def main(file: str, mot: str):
    """
    Lit une machine de Turing puis simule un mot sur un automate cellulaire.
    """
    automaton, initial_state = turing_to_automaton(file)
    word_automate, word_turing = read_word(mot, initial_state)

    A.ConfigurationAutomaton(word_automate, automaton).simulate_automaton(20, stop_on_stable=True)
    T.ConfigurationTuring(word_turing, machine = T.read_turing(file), state = initial_state, head = 0).simulate_turing()


if __name__ == "__main__":
    fichier = sys.argv[1]
    print(f"Lecture de la machine de Turing à partir de {fichier}")

    mot = sys.argv[2] if len(sys.argv) > 2 else ""

    main(fichier, mot)