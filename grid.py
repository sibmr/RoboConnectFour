import numpy as np


class Grid:

    def __init__(self):
        # Setup internal grid state
        self.kGridWidth = 7
        self.kGridHeight = 6
        self.grid = np.zeros((self.kGridWidth, self.kGridHeight), dtype=np.uint8)
        self.counter = 0
        self.log = []

    def insert(self, column: int, player: int):
        # Insert item into defined column
        assert(column >= 0), "Negative column not allowed"
        assert(column < self.kGridWidth), "Column number greater than grid size"
        assert(self.grid[column][-1] == 0), "Column already full"
        idx_lst = np.where(self.grid[column]==0)
        row = idx_lst[0][0]
        self.grid[column][row] = player
        self.log.append([column, row])
        self.counter += 1

    def free_columns(self):
        # Return list of columns with remaining slots
        free = []
        for i, col in enumerate(self.grid):
            if col[-1] == 0:
                free.append(i)
        return free

    def equal(self, grid):
        return np.array_equal(self.grid, grid)

    def print(self):
        # Method to print grid state to console
        for row in self.grid.transpose()[::-1]:
            for col_i in row:
                if col_i != 0:
                    print('|', col_i, end=' ')
                else:
                    print('|', ' ', end=' ')
            print('|\n', *['-']*(self.kGridWidth*4+1), sep='')
    
    def won(self):
        # Check if game is won and return winning player
        for i in range(0, self.kGridWidth):
            for j in range(0, self.kGridHeight):
                try:
                    player_won = self.check_cell(i,j)
                except AssertionError as e:
                    continue
                if player_won is not None:
                    return player_won

    def check_cell(self, col: int, row: int):
        # Check if given cell is part of a winning connect 4 row
        player = self.grid[col][row]
        assert(player != 0), "Cell not filled yet"
        
        # Vertical
        counter_v = 0
        for i in range(-3,4):
            if row+i >= 0 and row+i < self.kGridHeight:
                cell_player = self.grid[col][row+i]
                if cell_player != player:
                    if i < 0:
                        counter_v = 0
                    if i > 0:
                        break
                else:
                    counter_v += 1
        if counter_v >= 4:
            #print("Won vertical")
            return player

        # Horizontal
        counter_h = 0
        for i in range(-3,4):
            if col+i >= 0 and col+i < self.kGridWidth:
                cell_player = self.grid[col+i][row]
                if cell_player != player:
                    if i < 0:
                        counter_h = 0
                    if i > 0:
                        break
                else:
                    counter_h += 1
        if counter_h >= 4:
            #print("Won horizontal")
            return player

        # Diagonal bottom left
        counter_d1 = 0
        for i in range(-3,4):
            if col+i >= 0 and row+i >= 0 and col+i < self.kGridWidth and row+i < self.kGridHeight:
                cell_player = self.grid[col+i][row+i]
                if cell_player != player:
                    if i < 0:
                        counter_d1 = 0
                    if i > 0:
                        break
                else:
                    counter_d1 += 1
        if counter_d1 >= 4:
            #print("Won diagonal bottom left")
            return player

        # Diagonal top left
        counter_d2 = 0
        for i in range(-3,4):
            if col-i >= 0 and row+i >= 0 and col-i < self.kGridWidth and row+i < self.kGridHeight:
                cell_player = self.grid[col-i][row+i]
                if cell_player != player:
                    if i < 0:
                        counter_d2 = 0
                    if i > 0:
                        break
                else:
                    counter_d2 += 1
        if counter_d2 >= 4:
            #print("Won diagonal top left")
            return player


if __name__ == "__main__":
    # Some setup to test the code
    g = Grid()

    for i in range(0,4):
        g.insert(3, player=1)
    g.print()
    print(g.won())
    print(g.check_cell(3,0))
        

