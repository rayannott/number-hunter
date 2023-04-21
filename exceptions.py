class CustomException(Exception):
    pass

class ConditionFailedException(CustomException):
    pass

class WrongNumberOfArguments(CustomException):
    pass

class InvalidPayment(CustomException):
    pass

class EmptyTradeM(CustomException):
    pass

class NotEnoughNumbers(CustomException):
    pass

# TODO: add more exceptions so that nothing crushes
