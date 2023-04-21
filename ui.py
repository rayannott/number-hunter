import os
import pickle
from datetime import datetime

from utils import SAVES_DIR, GameInfo
from game import Game
from exceptions import CustomException


HELP_STR = [
    ['help', 'print this message'],
    ['new', 'create a new game with default settings'],
    ['new <name>', ''],
    ['load', 'load a list of local saves'],
    ['load <index>', 'load a game with chosen index'],
    ['exit', 'exit the program'],
    ['', ''],
]


class App:
    def menu(self):
        print('Menu')
        self.running_menu = True
        while self.running_menu:
            inp = input(': ')
            match inp.split():
                case ['help']:
                    for command, info in HELP_STR:
                        print(f'{command:<10}\t\t{info}')
                case ['new']:
                    self.gi = GameInfo()
                    self.save_name = self.gi.save_name
                    self.g = Game(self.gi)
                    self.run()
                case ['new', name]:
                    self.gi = GameInfo(name)
                    self.save_name = self.gi.save_name
                    self.g = Game(self.gi)
                    self.run()
                case ['load']:
                    self.game_files = [file for file in os.listdir('saves') if file.endswith('.pi')]
                    if not self.game_files:
                        print('no saves')
                    else:
                        for i, file in enumerate(self.game_files):
                            print(i, file)
                case ['load', game_ind_str]:
                    self.game_files = [file for file in os.listdir('saves') if file.endswith('.pi')]
                    if not self.game_files:
                        print('no saves')
                    else:
                        self.save_name = self.game_files[int(game_ind_str)]
                        with open(os.path.join(SAVES_DIR, self.save_name), 'rb') as f:
                            self.g: Game = pickle.load(f) # TODO: does not load
                            self.gi = self.g.info
                        self.run()
                case ['exit']:
                    self.running_menu = False

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
            case ['quit']:
                self.running = False
                self.running_menu = False
            case ['nums']:
                self.display_nums()
            case ['trades']:
                self.display_trades()
            case ['inv']:
                self.display_nums()
                print()
                self.display_trades()
            case [trade_index, *args_str]:
                # trade!
                args = list(map(int, args_str))
                try:
                    returns, gifted_trade = self.g.trade(int(trade_index), args)
                except CustomException as e:
                    print(e)
                else:
                    add = f' + new trade "{gifted_trade}".' if gifted_trade else '.'
                    print(f'You received: {returns}{add}')


    def run(self):
        self.running = True
        print(f'Started game {self.gi.save_name} from {datetime.fromtimestamp(self.gi.date_created_timestamp)}')
        while not self.g.is_victory() and self.running:
            inp = input('>>> ')
            self.execute_command(inp)
        
        if self.g.is_victory():
            print('You won!')

    def save_game(self):
        with open(os.path.join(SAVES_DIR, self.save_name), 'wb') as f:
            pickle.dump(self.g, f)
