from instructions.instruction import Instruction


class PrintInstruction(Instruction):
    def __init__(self, instruction_data, variables):
        super().__init__(instruction_data, variables)
        arr_name = instruction_data[0].value
        # arr_value = instruction_data[1]

        if '"' in arr_name or "'" in arr_name:
            print(arr_name.strip("\"").strip("\'"))
        else:
            print(variables[arr_name])
        # variables[arr_name] = arr_value

    def execute(self):
        return
