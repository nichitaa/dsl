from instructions.instruction import Instruction


class StringInstruction(Instruction):
    def __init__(self, instruction_data, variables):
        super().__init__(instruction_data, variables)
        str_var_name = instruction_data[0].value
        str_value = str(instruction_data[1][1:-1])
        variables[str_var_name] = str_value

    def execute(self):
        return
