from copy import deepcopy

from grid import Grid


class Game:

    def __init__(self, strategy_1, strategy_2, grid=None, selfstate=False):
        if grid is None:
            grid = Grid()
        self.grid = grid
        self.selfstate = selfstate
        self.grid_has_changed = False
        self.next_move = True
        self.player_1 = strategy_1(player=1, grid=self.grid, selfstate=selfstate)
        self.player_2 = strategy_2(player=2, grid=self.grid, selfstate=selfstate)
        self.player = self.player_1

    def turn(self):
        if self.player == self.player_1:
            self.player = self.player_2
        else:
            self.player = self.player_1

    def set_grid(self, grid):
        if not self.selfstate:
            if not self.grid.equal(grid):
                self.grid_has_changed = True
            elif self.grid_has_changed:
                self.grid_has_changed = False
                self.next_move = True
            self.grid.grid = grid
        else:
            print("Warning: Set grid but selfstate is True... Skip")

    def play(self):
        column = 0
        while column is not None:
            column = self.step()
        self.grid.print()

    def step(self):
        self.next_move = False
        self.grid.print()
        print("Player " + str(self.player.player) + "'s Turn: ", end='')
        if self.grid.won() is not None:
            print("*** Player " + str(self.grid.won()) + " won ***")
            return None
        column = self.player.insert()
        print(str(column))
        if column is None:
            print("*** Draw ***")
            return None

        self.turn()
        return column


if __name__ == "__main__":
    import strategy
    game = Game(strategy.MinMaxStrategy, strategy.MonteCarloStrategy)
    game.play()