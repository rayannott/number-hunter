import os
import random
from string import ascii_letters
import pickle

from utils import SAVES_DIR
from game import Game
from exceptions import CustomException


class App:
    def get_game(self):
        inp = input('New game? (y/n) ')
        if inp == 'y':
            self.save_name = ''.join(random.choices(ascii_letters, k=10)) + '.pi'
            return Game()
        # loading
        game_files = [file for file in os.listdir('saves') if file.endswith('.pi')]
        for i, file in enumerate(game_files):
            print(i, file)
        game_ind_str = input('Choose save: ')
        self.save_name = game_files[int(game_ind_str)] # TODO try int()
        with open(os.path.join(SAVES_DIR, self.save_name)) as f:
            g = pickle.load(f)
            return g

    def __init__(self) -> None:
        self.g = self.get_game()
        self.running = True

    def display_nums(self):
        print(', '.join(f'{num}({amount})' for num, amount in self.g.numbers.items() if amount))

    def display_trades(self):
        for i, trade in enumerate(self.g.my_trades):
            if trade.amount:
                print(f'{i}. {trade}')

    def execute_command(self, command: str):
        cmds = command.split()
        match cmds:
            case ['exit']:
                self.running = False
                self.save_game()
            case ['nums']:
                self.display_nums()
            case ['trades']:
                self.display_trades()
            case ['inv']:
                self.display_nums()
                print()
                self.display_trades()
            case ['trade' | 't', trade_index, *args_str]:
                args = list(map(int, args_str))
                try:
                    returns, gifted_trade = self.g.trade(int(trade_index), args)
                except CustomException as e:
                    print(e)
                else:
                    add = f' + new trade "{gifted_trade}".' if gifted_trade else '.'
                    print(f'You received: {returns}{add}')
            case ['shop']:
                print(self.g.available_deals)
            case ['shop', 'roll']:
                # TODO
                pass
            case ['shop', 'buy', buy_index_str]:
                buy_index = int(buy_index_str)
                # TODO

    def run(self):
        while not self.g.is_victory() and self.running:
            inp = input('>>> ')
            self.execute_command(inp)
        
        if self.g.is_victory():
            print('You won!')

    def save_game(self):
        with open(os.path.join(SAVES_DIR, self.save_name), 'wb') as f:
            pickle.dump(self.g, f)
