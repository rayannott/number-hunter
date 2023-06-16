import os
import pickle
from datetime import datetime

from utils import SAVES_DIR, GameInfo, N_FOR_BARGAIN, N_FOR_MEGA_BARGAIN, N, TRADES_BOUND
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
    ['payments', 'describe each payment option'],
    ['returns', 'describe each return type'],
    ['info', 'print out the current game\'s info and stats'],
    ['exit', 'save; go back to menu'],
    ['exit -d, --discard', 'do not save; go back to menu'],
    ['quit', 'save; quit the program'],
    ['inv | +', 'list your inventary: numbers and trades'],
    ['ach | achievements', 'list completed achievements'],
    ['ach | achievements -a, --all', 'list all achievements'],
    ['<trade_index> *<args>', 'trade numbers!'],
    ['save', 'save current state of the game (this is done automatically on \'exit\' and \'quit\')'],
    ['sell *<trade_ids>', 'give away the chosen trades and get from 1 to 2 random numbers for each of them'],
    ['bargain *<args>', f'give away {N_FOR_BARGAIN} unique numbers to get one random trade or {N_FOR_MEGA_BARGAIN} to get to choose one trade from 4 random trades'],
    ['missing', 'print out missing numbers'],
]
 
RULES_STR = f'''
Welcome to the Number Hunter --- the game about collecting numbers!
The goal is to collect all integers from 0 to {N-1} by trading.
On launch, you are shown your inventary: numbers and trades.
Numbers are the main currency here (nerd alert!). They are listed separated by commas: <number>(<amount>).
Trades are main way to change one numbers for anothers. Number of active trades is bounded by ({TRADES_BOUND} + <number of completed achievements>).\
 Each trade consists of a payment and a return type.
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
        print('--- Menu ---')
        self.running_menu = True
        while self.running_menu:
            inp = input(': ')
            self.execute_command_menu(inp.split())
            
    def execute_command_menu(self, cmds: list[str]):
        match cmds:
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
            case ['new', *args]:
                name = None
                init_trades = 10; init_nums = 10
                if not args:
                    self.gi = GameInfo()
                else:
                    for arg in args:
                        if '=' not in arg:
                            name = arg
                        else:
                            param, value = arg.split('=')
                            if param == '--trades':
                                try:
                                    init_trades = int(value)
                                except ValueError:
                                    print(f'Not an integer: {value}')
                                    return
                            elif param == '--nums':
                                try:
                                    init_nums = int(value)
                                except ValueError:
                                    print(f'Not an integer: {value}')
                                    return
                            else:
                                print('Unknown parameter:', param)
                if name is not None:
                    self.gi = GameInfo(name + '.pi', init_nums=init_nums, init_trades=init_trades)
                else:
                    self.gi = GameInfo(init_nums=init_nums, init_trades=init_trades)
                self.save_name = self.gi.save_name
                self.g = Game(self.gi)
                self.run()
            case ['load']:
                if not os.path.exists(SAVES_DIR):
                    os.mkdir(SAVES_DIR)
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
                    return
                try:
                    self.save_name = self.game_files[int(game_ind_str)]
                except ValueError:
                    print(f'{game_ind_str} is not an integer')
                    return
                except IndexError:
                    print(f'There is no save with index {game_ind_str}')
                    return
                with open(os.path.join(SAVES_DIR, self.save_name), 'rb') as f:
                    self.g: Game = pickle.load(f) # TODO: does not load
                    self.gi = self.g.info
                self.run()
            case ['exit' | 'quit']:
                self.running_menu = False
            case _:
                print(f'Unknown command sequence: {cmds}')

    def display_nums(self):
        print(', '.join(f'{num:>2}({amount})' for num, amount in self.g.numbers.items() if amount))

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
                print(ach.describe())

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
            case ['exit' | 'quit', *flags]:
                self.running = False
                if cmds[0] == 'quit':
                    self.running_menu = False
                if '-d' in flags or '--discard' in flags:
                    print('Discarded save')
                    return
                elif flags:
                    print('Unknown flag(s):', flags)
                self.save_game()
            case ['info']:
                print(self.g.info)
                print(f'Traded in total: {self.g.times_traded} times')
                print(f'Number of active trades: {self.g.num_active_trade_indices()}/{TRADES_BOUND + len(self.g.achievements)}')
                print('Sum of all numbers (incl. duplicates):', self.g.sum_of_all_numbers())
            case ['test']:
                pass
            case ['save']:
                self.save_game()
            case ['ach' | 'achievements']:
                if not self.g.achievements:
                    print('no achievements')
                    return
                print(f'*** Completed achievements ({len(self.g.achievements)}/{len(ACHIEVEMENTS)}) ***')
                for ach in self.g.achievements:
                    print(ach.describe())
            case ['ach' | 'achievements', flag]:
                if not flag in ['-a', '--all']:
                    print(f'{flag} is an unknown flag')
                    return
                print('--- All achievements ---')
                for ach in ACHIEVEMENTS:
                    posession_str = '+' if ach in self.g.achievements else '-'
                    print(f'[{posession_str}] {ach.describe()}')     
            case ['inv' | '+']:
                self.display_nums()
                print()
                self.display_trades()
            case ['missing']:
                if self.g.is_victory():
                    print('No missing numbers')
                    return
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
                    received_trades = self.g.bargain(args)
                except CustomException as e:
                    print(e)
                    return
                if len(received_trades) == 1:
                    print(f'Bargain successful! You received: {received_trades[0]}')
                    self.g.my_trades.append(received_trades[0])
                else:
                    print('Choose a trade to take by index:')
                    for i, tr in enumerate(received_trades):
                        print(f'{i}.  {tr}')
                    successful = False
                    while not successful:
                        chosen_index_str = input('Your choice: ')
                        try:
                            chosen_trade = received_trades[int(chosen_index_str)]
                        except ValueError:
                            print(f'{chosen_index_str} is not an integer')
                        except IndexError:
                            print(f'There is no offer with index {chosen_index_str}')
                        else:
                            successful = True
                            print(f'Bargain successful! You received: {chosen_trade}')
                            self.g.my_trades.append(chosen_trade)
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
        if not self.g.shown_you_won_message and self.g.is_victory():
            print('----- You won! ------')
            self.g.shown_you_won_message = True
            self.g.victory = True
            for ach in ACHIEVEMENTS:
                ach.activate()
            for ach in self.g.achievements:
                ach.activate()
        self.alert_new_achievements()

    def run(self):
        self.running = True
        print(f'Started game {self.gi}')
        if self.g.is_victory(): print('You won this game!')
        self.execute_command('inv')
        while self.running:
            inp = input('>>> ')
            self.execute_command(inp)   

    def save_game(self):
        if not os.path.exists(SAVES_DIR):
            os.mkdir(SAVES_DIR)
        with open(os.path.join(SAVES_DIR, self.save_name), 'wb') as f:
            pickle.dump(self.g, f)
        print('Saved')
