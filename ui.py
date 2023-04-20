from game import Game


class App:
    def __init__(self) -> None:
        self.g = Game()
        self.running = True

    def execute_command(self, command: str):
        cmds = command.split()
        match cmds:
            case ['exit']:
                self.running = False
                self.save_game()
            case ['inv' | 'nums']:
                print(self.g.numbers)
            case ['trades']:
                print(self.g.my_trades)
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

    def save_game(self):
        pass
