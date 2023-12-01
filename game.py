import random
import pickle
from cfr import *
import time

with open("bot.p", "rb") as f:
    trainer = pickle.load(f)


def get_action(hand, history = ''):
    strength = str(evaluate_hand(hand))
    key = strength + ' ' + history
    strategy = [float(prob) for prob in trainer.node_map[key].get_average_strategy()]
    action = random.choices(['p', 'b'], weights=strategy, k=1)[0]
    return action

def deal_hands(deck):
    random.shuffle(deck)
    return [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]

def player_action(player_hand):
    print(f'Your hand is {player_hand}')
    while True:
        action = input("Enter your action (p for pass, b for bet, exit to quit): ")
        if action in ['p', 'b']:
            return action
        elif action.lower() == 'exit':
            print("Exiting game...")
            exit()  # Exit the game
        else:
            print("Invalid action. Please enter 'p' for pass, 'b' for bet, or 'exit' to quit.")

class poker_game:
    def __init__(self):
        self.pot = 0
        self.round = 0
        self.player_chips = 100
        self.bot_chips = 100
        self.deck = create_deck()
        self.round = 0
        self.active_player = 0
    
    def reset_chips(self):
        self.player_chips = 100
        self.bot_chips = 100

    def play(self):
        print('To play the game, press b to bet and p to pass')
        while self.player_chips > 0 and self.bot_chips > 0:
            time.sleep(2)
            self.player_chips -= 10
            self.bot_chips -= 10
            self.round += 1
            pot = 20
            random.shuffle(self.deck)
            player_hand = [self.deck[0],self.deck[1]]
            bot_hand = [self.deck[2],self.deck[3]]
            history = ''
            

            if self.round % 2 == 0:
                self.active_player = 0
                print('_____________________________________________')
                print(f'Start Round {self.round}, You go first')
                print(f'You have {self.player_chips+10} and Bot has {self.bot_chips+10}')
                print('_____________________________________________')
                action = str(player_action(player_hand))
                history = history + action
                time.sleep(1)
                bot_action = get_action(bot_hand, history)
                history = history + bot_action

                if history == 'pp':
                    print('The bot has passed')
                    time.sleep(1)
                    if compare_hands(player_hand, bot_hand) == 0:
                        self.player_chips += 10
                        self.bot_chips += 10
                        print(f'The bot had {bot_hand}')
                        print('Tie, chips are returned')
                    elif compare_hands(player_hand, bot_hand) > 0:
                        self.player_chips += pot
                        print(f'The bot had {bot_hand}')
                        print('You have won!')
                    elif compare_hands(player_hand, bot_hand) < 0:
                        self.bot_chips += pot
                        print(f'The bot had {bot_hand}')
                        print('The bot wins')
                
                elif history == 'bb':
                    pot += 20
                    self.player_chips -= 10
                    self.bot_chips -= 10
                    print('The bot has bet')

                    if compare_hands(player_hand, bot_hand) == 0:
                        self.player_chips += 20
                        self.bot_chips += 20
                        print(f'The bot had {bot_hand}')
                        print('Tie, chips are returned')
                    elif compare_hands(player_hand, bot_hand) > 0:
                        self.player_chips += pot
                        print(f'The bot had {bot_hand}')
                        print('You have won!')
                    elif compare_hands(player_hand, bot_hand) < 0:
                        self.bot_chips += pot
                        print(f'The bot had {bot_hand}')
                        print('The bot wins')
                
                elif history == 'bp':
                    self.player_chips += 20
                    print('The bot has folded, you win!')
                
                elif history == 'pb':
                    print('The bot has raised')
                    action = str(player_action(player_hand))
                    history = history + action

                    if history == 'pbp':
                        print('You fold, the Bot wins')
                        self.bot_chips += pot
                    
                    if history  == 'pbb':
                        pot += 20
                        self.player_chips -= 10
                        self.bot_chips -= 10
                        if compare_hands(player_hand, bot_hand) == 0:
                            self.player_chips += 20
                            self.bot_chips += 20
                            print(f'The bot had {bot_hand}')
                            print('Tie, chips are returned')
                        elif compare_hands(player_hand, bot_hand) > 0:
                            self.player_chips += pot
                            print(f'The bot had {bot_hand}')
                            print('You have won!')
                        elif compare_hands(player_hand, bot_hand) < 0:
                            self.bot_chips += pot
                            print(f'The bot had {bot_hand}')
                            print('The bot wins')                        

            if self.round % 2 != 0:
                self.active_player = 0
                print('_____________________________________________')
                print(f'Start Round {self.round}, Bot goes first')
                print(f'You have {self.player_chips+10} and Bot has {self.bot_chips+10}')
                print('_____________________________________________')
                print('Press p to pass and b to bet')
                bot_action = get_action(bot_hand, )
                history = history + bot_action

                if history == 'b':
                    print('The bot has bet')
                    action = player_action(player_hand)
                    history = history + action

                    if history == 'bb':
                        pot += 20
                        self.player_chips -= 10
                        self.bot_chips -= 10
                        if compare_hands(player_hand, bot_hand) == 0:
                            self.player_chips += 20
                            self.bot_chips += 20
                            print(f'The bot had {bot_hand}')
                            print('Tie, chips are returned')
                        elif compare_hands(player_hand, bot_hand) > 0:
                            self.player_chips += pot
                            print(f'The bot had {bot_hand}')
                            print('You have won!')
                        elif compare_hands(player_hand, bot_hand) < 0:
                            self.bot_chips += pot
                            print(f'The bot had {bot_hand}')
                            print('The bot wins')  
                    
                    if history == 'bp':
                        print('You have folded, the bot wins')
                        self.bot_chips += pot
                
                if history == 'p':
                    print('The bot has passed')
                    action = player_action(player_hand)
                    history = history + action

                    if history == 'pb':
                        time.sleep(2)
                        bot_action = get_action(bot_hand, history)
                        history = history + bot_action
                        
                        if bot_action == 'p':
                            print('The bot has folded, you win!')
                            self.player_chips += pot
                        
                        elif bot_action == 'b':
                            print('The bot as called')
                            time.sleep(1)
                            pot += 20
                            self.player_chips -= 10
                            self.bot_chips -= 10
                            if compare_hands(player_hand, bot_hand) == 0:
                                self.player_chips += 20
                                self.bot_chips += 20
                                print(f'The bot had {bot_hand}')
                                print('Tie, chips are returned')
                            elif compare_hands(player_hand, bot_hand) > 0:
                                self.player_chips += pot
                                print(f'The bot had {bot_hand}')
                                print('You have won!')
                            elif compare_hands(player_hand, bot_hand) < 0:
                                self.bot_chips += pot
                                print(f'The bot had {bot_hand}')
                                print('The bot wins')
                
                    if history == 'pp':
                        if compare_hands(player_hand, bot_hand) == 0:
                            self.player_chips += 10
                            self.bot_chips += 10
                            print(f'The bot had {bot_hand}')
                            print('Tie, chips are returned')
                        elif compare_hands(player_hand, bot_hand) > 0:
                            self.player_chips += pot
                            print(f'The bot had {bot_hand}')
                            print('You have won!')
                        elif compare_hands(player_hand, bot_hand) < 0:
                            self.bot_chips += pot
                            print(f'The bot had {bot_hand}')
                            print('The bot wins')
        
        print(f'Game over: Bot has {self.bot_chips} and you have {self.player_chips}')
        self.reset_chips()
    
mygame = poker_game()
mygame.play()







