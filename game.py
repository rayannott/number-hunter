class Game:
    def __init__(self, N: int) -> None:
        '''
        :param N: number of integers to collect (from 1 to N)
        '''
        self.numbers = {i: 0 for i in range(1, N+1)}
        self.operations = []

    def is_victory(self):
        return all(self.numbers.values())

    def execute(self, operation, args):
        pass

    def buy(self, operation, args):
        pass

    