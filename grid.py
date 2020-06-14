import numpy as np

class Grid:

    def __init__(self):
        self.kGridWidth = 7
        self.kGridHeight = 6
        self.grid = np.zeros((self.kGridWidth, self.kGridHeight), dtype=np.uint8)

    def insert(self, column: int, player: int):
        assert(column >= 0), "Negative column not allowed"
        assert(column < self.kGridWidth), "Column number greater than grid size"
        assert(self.grid[column][-1] == 0), "Column already full"
        idx_lst = np.where(self.grid[column]==0)
        self.grid[column][idx_lst[0][0]] = player

    def print(self):
        for row in self.grid.transpose()[::-1]:
            for col_i in row:
                if col_i != 0:
                    print('|', col_i, end=' ')
                else:
                    print('|', ' ', end=' ')
            print('|\n', *['-']*(self.kGridWidth*4+1), sep='')
    
    def won(self):
        for i in range(0, self.kGridWidth):
            for j in range(0, self.kGridHeight):
                try:
                    player_won = self.check_cell(i,j)
                except AssertionError as e:
                    continue
                if player_won is not None:
                    return player_won

    def check_cell(self, col: int, row: int):
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
            return cell_player

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
            return cell_player

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
            return cell_player  

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
            return cell_player


if __name__ == "__main__":
    g = Grid()
    g.insert(0, player=1)
    g.insert(1, player=1)
    g.insert(1, player=1)

    for i in range(0,4):
        g.insert(2, player=1)
        g.insert(3, player=1)
    g.print()
    print(g.won())
        

