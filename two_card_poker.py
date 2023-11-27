import numpy as np
import random
import time
import sys
import pickle

def card_value(card):
    """ Convert card to a value for comparison. Assumes card is a string like '2H' or 'AD' """
    value_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return value_dict[card[0]]

def evaluate_hand(hand):
    """ Evaluate a hand and return its score. """
    card1, card2 = hand
    value1, value2 = card_value(card1), card_value(card2)
    suit1, suit2 = card1[1], card2[1]

    # Check for suited pair, pair, suit, or high card
    if suit1 == suit2:
        if value1 == value2:
            return 300 + value1  # Suited pair
        else:
            return 100 + max(value1, value2)  # Suit
    elif value1 == value2:
        return 200 + value1  # Pair
    else:
        return max(value1, value2)  # High card

def compare_hands(player, opponent):
    """ Compare two hands and return the winning hand or 'Tie' """
    score1 = evaluate_hand(player)
    score2 = evaluate_hand(opponent)

    if score1 > score2:
        return 1
    elif score2 > score1:
        return -1
    else:
        return 0
    
def compare_strength(score1, score2):
    if score1 > score2:
        return 1
    elif score2 > score1:
        return -1
    else:
        return 0
    

def create_deck():
    suits = ['H', 'D' 'S', 'C'] 
    ranks = ['2', '3', '4', '5','6','7', '8', '9','T', 'J', 'Q', 'K', 'A']
    
    deck = [rank + suit for suit in suits for rank in ranks]
    return deck

class poker_bot:
    def __init__(self):
        self.node_map = {} # map the possible states
        self.expected_game_value = 0 # track the expected value
        self.current_player = 0 # track the current player
        self.deck = create_deck() # create the deck
        self.n_actions = 2 # total actions determine node splits
    
    def train(self, n_iter):
        """
        Iterates over the cfr function and updates the strategy 
        """
        expected_game_value = 0
        for _ in range(n_iter):
            if _ % 10000 == 0:
                print(_)
            random.shuffle(self.deck)
            expected_game_value += self.cfr('', 1, 1)
            for _, v in self.node_map.items():
                v.update_strategy()
            
        expected_game_value /= n_iter
        display_results(expected_game_value, self.node_map)
    
    def cfr(self, history, pr_1, pr_2):
        """
        history: past moves played
        pr_1: probability of playing the first option
        pr_2: probabilitiy of playing the second option
        """
        n = len(history)
        is_player1 = n % 2 == 0
        
        if is_player1:
            player_hand = evaluate_hand([self.deck[0], self.deck[1]])
            opponent_hand = evaluate_hand([self.deck[2], self.deck[3]])
        else:
            player_hand = evaluate_hand([self.deck[2], self.deck[3]])
            opponent_hand = evaluate_hand([self.deck[0], self.deck[1]])

        if self.is_terminal(history):
            reward = self.get_reward(history, player_hand, opponent_hand)
            return reward
        
        node = self.get_node(player_hand, history)
        strategy = node.strategy

        # Create a place to store payoffs
        action_utils = np.zeros(self.n_actions)

        # Find possible payoffs for both actions
        for act in range(self.n_actions):
            next_history = history + node.action_dict[act]
            if is_player1:
                action_utils[act] = -1 * self.cfr(next_history, pr_1 * strategy[act], pr_2)
            else:
                action_utils[act] = -1 * self.cfr(next_history, pr_1, pr_2 * strategy[act])

        util = sum(action_utils * strategy)
        regrets = action_utils - util
        if is_player1:
            node.reach_pr += pr_1
            node.regret_sum += pr_2 * regrets
        else:
            node.reach_pr += pr_2
            node.regret_sum += pr_1 * regrets

        return util

    @staticmethod
    def is_terminal(history):
        if history[-2:] == 'pp' or history[-2:] == "bb" or history[-2:] == 'bp':
            return True

    @staticmethod
    def get_reward(history, player_hand, opponent_hand):
        terminal_pass = history[-1] == 'p'
        double_bet = history[-2:] == "bb"
        if terminal_pass:
            if history[-2:] == 'pp':
                return compare_strength(player_hand, opponent_hand)
            else:
                return 1
        elif double_bet:
            return 2 * compare_strength(player_hand, opponent_hand)
    
    def get_node(self, hand, history):
        key = str(hand) + " " + history
        if key not in self.node_map:
            action_dict = {0: 'p', 1: 'b'}
            info_set = Node(key, action_dict)
            self.node_map[key] = info_set
            return info_set
        return self.node_map[key]
    
class Node:
    def __init__(self, key, action_dict, n_actions=2):
        self.key = key
        self.n_actions = n_actions
        self.regret_sum = np.zeros(self.n_actions)
        self.strategy_sum = np.zeros(self.n_actions)
        self.action_dict = action_dict 
        self.strategy = np.repeat(1/self.n_actions, self.n_actions)
        self.reach_pr = 0
        self.reach_pr_sum = 0

    def update_strategy(self):
        self.strategy_sum += self.reach_pr * self.strategy
        self.reach_pr_sum += self.reach_pr
        self.strategy = self.get_strategy()
        self.reach_pr = 0

    def get_strategy(self):
        regrets = self.regret_sum
        regrets[regrets < 0] = 0
        normalizing_sum = sum(regrets)
        if normalizing_sum > 0:
            return regrets / normalizing_sum
        else:
            return np.repeat(1/self.n_actions, self.n_actions)

    def get_average_strategy(self):
        strategy = self.strategy_sum / self.reach_pr_sum
        # Re-normalize
        total = sum(strategy)
        strategy /= total
        return strategy

    def __str__(self):
        strategies = ['{:03.2f}'.format(x)
                      for x in self.get_average_strategy()]
        return '{} {}'.format(self.key.ljust(6), strategies)

def display_results(ev, i_map):
    print('player 1 expected value: {}'.format(ev))
    print('player 2 expected value: {}'.format(-1 * ev))

    print()
    print('player 1 strategies:')
    sorted_items = sorted(i_map.items(), key=lambda x: x[0])
    for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
        print(v)
    print()
    print('player 2 strategies:')
    for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
        print(v)
