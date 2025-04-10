class Cell:
    """A class to represent a cell in a cellular automata"""
    def __init__(self, left=None, right=None):
        self.state = False
        self.left = left
        self.right = right

    def get_state(self):
        return self.state
    
    def set_state(self):
        self.state = True if self.state == False else False

    def set_state2(self, state: bool):
        self.state = state
        
class Automata:
    """A class to represent a cellular automata"""
    def __init__(self):
        self.cells = []

if __name__ == "__main__":
    automata = Automata()
    cell1 = Cell()
    cell2 = Cell()
    cell3 = Cell()
    automata.cells.append(cell1)
    automata.cells.append(cell2)
    automata.cells.append(cell3)
    cell1.left = cell2
    cell2.set_state(True)
    cell2.right = cell3
    print (cell1.left.get_state())