import random
from copy import deepcopy
import time
import numpy as np

from grid import Grid
from game import Game


class Strategy:

    def __init__(self, player, grid: Grid, selfstate=False):
        self.player = player
        self.grid = grid
        self.selfstate = selfstate

    def insert(self, column):
        # TODO remove insert method, no ground truth game state
        if self.selfstate:
            self.grid.insert(column, self.player)


class RandomStrategy(Strategy):

    def insert(self):
        column = None
        columns_free = self.grid.free_columns()
        if len(columns_free):
            index = random.randint(0, len(columns_free)-1)
            column = columns_free[index]
            Strategy.insert(self, column)
        return column


class HumanStrategy(Strategy):
    user_input = 6
    def insert(self):
        column = None
        columns_free = self.grid.free_columns()
        if len(columns_free):
            while column is None:
                ans = input()
                try:
                    column = int(ans)
                    if column not in columns_free:
                        column = None
                        raise IndexError
                except ValueError:
                    print("No valid integer, please try again: ", end='')
                except IndexError:
                    print("Column not available, please try again: ", end='')
            Strategy.insert(self, column)
        return column

class AsyncHumanStrategy(Strategy):

    def insert(self):
        column = None
        columns_free = self.grid.free_columns()
        if len(columns_free):
            while column is None:
                ans = self.user_input
                try:
                    column = int(ans)
                    if column not in columns_free:
                        column = None
                        raise IndexError
                except ValueError:
                    print("No valid integer, please try again: ", end='')
                except IndexError:
                    print("Column not available, please try again: ", end='')
            Strategy.insert(self, column)
        return column


class MonteCarloStrategy(Strategy):

    def insert(self):
        computation_time = 1.0
        column = None
        columns_free = self.grid.free_columns()
        if len(columns_free):
            columns_free_win_ratio = []
            for column_free in columns_free:
                wins = 0.0
                losses = 0.0
                start_time = time.time()
                while time.time() < start_time + computation_time / len(columns_free):
                    game = Game(RandomStrategy, RandomStrategy, deepcopy(self.grid), selfstate=True)
                    my_player_id = game.player.player
                    Strategy.insert(game.player, column_free)
                    game.turn()
                    running = True
                    while running:
                        column = game.player.insert()
                        if column is None:
                            break
                        idx_lst = np.where(game.grid.grid[column] != 0)
                        row = idx_lst[0][-1]
                        player_won_check = game.grid.check_cell(column, row)
                        player_won = game.grid.won()
                        #print("GAME GRID CHECK CELL: ", str(player_won), str(player_won_check), str(column), str(row))
                        if player_won != player_won_check:
                            pass #print("Bug: Win not caught")
                        if player_won is not None:
                            running = False
                            if player_won == my_player_id:
                                wins += 1
                            else:
                                losses += 1
                        game.turn()
                if losses == 0:
                    ratio = wins
                else:
                    ratio = wins/losses
                #print("Wins", str(wins), "Losses", str(losses))
                columns_free_win_ratio.append(ratio)
            index = np.where(columns_free_win_ratio == np.amax(columns_free_win_ratio))[0][0]
            column = columns_free[index]
            Strategy.insert(self, column)
        return column


class MinMaxStrategy(Strategy):

    def min_max(self, grid, depth, player, is_maximizing):
        if player == 1:
            other_player = 2
        else:
            other_player = 1
        if depth <= 0:
            return 0
        w = grid.won()
        if w is not None:
            if w == self.player:
                return depth
            else:
                return -depth
        if is_maximizing:
            best_value = 1
        else:
            best_value = -1
        for c in grid.free_columns():
            grid.insert(c, player)
            value = self.min_max(deepcopy(grid), depth-1, other_player, not is_maximizing)
            if is_maximizing:
                best_value = max(best_value, value)
            else:
                best_value = min(best_value, value)
        return best_value

    def insert(self):
        column = None
        columns_free = self.grid.free_columns()
        if len(columns_free):
            scores = [-10000] * len(self.grid.grid)
            for i in columns_free:
                grid = deepcopy(self.grid)
                grid.insert(i, self.player)
                if self.player == 1:
                    player = 2
                else:
                    player = 1
                scores[i] = self.min_max(grid, 4, player, False)
            column = scores.index(max(scores))
            Strategy.insert(self, column)
        return column
