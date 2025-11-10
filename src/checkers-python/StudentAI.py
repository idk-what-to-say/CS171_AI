from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.max_depth = 4
    def get_move(self,move):
        # if len(move) != 0:
        #     self.board.make_move(move,self.opponent[self.color])
        # else:
        #     self.color = 1
        # moves = self.board.get_all_possible_moves(self.color)
        # index = randint(0,len(moves)-1)
        # inner_index =  randint(0,len(moves[index])-1)
        # move = moves[index][inner_index]
        # self.board.make_move(move,self.color)
        # return move
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)
        if not moves:
            return Move([])

        best_move = None
        best_value = float('-inf')
        for move_list in moves:
            for candidate_move in move_list:
                self.board.make_move(candidate_move, self.color)
                value = self._minimax(self.max_depth - 1, False, self.opponent[self.color], float('-inf'), float('inf'))
                self.board.undo()
                if value > best_value:
                    best_value = value
                    best_move = candidate_move

        if best_move is None:
            best_move = moves[0][0]

        self.board.make_move(best_move, self.color)
        return best_move

    def _minimax(self, depth, maximizing_player, current_color, alpha, beta):
        moves = self.board.get_all_possible_moves(current_color)
        if depth == 0:
            return self._evaluate_board()

        if not moves:
            return float('-inf') if maximizing_player else float('inf')

        if maximizing_player:
            value = float('-inf')
            for move_list in moves:
                for candidate_move in move_list:
                    self.board.make_move(candidate_move, current_color)
                    value = max(value, self._minimax(depth - 1, False, self.opponent[current_color], alpha, beta))
                    self.board.undo()
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break
            return value
        else:
            value = float('inf')
            for move_list in moves:
                for candidate_move in move_list:
                    self.board.make_move(candidate_move, current_color)
                    value = min(value, self._minimax(depth - 1, True, self.opponent[current_color], alpha, beta))
                    self.board.undo()
                    beta = min(beta, value)
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break
            return value

    def _evaluate_board(self):
        score = 0
        my_color = self._color_to_char(self.color)
        opponent_color = self._color_to_char(self.opponent[self.color])

        for r in range(self.row):
            for c in range(self.col):
                checker = self.board.board[r][c]
                if checker.color == my_color:
                    score += self._piece_value(checker)
                    score += self._positional_bonus(checker)
                elif checker.color == opponent_color:
                    score -= self._piece_value(checker)
                    score -= self._positional_bonus(checker)

        return score

    def _piece_value(self, checker):
        base_value = 5 if checker.is_king else 3
        return base_value

    def _positional_bonus(self, checker):
        if checker.is_king:
            return 0.5

        my_color = self._color_to_char(self.color)
        if my_color == 'B':
            advancement_bonus = checker.row * 0.1
        else:
            advancement_bonus = (self.row - 1 - checker.row) * 0.1

        central_bonus = (self.col / 2 - abs(checker.col - (self.col - 1) / 2)) * 0.05
        return advancement_bonus + central_bonus

    def _color_to_char(self, color):
        if color == 1:
            return 'B'
        return 'W'

