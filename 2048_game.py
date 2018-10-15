import sys
import random as rn
import numpy as np

import getch

class Game_2048(object):
    '''
        2048 Game Implementation
    '''
    def __init__(self, shape):
        # Initialize the board
        self.board = np.zeros(shape, dtype=np.int)

    def is_game_over(self):
        return False

    def fill_matrix(self, board):
        """ Fill the matrix with random 2 or 4 on random psoition."""
        i, j = (board == 0).nonzero()
        if i.size != 0:
            rnd = rn.randint(0, i.size - 1)
            board[i[rnd], j[rnd]] = 2 * ((rn.random() > .9) + 1)
        return board

    def move_element(self, col):
        '''
        summation of two adjacent numbers having same values
        and move them to left
        '''
        new_col = np.zeros((col.size), dtype=col.dtype)
        j = 0
        previous = None
        for i in range(col.size):
            if col[i] != 0:
                if previous is None:
                    previous = col[i]
                else:
                    if previous == col[i]:
                        new_col[j] = 2 * col[i]
                        j += 1
                        previous = None
                    else:
                        new_col[j] = previous
                        j += 1
                        previous = col[i]
        if previous is not None:
            new_col[j] = previous
        return new_col

    def move(self, direction):
        rotated_board = np.rot90(self.board, direction)
        cols = [rotated_board[i, :] for i in range(rotated_board.shape[0])]
        new_board = np.array([self.move_element(col) for col in cols])
        return np.rot90(new_board, -direction)

    def start_game(self, direction):
        new_board = self.move(direction)
        if np.array_equal(self.board, new_board):
            if 0 not in new_board:
                moved = self.is_game_over()
            return True, new_board
        else:
            self.board = new_board
            moved = True
        new_board = self.fill_matrix(new_board)
        return moved, new_board


mapper = {
    'a': 0,
    'w': 1,
    'd': 2,
    's': 3
}
try:
    t = (sys.argv[1], sys.argv[2])
except IndexError as e:
    t = (4, 4)
game = Game_2048(t)
game.fill_matrix(game.board)
game.fill_matrix(game.board)
print(game.board)

while True:
    d = getch.getche()
    try:
        flag, board = game.start_game(mapper[d])
        print(board)
        if not flag:
            break
    except KeyError:
        print("Please enter valid move(use a:left, d:right, w:up, s:down)")
