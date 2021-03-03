from instructions.instruction import Instruction


class ArrayInstruction(Instruction):
    def __init__(self, instruction_data, variables):
        super().__init__(instruction_data, variables)
        arr_name = instruction_data[0].value
        arr_value = instruction_data[1]
        variables[arr_name] = arr_value

    def execute(self):
        return
