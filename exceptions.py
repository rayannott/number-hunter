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

class NumbersNotUnique(CustomException):
    pass

class BargainWrongNumberOfArgs(CustomException):
    pass

class InvalidTradeIndex(CustomException):
    pass

# TODO: add more exceptions so that nothing crushes
