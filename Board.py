"""
The Board class implements the functionality of the playing board
"""
from unittest import TestCase
from colorama import *


class GameError(Exception):
    """
    Exception class for violating the game's rules
    """
    def __init__(self, message):
        self.message = message


class Board:
    """
    The Board class stores the information of the playing board
    """
    def __init__(self):
        """
        B = black
        0 = empty
        W = white
        """
        self.board = [['0' for i in range(15)] for j in range(15)]

    def is_available(self, i, j):
        """
        Checks whether a cell is available
        :param i: row index
        :param j: column index
        :return: True if available, False if not
        """
        if self.board[i][j] in ['0', 0] and 0 <= i < 15 and 0 <= j < 15:
            return True
        return False

    def move(self, i, j, c):
        """
        Makes a move to the desired location with the specified colour
        :param i: row index
        :param j: column index
        :param c: the colour to make the move with
        :return:
        """
        if self.is_available(i, j) and 0 <= i < 15 and 0 <= j < 15:
            self.board[i][j] = c
        else:
            raise GameError("You can't make that move")

    def winning_move(self, i, j, c):
        """
        Checks whether there exist five pieces of colour c in a line containing the cell [i][j]
        :param i: line coordinate - int
        :param j: column coordinate - int
        :param c: colour - char
        :return: True or False whether it's a win or not
        """
        """Line"""
        nr = 0
        initial_i = i
        initial_j = j
        while self.board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j -= 1
        i = initial_i
        j = initial_j + 1
        while self.board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j += 1

        if nr > 4:
            return True

        """Column"""
        nr = 0
        i = initial_i
        j = initial_j
        while self.board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            i -= 1
        i = initial_i + 1
        j = initial_j
        while self.board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            i += 1

        if nr > 4:
            return True

        """First diagonal"""
        nr = 0
        i = initial_i
        j = initial_j
        while self.board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j -= 1
            i -= 1
        i = initial_i + 1
        j = initial_j + 1
        while self.board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j += 1
            i += 1

        if nr > 4:
            return True

        """Second diagonal"""
        nr = 0
        i = initial_i
        j = initial_j
        while self.board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j -= 1
            i += 1
        i = initial_i - 1
        j = initial_j + 1
        while self.board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j += 1
            i -= 1

        if nr > 4:
            return True

        return False

    def __str__(self):
        r = '   0 1 2 3 4 5 6 7 8 9 A B C D E\n'
        for i in range(15):
            r += str(i) + ' '
            if i < 10:
                r += ' '
            for j in range(15):
                if self.board[i][j] == 'W':
                    r += str(Back.WHITE + Fore.BLACK + self.board[i][j]) + ' '
                elif self.board[i][j] == 'B':
                    r += str(Back.BLACK + Fore.WHITE + self.board[i][j]) + ' '
                else:
                    r += str(Back.RESET + Fore.RESET + '_') + ' '
            r += '\n'
        return r


class TestBoard(TestCase):
    def setUp(self):
        self.b = Board()
        self.b.board[0][0] = 'B'
        self.b.board[0][1] = 'B'
        self.b.board[0][2] = 'B'
        self.b.board[0][3] = 'B'

    def test_is_available(self):
        self.assertFalse(self.b.is_available(0, 2))
        self.assertTrue(self.b.is_available(1, 2))

    def test_move(self):
        self.b.move(1, 3, 'W')
        self.assertEqual(self.b.board[1][3], 'W')
        self.assertFalse(self.b.is_available(1, 3))

    def test_winning_move(self):
        self.b.board[0][4] = 'B'
        self.assertTrue(self.b.winning_move(0, 4, 'B'))
        self.b.board[5][12] = 'B'
        self.b.board[6][11] = 'B'
        self.b.board[7][10] = 'B'
        self.b.board[8][9] = 'B'
        self.b.board[9][8] = 'B'
        self.assertTrue(self.b.winning_move(9, 8, 'B'))
        self.assertFalse(self.b.winning_move(9, 8, 'W'))