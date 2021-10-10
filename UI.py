"""
The UI class allows the players to play
"""
from AI import AI, Move
from Board import *


class UIError(Exception):
    def __init__(self, message):
        self.message = message


class UI:
    """
    UI class lets the users plat
    """
    def __init__(self):
        """
        self.turn = 1 black's turn
        self.turn = -1 white's turn
        """
        self.board = Board()
        self.turn = 1

    def get_turn(self):
        """
        Returns the colour whose turn is
        :return:
        """
        if self.turn > 0:
            return 'B'
        else:
            return 'W'

    def print_board(self):
        print(self.board.__str__())

    def make_move(self, i, j):
        """
        Makes a move to the specified cell if possible
        :param i: row index
        :param j: column index
        :return:
        """
        c = self.get_turn()

        self.board.move(i, j, c)
        self.turn = -self.turn

    def get_move(self):
        """
        Awaits input from the user as coordinates for a move
        :return:
        """
        c = self.get_turn()
        c = c + '>> '
        move = input(c)
        tokens = move.strip().split(' ')
        if len(tokens) != 2:
            raise UIError("The coordinates must be two numbers between 0 an 14 included.")
        if not tokens[0].isnumeric() or not tokens[1].isnumeric():
            raise UIError("The move coordinates must be two numbers between 0 an 14 included.")
        else:
            i = int(tokens[0])
            j = int(tokens[1])
            if i < 0 or i > 14 or j < 0 or j > 14:
                raise UIError("Your moves should be numbers between 0 and 14 included")

            return i, j

    def play_against_human(self):
        """
        The function in which the game between 2 users is played
        :return:
        """
        done = False
        while not done:
            try:
                self.print_board()
                move = self.get_move()
                i, j = move[0], move[1]
                c = self.get_turn()
                self.make_move(i, j)
                done = self.board.winning_move(i, j, c)
            except (UIError, GameError) as error:
                print(str(error))

        self.turn = -self.turn
        self.print_board()
        print(self.get_turn(), "wins")

    def play_against_ai(self):
        ai = AI('W', self.board.board)
        done = False
        while not done:
            try:
                if self.turn > 0:
                    self.print_board()
                    move = self.get_move()
                    i, j = move[0], move[1]
                    c = self.get_turn()
                    self.make_move(i, j)
                    done = self.board.winning_move(i, j, c)

                else:
                    move = ai.best_move(self.board.board, self.get_turn())
                    print(move.i, move.j)
                    move.i = int(move.i)
                    move.j = int(move.j)
                    self.make_move(move.i, move.j)
                    done = self.board.winning_move(move.i, move.j, move.c)

            except (UIError, GameError) as error:
                print(str(error))

        self.turn = -self.turn
        self.print_board()
        print(self.get_turn(), "wins")

    def play(self):
        print("Who would you like to play against?")
        print("1. Human player")
        print("2. AI player")
        done = False
        while not done:
            command = input("Choose one >> ")
            command = command.strip()
            if command == '1':
                self.play_against_human()
                done = True
            elif command == '2':
                self.play_against_ai()
                done = True
            else:
                print("Your input must be 1 or 2")
        print("That's all folks!")


ui = UI()
ui.play()
