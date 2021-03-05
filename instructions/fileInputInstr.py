import os
from instructions.instruction import Instruction
from consts.consts import *


class FileInputInstruction(Instruction):
    def __init__(self, instruction_data, variables):
        super().__init__(instruction_data, variables)
        arr_name = instruction_data[0].value
        filename = instruction_data[1].strip('"')
        var_type = STRING
        if len(instruction_data) > 2:
            var_type = instruction_data[2].data

        var = []
        if arr_name in variables:
            var = variables[arr_name]
        else:
            variables[arr_name] = var

        int_lambda = lambda var: int(var)
        float_lambda = lambda var: float(var)
        bool_lambda = lambda var: bool(var)
        str_lambda = lambda var: var

        lamb = str_lambda
        if var_type == INT:
            lamb = int_lambda
        elif var_type == FLOAT:
            lamb = float_lambda
        elif var_type == BOOL:
            lamb = bool_lambda

        try:
            stream = open(os.path.join('./test/', filename), "r")
            for line in stream:
                var.append(lamb(line))

        except IOError:
            raise Exception(f'Cannot open file: {filename}')

    def execute(self):
        return
