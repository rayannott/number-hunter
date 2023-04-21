import os
import pickle
from datetime import datetime

from utils import SAVES_DIR, GameInfo, N_FOR_BARGAIN
from game import Game
from exceptions import CustomException
from achievements import ACHIEVEMENTS


HELP_STR_MENU = [
    ['help', 'print this message'],
    ['new', 'create a new game with default settings'],
    ['new <name>', 'create a new game with a given name'],
    ['load', 'load a list of local saves'],
    ['load <index>', 'load a game with chosen index'],
    ['exit | quit', 'quit the program'],
    ['', ''],
]

HELP_STR = [
    ['help', 'print this message'],
    ['exit', 'save; go back to menu'],
    ['quit', 'save; quit the program'],
    ['inv | +', 'list your inventary: numbers and trades'],
    ['ach | achievements', 'list completed achievements'],
    ['ach | achievements -a', 'list all achievements'],
    ['<trade_index> *<args>', 'trade numbers!'],
    ['save', 'save the current state of the game (this is done automatically on "exit" and "quit")'],
    ['sell <trade_index>', 'give away the chosen trade and get from 1 to 2 random numbers'],
    ['bargain *<args>', f'give away {N_FOR_BARGAIN} unique numbers to get one random trade'],
]

class App:
    def menu(self):
        print('Menu')
        self.running_menu = True
        while self.running_menu:
            inp = input(': ')
            match inp.split():
                case ['help']:
                    for command, info in HELP_STR_MENU:
                        print(f'{command:<10}\t\t{info}')
                case ['new']:
                    self.gi = GameInfo()
                    self.save_name = self.gi.save_name
                    self.g = Game(self.gi)
                    self.run()
                case ['new', name]:
                    self.gi = GameInfo(name + '.pi')
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
                case ['exit' | 'quit']:
                    self.running_menu = False
                case _:
                    print(f'Unknown command: {inp}')

    def display_nums(self):
        print(', '.join(f'{num}({amount})' for num, amount in self.g.numbers.items() if amount))

    def display_trades(self):
        max_width = max(len(str(trade.trade.payment)) for trade in self.g.my_trades) + 2
        for i, trade in enumerate(self.g.my_trades):
            if trade.amount:
                pure_trade = trade.trade
                multiplier_str = f'{pure_trade.multiplier}*' if pure_trade.multiplier > 1 else ' '
                print(f'{i:>3}.({trade.amount}) {str(pure_trade.payment) + " "*(max_width - len(str(pure_trade.payment)))}     ->    {multiplier_str}{pure_trade.returns.name}')

    def alert_new_achievements(self):
        just_completed_achievements = self.g.check_achievements()
        if just_completed_achievements:
            print('--- New achievement! ---')
            for ach in just_completed_achievements:
                print(f'{ach.name}: {ach.descr}')

    def execute_command(self, command: str):
        cmds = command.split()
        match cmds:
            case ['help']:
                for command, info in HELP_STR:
                    print(f'{command:<20}\t\t{info}')
            case ['exit']:
                self.running = False
                self.save_game()
            case ['quit']:
                self.running = False
                self.running_menu = False
                self.save_game()
            case ['save']:
                self.save_game()
            case ['ach' | 'achievements']:
                if not self.g.achievements:
                    print('no achievements')
                else:
                    print('*** Completed achievements ***')
                    for ach in self.g.achievements:
                        print(f'{ach.name}: {ach.descr}')
            case ['ach' | 'achievements', flag]:
                if not flag in ['-a', '--all']:
                    print(f'{flag} is an unknown flag')
                    return
                print('--- All achievements ---')
                for ach in ACHIEVEMENTS:
                    posession_str = '+' if ach in self.g.achievements else '-'
                    print(f'[{posession_str}] {ach.name}: {ach.descr}')     
            case ['inv' | '+']:
                self.display_nums()
                print()
                self.display_trades()
            case ['sell', trade_index]:
                returns = self.g.sell(int(trade_index))
                print(f'You sold the trade and received: {returns}')
                self.alert_new_achievements()
            case ['bargain', *args_str]:
                args = list(map(int, args_str))
                try:
                    received_trade = self.g.bargain(args)
                except CustomException as e:
                    print(e)
                else:
                    print(f'Bargain successful! You received: {received_trade}')
                    self.alert_new_achievements()
            case [trade_index, *args_str]:
                # trade!
                args = list(map(int, args_str))
                try:
                    returns, gifted_trade = self.g.trade(int(trade_index), args)
                except CustomException as e:
                    print(e)
                else:
                    add = f' and new trade "{gifted_trade}".' if gifted_trade else '.'
                    print(f'You received: {returns}{add}')
                    self.alert_new_achievements()

    def run(self):
        self.running = True
        print(f'Started game {self.gi.save_name} from {datetime.fromtimestamp(self.gi.date_created_timestamp)}')
        self.execute_command('inv')
        self.alert_new_achievements()
        while not self.g.is_victory() and self.running:
            inp = input('>>> ')
            self.execute_command(inp)
        
        if self.g.is_victory():
            print('You won!')

    def save_game(self):
        with open(os.path.join(SAVES_DIR, self.save_name), 'wb') as f:
            pickle.dump(self.g, f)
