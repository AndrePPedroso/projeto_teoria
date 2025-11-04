import random

class DilemaPrisioneiroUseCase:
    def __init__(self, strategy1, strategy2, iterations):
        self.strategy1 = strategy1
        self.strategy2 = strategy2
        self.iterations = iterations
        self.history1 = []
        self.history2 = []
        self.payoff1 = 0
        self.payoff2 = 0

    def get_payoffs(self, move1, move2):
        if move1 == 'cooperate' and move2 == 'cooperate':
            return 3, 3
        elif move1 == 'cooperate' and move2 == 'defect':
            return 0, 5
        elif move1 == 'defect' and move2 == 'cooperate':
            return 5, 0
        elif move1 == 'defect' and move2 == 'defect':
            return 1, 1

    def get_move(self, strategy, history, opponent_history):
        if strategy == 'always_cooperate':
            return 'cooperate'
        elif strategy == 'always_defect':
            return 'defect'
        elif strategy == 'tit_for_tat':
            if not opponent_history:
                return 'cooperate'
            else:
                return opponent_history[-1]
        elif strategy == 'random':
            return random.choice(['cooperate', 'defect'])

    def run_simulation(self):
        for _ in range(self.iterations):
            move1 = self.get_move(self.strategy1, self.history1, self.history2)
            move2 = self.get_move(self.strategy2, self.history2, self.history1)

            self.history1.append(move1)
            self.history2.append(move2)

            payoff1, payoff2 = self.get_payoffs(move1, move2)
            self.payoff1 += payoff1
            self.payoff2 += payoff2

        return {
            'history1': self.history1,
            'history2': self.history2,
            'payoff1': self.payoff1,
            'payoff2': self.payoff2,
        }
