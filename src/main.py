class Cell:
    """A class to represent a cell in a cellular automata"""
    def __init__(self, state={0,1}, left=None, right=None):
        self.state = state
        self.left = left
        self.right = right

    def get_state(self):
        return self.state
    
    def get_neighbors(self):
        """Return the left and right neighbors of the cell"""
        return self.left, self.right
    
    def set_state(self):
        self.state = True if self.state == False else False

    def set_state2(self, state: bool):
        self.state = state
        
class Automata:
    """A class to represent a cellular automata"""
    def __init__(self, cells=None, transitions=None):
        self.cells = [] # a list of cells
        self.transitions = transitions # a dictionary of transitions {(s_left, s_center, s_right): s_next, ...}

        if cells is not None:
            self.set_cells(cells)

    def add_cell(self, cell):
        self.cells.append(cell)

    def set_cells(self, str_cells):
        for cell in str_cells:
            if cell == "0":
                cell = Cell(0)
            elif cell == "1":
                cell = Cell(1)
            elif cell == "-1":
                cell = Cell(-1)
            else:
                raise ValueError("Invalid cell state")
            # Add the cell to the automata
            self.add_cell(cell)

        for i, cell in enumerate(self.cells):
            if i == 0: # first cell
                cell.left = None
            else:
                cell.left = self.cells[i-1]

            if i == len(self.cells) - 1: # last cell
                cell.right = None
            else:
                cell.right = self.cells[i+1]

    def set_transitions(self, *args):
        if len(args) == 1:
            file = args[0]
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line.startswith("#"):
                        continue
                    parts = line.split(",")
                    if len(parts) == 4:
                        self.transitions[(int(parts[0]), int(parts[1]), int(parts[2]))] = int(parts[3])
                    else:
                        raise ValueError("Invalid transition format")
                    
    def get_transitions(self):
        return self.transitions 

    def print_cells(self):
        for i, cell in enumerate(self.cells):
            print(f"Cell {i} — state: {cell.get_state()}")

            left, right = cell.get_neighbors()

            if left is not None:
                print(f"  Left neighbor (Cell {i-1}) state: {left.get_state()}")
            else:
                print("  Left neighbor: None")

            if right is not None:
                print(f"  Right neighbor (Cell {i+1}) state: {right.get_state()}")
            else:
                print("  Right neighbor: None")

            print("-" * 30)

        
class Configuration:
    """A class to represent a configuration of a cellular automata"""
    def __init__(self, automata_transitions:dict, cells:list[{-1,0,1}], t:int):
        self.automata = automata_transitions # a dictionary of transitions {(s_left, s_center, s_right): s_next, ...}
        self.cells = cells # a list of cells
        self.time = t # the time step

    def config(self, t, mot):
        pass

def main():
    config_initiale = "011001"
    automata = Automata(config_initiale)
    
    automata.print_cells()

if __name__ == "__main__":
    main()