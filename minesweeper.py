import random

import pprint

class Minesweeper():

    def __init__(self):
        self.board = None
        self.bombs = set()

    def _provision_bombs(self, bombs):
        if bombs < 0:
            raise Exception('Invalid Number of Bombs')
        while bombs != 0:
            row = random.randint(0, len(self.board)-1)
            col = random.randint(0, len(self.board[0])-1)
            if (row, col) not in self.bombs:
                    self.bombs.add((row, col))
                    bombs -= 1

    def print_board(self, with_bombs=False):
        if with_bombs:
            # the game must be over too.
            for (r,c) in self.bombs:
                self.board[r][c] = '*'
        #pprint.pprint(self.board)
        self._print_board()

    def _print_board(self):
        print '  ' + ' '.join([str(i) for i in range(1, len(self.board) + 1)])
        for i in range(len(self.board)):
            print(str(i+1) + ' ' +
                    ' '.join([str(k) for k in self.board[i]])
                    )

    def neighbors(self, r, c):
        # Returns a list of valid paths for that r,c
        lst = []
        def is_valid(row, col):
            return -1 < row < len(self.board) and -1  < col <len(self.board[0])

        for (x,y) in [
                (r, c-1),
                (r, c+1),
                (r-1, c),
                (r+1, c),
                (r-1, c-1),
                (r+1, c-1),
                (r+1, c+1),
                (r-1, c+1)]:
            if is_valid(x, y):
                lst.append((y,x))
        return lst

    def adjacent_bombs(self, r, c):
        "Returns the number of bombs next to the cell."
        bombs = 0
        for (row, column) in self.neighbors(r, c):
            if (row, column) in self.bombs:
                bombs += 1
        return bombs

    def reveal_cell(self, r, c):
        if self.board[r][c] == 'H':
            adj_bombs = self.adjacent_bombs(r, c)
            self.board[r][c] = adj_bombs or '.'
            if self.board[r][c] == '.': # No adjacent bombs, discover new cells
                for (r1, c1) in self.neighbors(r, c):
                    self.reveal_cell(r1, c1)

    def won_game(self):
        # doing a linear scan, can be optimized by tracking where user has already been
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == 'H' and (r, c) not in self.bombs:
                    return False


    def visit_cell(self, row, column):
        if (row, column) in self.bombs:
            return True
        self.reveal_cell(row, column)
        if self.won_game():
            return True
        return False


    def provision_board(self, row, column, bombs):
        self.board = [['H' for _ in range(column)] for _ in range(row)]
        self._provision_bombs(bombs)

    def main(self):
        while True:
            self.print_board()
            row = raw_input('Rows:')
            col = raw_input('Columns:')
            game_over =  self.visit_cell(int(row)-1, int(col)-1)
            if game_over:
                self.print_board(with_bombs=True)
                break

if __name__ == '__main__':
    row = raw_input('Rows for the board:')
    col = raw_input('Columns for the board:')
    mines = raw_input('Mines to place on the board:')
    game = Minesweeper()
    game.provision_board(int(row), int(col), int(mines))
    game.main()












