from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
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

        self.num_simulations = 200
        self.rollout_limit   = 40
        self.C               = 1.4

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        move_lists = self.board.get_all_possible_moves(self.color)
        legal_moves = self._flatten_moves(move_lists)

        if not legal_moves:
            return Move([])
        if len(legal_moves) == 1:
            best_move = legal_moves[0]
            self.board.make_move(best_move, self.color)
            return best_move

        plays = {m: 0 for m in legal_moves}
        wins = {m: 0.0 for m in legal_moves}

        for _ in range(self.num_simulations):
            root_move = self._select_move_ucb(legal_moves, wins, plays)
            winner = self._simulate(root_move)

            plays[root_move] += 1
            if winner == self.color:
                wins[root_move] += 1.0
            elif winner == 0:
                wins[root_move] += 0.5

        def avg_score(m):
            if plays[m] == 0:
                return -float('inf')
            return wins[m] / plays[m]

        best_move = max(legal_moves, key=avg_score)
        self.board.make_move(best_move, self.color)
        return best_move

    def _simulate(self, root_move):
        move_history = []

        self.board.make_move(root_move, self.color)
        move_history.append(root_move)
        current_color = self.opponent[self.color]

        steps = 0
        winner = 0
        while steps < self.rollout_limit:
            move_lists = self.board.get_all_possible_moves(current_color)
            legal_moves = self._flatten_moves(move_lists)

            if not legal_moves:
                winner = self.opponent[current_color]
                break

            m = legal_moves[randint(0, len(legal_moves) - 1)]
            self.board.make_move(m, current_color)
            move_history.append(m)

            current_color = self.opponent[current_color]
            steps += 1
        else:
            winner = 0

        for _ in range(len(move_history)):
            self.board.undo()

        return winner

    def _flatten_moves(self, move_lists):
        flat = []
        for ml in move_lists:
            for m in ml:
                flat.append(m)
        return flat

    def _select_move_ucb(self, legal_moves, wins, plays):
        untried = [m for m in legal_moves if plays[m] == 0]
        if untried:
            return untried[randint(0, len(untried) - 1)]

        total_sim = sum(plays[m] for m in legal_moves)
        log_total = math.log(total_sim)

        best_score = -float('inf')
        best_move = None
        for m in legal_moves:
            q = wins[m] / plays[m]
            ucb = q + self.C * math.sqrt(log_total / plays[m])
            if ucb > best_score:
                best_score = ucb
                best_move = m
        return best_move