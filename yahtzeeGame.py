import random
from collections import Counter


class YahtzeeGame:
    def __init__(self):
        self.dice = [0] * 5
        self.turns = [3, 3]  # Number of turns for each player
        self.scores = {
            'ones': None, 'twos': None, 'threes': None, 'fours': None,
            'fives': None, 'sixes': None, 'three_of_a_kind': None,
            'four_of_a_kind': None, 'full_house': None, 'small_straight': None,
            'large_straight': None, 'yahtzee': None, 'chance': None
        }
        self.current_player = 0  # Start with player 0

    def switch_player(self):
        self.current_player = 1 - self.current_player  # Switch between 0 and 1

    def roll_dice(self, keep=None):
        if self.turns[self.current_player] == 0:
            return "No more rolls left"
        if keep is None:
            keep = []
        for i in range(5):
            if i not in keep:
                self.dice[i] = random.randint(1, 6)
        self.turns[self.current_player] -= 1
        return self.dice

    def reset(self):
        self.dice = [0] * 5
        self.turns = [3, 3]

    def calculate_score(self, category):
        counter = Counter(self.dice)
        if category == 'ones':
            return counter[1] * 1
        elif category == 'twos':
            return counter[2] * 2
        elif category == 'threes':
            return counter[3] * 3
        elif category == 'fours':
            return counter[4] * 4
        elif category == 'fives':
            return counter[5] * 5
        elif category == 'sixes':
            return counter[6] * 6
        elif category == 'three_of_a_kind':
            if any(count >= 3 for count in counter.values()):
                return sum(self.dice)
        elif category == 'four_of_a_kind':
            if any(count >= 4 for count in counter.values()):
                return sum(self.dice)
        elif category == 'full_house':
            if 3 in counter.values() and 2 in counter.values():
                return 25
        elif category == 'small_straight':
            if set([1, 2, 3, 4]).issubset(counter.keys()) or set([2, 3, 4, 5]).issubset(counter.keys()) or set([3, 4, 5, 6]).issubset(counter.keys()):
                return 30
        elif category == 'large_straight':
            if set([1, 2, 3, 4, 5]).issubset(counter.keys()) or set([2, 3, 4, 5, 6]).issubset(counter.keys()):
                return 40
        elif category == 'yahtzee':
            if any(count == 5 for count in counter.values()):
                return 50
        elif category == 'chance':
            return sum(self.dice)
        return 0

    def add_score(self, category):
        if self.scores[category] is None:
            self.scores[category] = self.calculate_score(category)
        else:
            return "Category already scored"
        return self.scores
