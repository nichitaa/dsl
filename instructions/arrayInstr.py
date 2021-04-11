from instructions.instruction import Instruction


class ArrayInstruction(Instruction):
    def __init__(self, instruction_data, variables):
        super().__init__(instruction_data, variables)
        arr_name = instruction_data[0].value
        arr_value = instruction_data[1]
        arr = []
        for value in arr_value:
            if "\"" in value or "\'" in value:
                arr.append(str(value[1:-1]))
            else:
                arr.append(float(value))
        variables[arr_name] = arr

    def execute(self):
        return
