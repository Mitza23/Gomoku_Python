from copy import deepcopy
from unittest import TestCase
from colorama import *

from Board import Board


class AI:
    def __init__(self, colour, board):
        """
        The AI class represents the Minimax algorithm applied for Gomoku
        :param colour: the colour which is played by the computer - string
        :param board: the current board of the game on which the algorithm has to compute the best move - matrix
        """
        self._colour = colour
        self._board = deepcopy(board)
        
    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, colour):
        self._colour = colour

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        self._board = deepcopy(board)

    def score(self, move, board):
        """
        Calculates heuristically the score of a move
        5 in a row = 1000
        4 in a row = 150
        3 in a row = 20
        2 in a row = 5
        :param move: move that was last made and whose impact is analysed - Move
        :param board: the board on which the movement was executed - matrix
        :return: the score of the move - int
        """
        # board[move.i][move.j] = move.c

        # print_board(board)

        score = 0
        i = move.i
        j = move.j
        c = move.c
        s5 = 1000
        s4 = 150
        s3 = 20
        s2 = 5

        """Line"""
        nr = 0
        initial_i = i
        initial_j = j
        while board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j -= 1
        i = initial_i
        j = initial_j + 1
        while board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j += 1

        aux = 0
        if nr == 5:
            aux = s5
        elif nr == 4:
            aux = s4
        elif nr == 3:
            aux = s3
        elif nr == 2:
            aux = s2

        score = max(score, aux)

        """Column"""
        nr = 0
        i = initial_i
        j = initial_j
        while board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            i -= 1
        i = initial_i + 1
        j = initial_j
        while board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            i += 1

        aux = 0
        if nr == 5:
            aux = s5
        elif nr == 4:
            aux = s4
        elif nr == 3:
            aux = s3
        elif nr == 2:
            aux = s2

        score = max(score, aux)

        """First diagonal"""
        nr = 0
        i = initial_i
        j = initial_j
        while board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j -= 1
            i -= 1
        i = initial_i + 1
        j = initial_j + 1
        while board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j += 1
            i += 1

        aux = 0
        if nr == 5:
            aux = s5
        elif nr == 4:
            aux = s4
        elif nr == 3:
            aux = s3
        elif nr == 2:
            aux = s2

        score = max(score, aux)

        """Second diagonal"""
        nr = 0
        i = initial_i
        j = initial_j
        while board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j -= 1
            i += 1
        i = initial_i - 1
        j = initial_j + 1
        while board[i][j] == c and 0 <= i < 15 and 0 <= j < 15:
            nr += 1
            j += 1
            i -= 1

        aux = 0
        if nr == 5:
            aux = s5
        elif nr == 4:
            aux = s4
        elif nr == 3:
            aux = s3
        elif nr == 2:
            aux = s2

        score = max(score, aux)

        # board[move.i][move.j] = '0'

        if c != self.colour:
            score = -score

        return score

    @staticmethod
    def get_adjacent_cells(board, i, j, c, result, viz):
        """
        Gets all the adjacent cells that are free to move in
        :param board: board to be searched in - matrix
        :param i: line index - int
        :param j: column index - int
        :param c: colour of movement - char
        :param result: list of possible moves related to that cell - list of Move
        :param viz: matrix in which previous possible moves have been marked - matrix
        :return:
        """
        for line in [i-1, i, i+1]:
            for col in [j-1, j, j+1]:
                if board[line][col] in ['0', 0] and viz[line][col] in ['0', 0] and 0 <= line < 15 and 0 <= col < 15:
                    result.append(Move(line, col, c))
                    viz[line][col] = 1

        # r = ''
        # for i in range(15):
        #     for j in range(15):
        #         r += str(board[i][j]) + ' '
        #     r += '\n'
        # r += '\n\n\n'
        # print(r)
        #
        # r = ''
        # for i in range(15):
        #     for j in range(15):
        #         r += str(viz[i][j]) + ' '
        #     r += '\n'
        # r += '\n\n\n'
        # print(r)

    def possible_moves(self, board, c):
        """
        Returns a list of all possible moves that can be done by the colour c on adjacent cells in the matrix that have
        the same colour c
        :param board: the game board - matrix
        :param c: the colour of the move to be made - string
        :return: list of all possible moves - list of Move
        """
        # print("<><><><><>")
        # print(c)
        # print_board(board)
        # print("<><><><><>")
        result = []
        viz = [[0 for i in range(15)] for j in range(15)]

        for i in range(15):
            for j in range(15):
                if board[i][j] == c:
                    self.get_adjacent_cells(board, i, j, c, result, viz)
        return result

    def minimax(self, move, board, depth, max_depth):
        # print("Minimax depth:", depth)
        # print_board(board)
        score = self.score(move, board)
        if score in [-1000, 1000] or depth == max_depth:
            return score

        else:
            if move.c == 'W':
                next_c = 'B'
            else:
                next_c = 'W'

            possible_moves = self.possible_moves(board, next_c)
            # print(len(possible_moves))
            # print(depth, 'next_c', next_c, "possible moves")
            # for mov in possible_moves:
            #     print(mov.i, mov.j, mov.c)
            #
            # print('========================')
            if len(possible_moves) == 0:
                return 0
            else:
                if depth % 2 == 1:
                    '''Minimizer'''
                    best_score = 10000
                    for new_move in possible_moves:
                        board[new_move.i][new_move.j] = new_move.c

                        score = self.minimax(new_move, board, depth + 1, max_depth)

                        board[new_move.i][new_move.j] = '0'
                        # print('MINI', new_move.i, new_move.j, new_move.c, 'score', score, 'depth', depth)
                        best_score = min(best_score, score)
                        if best_score == -1000:
                            return best_score

                else:
                    '''Maximizer'''
                    best_score = -10000
                    for new_move in possible_moves:
                        board[new_move.i][new_move.j] = new_move.c

                        score = self.minimax(new_move, board, depth + 1, max_depth)

                        board[new_move.i][new_move.j] = 0
                        # print('MAXI', new_move.i, new_move.j, new_move.c, 'score', score, 'depth', depth)
                        best_score = max(best_score, score)
                        if best_score == 1000:
                            return best_score

                return best_score

    def best_move(self, board, c):
        possible_moves = self.possible_moves(board, c)
        best_move = Move(0, 0, c, -1000000)
        for mov in possible_moves:
            board[mov.i][mov.j] = mov.c
            mov.score = self.minimax(mov, board, 1, 3)
            board[mov.i][mov.j] = 0
            if mov.score > best_move.score:
                best_move = mov
        return best_move


class Move:
    def __init__(self, i, j, c, score=0):
        """
        The Move class represents a move done in the game of Gomoku
        :param i: row index - int
        :param j: column index - int
        :param c: colour of the play - string
        :param score: score of the move - int
        """
        self.i = i
        self.j = j
        self.c = c
        self.score = score


def print_board(board):
    r = '   0 1 2 3 4 5 6 7 8 9 A B C D E\n'
    for i in range(15):
        r += str(i) + ' '
        if i < 10:
            r += ' '
        for j in range(15):
            if board[i][j] == 'W':
                r += str(Back.BLUE + Fore.WHITE + board[i][j]) + ' '
            elif board[i][j] == 'B':
                r += str(Back.WHITE + Fore.BLACK + board[i][j]) + ' '
            else:
                r += str(Back.RESET + Fore.RESET + '_') + ' '
        r += '\n'
    print(r)


class TestAI(TestCase):
    def setUp(self):
        self.ai = AI('W', Board().board)
        self.ai.board[3][3] = 'W'
        self.ai.board[4][4] = 'W'
        self.ai.board[0][4] = 'B'
        self.ai.board[0][5] = 'B'
        self.ai.board[0][6] = 'B'

    def test_score(self):
        # print(self.ai.score(Move(0, 7, 'B'), self.ai.board))
        self.ai.board[0][7] = 'B'
        self.assertEqual(self.ai.score(Move(0, 7, 'B'), self.ai.board), -150)
        self.ai.board[0][7] = 0
        self.assertEqual(self.ai.score(Move(0, 6, 'B'), self.ai.board), -20)

    def test_get_adjacent_cells(self):
        result = []
        self.ai.get_adjacent_cells(self.ai.board, 3, 3, 'W', result, [[0 for i in range(15)] for j in range(15)])
        # for mov in result:
        #     print(mov.i, mov.j)
        self.assertEqual(len(result), 7, result)

    def test_possible_moves(self):
        result = self.ai.possible_moves(self.ai.board, 'W')
        # r = ''
        # for i in range(15):
        #     for j in range(15):
        #         r += str(self.ai.board[i][j]) + ' '
        #     r += '\n'
        # print(r)
        # for mov in result:
        #     print(mov.i, mov.j)
        self.assertEqual(len(result), 12)

    def test_minimax(self):
        self.ai.board[0][2] = 'B'
        self.ai.board[0][6] = '0'
        self.ai.colour = 'B'
        board = deepcopy(self.ai.board)
        score = self.ai.minimax(Move(0, 2, 'B'), board, 1, 4)
        print(score)
