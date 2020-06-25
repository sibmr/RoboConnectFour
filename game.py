from grid import Grid


class Game:

    def __init__(self, strategy_1, strategy_2, grid=None):
        if grid is None:
            grid = Grid()
        self.grid = grid
        self.player_1 = strategy_1(player=1, grid=self.grid)
        self.player_2 = strategy_2(player=2, grid=self.grid)
        self.player = self.player_1

    def turn(self):
        if self.player == self.player_1:
            self.player = self.player_2
        else:
            self.player = self.player_1

    def play(self):
        column = 0
        while column is not None:
            column = self.step()
        self.grid.print()

    def step(self):
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