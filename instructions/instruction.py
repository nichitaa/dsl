from abc import abstractmethod


class VirtualException(BaseException):
    def __init__(self, _type, _func):
        BaseException(self)


class Instruction:
    @abstractmethod
    def __init__(self, instruction_data, variables):
        pass

    @abstractmethod
    def execute(self):
        pass
