import random


class TicTacToe:
    def __init__(self):
        self.board = None

    @staticmethod
    def select_menu():
        while True:
            command = input('Input command: ').split()
            if len(command) == 1 and command[0].lower() == 'exit':
                exit()
            elif len(command) == 3 and command[0].lower() == 'start':
                players = []
                for turn, option in enumerate(command[1:]):
                    turn = 'X' if turn == 0 else 'O'
                    if option.lower() == 'user':
                        players.append(User(turn))
                    elif option.lower() in ['easy', 'medium', 'hard']:
                        players.append(AI(turn, option.lower()))
                return players
            print('Bad parameters!')

    def check_winner(self, board=None):
        if board is None:
            board = self.board
        for i in range(3):
            if board.field[i][0] == board.field[i][1] == board.field[i][2] != ' ':
                return f'{board.field[i][0]} wins'
            elif board.field[0][i] == board.field[1][i] == board.field[2][i] != ' ':
                return f'{board.field[0][i]} wins'
        if board.field[0][0] == board.field[1][1] == board.field[2][2] != ' ':
            return f'{board.field[0][0]} wins'
        elif board.field[0][2] == board.field[1][1] == board.field[2][0] != ' ':
            return f'{board.field[0][2]} wins'
        if ' ' not in board.field[0] and ' ' not in board.field[1] and ' ' not in board.field[2]:
            return 'Draw'


class Board:
    def __init__(self):
        self.field = [[' ' for _ in range(3)] for _ in range(3)]

    def __str__(self):
        end = 9 * '-'
        return end + '\n' + '\n'.join('| ' + ' '.join(row) + ' |' for row in self.field) + '\n' + end


class User:
    def __init__(self, turn):
        self.turn = turn

    @staticmethod
    def move(board):
        while True:
            coordinates = input('Enter the coordinates: ').split()
            if not len(coordinates) == 2 or not coordinates[0].isdigit() and not coordinates[1].isdigit():
                print('You should enter numbers!')
            elif coordinates[1] not in '123' or coordinates[0] not in '123':
                print('Coordinates should be from 1 to 3!')
            elif board.field[int(coordinates[0]) - 1][int(coordinates[1]) - 1] != ' ':
                print('This cell is occupied! Choose another one!')
            else:
                return int(coordinates[0]) - 1, int(coordinates[1]) - 1


class AI:
    def __init__(self, turn, level):
        self.turn = turn
        self.other = 'X' if turn == 'O' else 'O'
        self.level = level

    def move(self, board):
        print(f'Making move level "{self.level}"')
        available = self.check_moves(board)
        if self.level == 'easy':
            return random.choice(available)
        if self.level == 'medium':
            return self.simulate(board, 'next') or random.choice(available)
        elif self.level == 'hard':
            return self.find_best_move(board)

    @staticmethod
    def check_moves(board):
        moves = []
        for i in range(3):
            for j in range(3):
                if board.field[i][j] == ' ':
                    moves.append((i, j))
        return moves

    def simulate(self, board, mode):
        for turn in [self.turn, self.other]:
            for i, j in self.check_moves(board):
                board.field[i][j] = turn
                winning_move = TicTacToe().check_winner(board)
                board.field[i][j] = ' '
                if mode == 'next' and winning_move:
                    return i, j

    def find_best_move(self, board):
        best_score = -1000
        best_move = (-1, -1)
        for i in range(3):
            for j in range(3):
                if board.field[i][j] == ' ':
                    board.field[i][j] = self.turn
                    score = self.minimax(board, 0, False)
                    board.field[i][j] = ' '
                    if score > best_score:
                        best_move = (i, j)
                        best_score = score
        return best_move

    def minimax(self, board, depth, is_max):
        result = TicTacToe().check_winner(board)
        if result:
            if result[0] == self.turn:
                return 100
            elif result[0] == self.other:
                return -100
            elif result == 'Draw':
                return 0
        if is_max:
            best = -1000
            for i in range(3):
                for j in range(3):
                    if board.field[i][j] == ' ':
                        board.field[i][j] = self.turn
                        best = max(best, self.minimax(board, 0, False))
                        board.field[i][j] = ' '
            return best
        else:
            best = 800
            for i in range(3):
                for j in range(3):
                    if board.field[i][j] == ' ':
                        board.field[i][j] = self.other
                        best = min(best, self.minimax(board, depth + 1, True))
                        board.field[i][j] = ' '
            return best


if __name__ == '__main__':
    game = TicTacToe()
    while True:
        game.board = Board()
        player_1, player_2 = game.select_menu()
        if isinstance(player_1, User):
            print(game.board)
        current = None
        while True:
            current = player_1 if not current or current == player_2 else player_2
            y, x = current.move(game.board)
            game.board.field[y][x] = current.turn
            print(game.board)
            winner = game.check_winner()
            if winner:
                print(winner, end='\n\n')
                break
