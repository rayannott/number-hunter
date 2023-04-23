import os
import pickle
from datetime import datetime

from utils import SAVES_DIR, GameInfo, N_FOR_BARGAIN, N
from game import Game
from exceptions import CustomException
from achievements import ACHIEVEMENTS
from return_types import HELP_RETURN_TYPES
from payments_library import HELP_PAYMENTS


HELP_STR_MENU = [
    ['help', 'print this message'],
    ['rules', 'print out the rules'],
    ['payments', 'describe each payment option'],
    ['returns', 'describe each return type'],
    ['new', 'create a new game with default settings'],
    ['new <name>', 'create a new game with a given name'],
    ['load', 'load a list of local saves'],
    ['load <index>', 'load a game with chosen index'],
    ['exit | quit', 'quit the program'],
]

HELP_STR = [
    ['help', 'show this message'],
    ['rules', 'print out the rules'],
    ['exit', 'save; go back to menu'],
    ['exit -d, --discard', 'do not save; go back to menu'],
    ['quit', 'save; quit the program'],
    ['inv | +', 'list your inventary: numbers and trades'],
    ['ach | achievements', 'list completed achievements'],
    ['ach | achievements -a, --all', 'list all achievements'],
    ['<trade_index> *<args>', 'trade numbers!'],
    ['save', 'save current state of the game (this is done automatically on "exit" and "quit")'],
    ['sell *<trade_ids>', 'give away the chosen trades and get from 1 to 2 random numbers for each of them'],
    ['bargain *<args>', f'give away {N_FOR_BARGAIN} unique numbers to get one random trade'],
    ['missing', 'print out missing numbers'],
]

RULES_STR = f'''
Welcome to the Number Hunter --- the game about collecting numbers!
The goal is to collect all integers from 0 to {N-1} by trading.
On launch, you are shown your inventary: numbers and trades.
Numbers are the main currency here (nerd alert!). They are listed separated by commas: <number>(<amount>).
Trades are main way to change one numbers for anothers. Each trade consists of a payment and a return type.
A payment is a number of slots with conditions. To trade successfully, provide a suitable number for each of these slots (order matters!).
    For example, [Prime, Even] is a payment which needs one prime and one even number. 
    To read more about different payment slot types, type 'payments'.
A return type indicates what number(s) you get upon completing the trade.
    For example, DOUBLE will get all of your submitted numbers doubled.
    Depending on the difficulty of the payment, a trade can have multiplied returns (indicated by "<multiplier>* next to the return type"). \
        This is equivalent to having traded this trade <multiplier> times.  
    To read more about different return types, type 'returns'.
'''

class App:
    def menu(self):
        print('Menu')
        self.running_menu = True
        while self.running_menu:
            inp = input(': ')
            match inp.split():
                case ['help']:
                    print()
                    for command, info in HELP_STR_MENU:
                        print(f'{command:<10}\t\t{info}')
                case ['rules']:
                    print(RULES_STR)
                case ['payments']:
                    for pmt, help_str in HELP_PAYMENTS.items():
                        print(f'{pmt.__name__:<15}    {help_str}')
                case ['returns']:
                    for rt, help_str in HELP_RETURN_TYPES.items():
                        print(f'{rt.name:<15}    {help_str}')
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
                        try:
                            self.save_name = self.game_files[int(game_ind_str)]
                        except ValueError:
                            print(f'{game_ind_str} is not an integer')
                            continue
                        except IndexError:
                            print(f'There is no save with index {game_ind_str}')
                            continue
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
                multiplier_str = f'{pure_trade.multiplier}*' if pure_trade.multiplier > 1 else '  '
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
                print()
                for command, info in HELP_STR:
                    print(f'{command:<20}\t\t{info}')
            case ['rules']:
                print(RULES_STR)
            case ['payments']:
                for pmt, help_str in HELP_PAYMENTS.items():
                    print(f'{pmt.__name__:<15}    {help_str}')
            case ['returns']:
                for rt, help_str in HELP_RETURN_TYPES.items():
                    print(f'{rt.name:<15}    {help_str}')
            case ['exit', *flags]:
                self.running = False
                if '-d' in flags or '--discard' in flags:
                    print('Discarded save')
                    return
                elif flags:
                    print('Unknown flag(s):', flags)
                self.save_game()
            case ['quit']:
                self.running = False
                self.running_menu = False
                self.save_game()
            case ['info']:
                print(self.g.info)
                print(f'You\'ve traded {self.g.times_traded} times')
            case ['save']:
                self.save_game()
            case ['ach' | 'achievements']:
                if not self.g.achievements:
                    print('no achievements')
                    return
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
            case ['missing']:
                print('Missing numbers:', end=' ')
                for num, amount in self.g.numbers.items():
                    if not amount:
                        print(num, end=' ')
                print()
            case ['sell', *trades_ids_str]:
                if len(self.g.achievements) < 2:
                    print('Complete at least 2 achievements first!')
                    return
                if not trades_ids_str:
                    print('No trades provided')
                    return
                try:
                    trades_ids = list(map(int, trades_ids_str))
                except ValueError:
                    print('Some of the values you entered are not numbers')
                    return
                try:
                    returns = self.g.sell(trades_ids)
                except CustomException as e:
                    print(e)
                    return
                print(f'You sold the trade(s) and received: {returns}')
                self.alert_new_achievements()
            case ['bargain', *args_str]:
                if len(self.g.achievements) < 2:
                    print('Complete at least 2 achievements first!')
                    return
                try:
                    args = list(map(int, args_str))
                except ValueError:
                    print('Some of the values you entered are not numbers')
                    return
                try:
                    received_trade = self.g.bargain(args)
                except CustomException as e:
                    print(e)
                    return
                print(f'Bargain successful! You received: {received_trade}')
                self.alert_new_achievements()
            case [trade_index_str, *args_str]:
                # trade!
                try:
                    trade_index = int(trade_index_str)
                except ValueError:
                    print(f'Unknown command: {trade_index_str}; try "help"')
                    return
                try:
                    args = list(map(int, args_str))
                    returns, gifted_trade = self.g.trade(trade_index, args)
                except ValueError:
                    print('Some of the values you entered are not numbers')
                    return
                except CustomException as e:
                    print(e)
                    return
                add = f' and new trade "{gifted_trade}".' if gifted_trade else '.'
                print(f'You received: {returns}{add}')
                self.alert_new_achievements()

    def run(self):
        self.running = True
        print(f'Started game {self.gi.save_name} from {datetime.fromtimestamp(self.gi.date_created_timestamp)}')
        if self.g.is_victory(): print('You won this game!')
        self.execute_command('inv')
        self.alert_new_achievements()
        while self.running:
            inp = input('>>> ')
            self.execute_command(inp)
        
        if self.g.is_victory():
            print('You won!')

    def save_game(self):
        with open(os.path.join(SAVES_DIR, self.save_name), 'wb') as f:
            pickle.dump(self.g, f)
        print('Saved')
