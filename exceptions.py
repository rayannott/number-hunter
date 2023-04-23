class CustomException(Exception):
    pass

class WrongNumberOfArguments(CustomException):
    pass

class InvalidPayment(CustomException):
    pass

class EmptyTradeM(CustomException):
    pass

class NotEnoughNumbers(CustomException):
    pass

class NumberOutOfRange(CustomException):
    pass

class NumbersNotUnique(CustomException):
    pass

class BargainWrongNumberOfArgs(CustomException):
    pass

class InvalidTradeIndex(CustomException):
    pass

class TooManyTradingIndices(CustomException):
    pass

# TODO: add more exceptions so that nothing crushes
