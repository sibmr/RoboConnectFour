import random
from copy import deepcopy
import time
import numpy as np

from grid import Grid
from game import Game


class Strategy:

    def __init__(self, player, grid: Grid):
        self.player = player
        self.grid = grid

    def insert(self, column):
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

