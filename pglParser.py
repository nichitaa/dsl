import json
import sys
from lark import Lark, Transformer, tree, v_args
import matplotlib.pyplot as plt

# Import instructions
from instructions.arrayInstr import ArrayInstruction
from instructions.fileInputInstr import FileInputInstruction
from instructions.plotInstr import PlotInstruction
from instructions.subplotInst import SubplotInstruction


class TreeToDSL(Transformer):
    array = list
    number = v_args(inline=True)(float)
    true = lambda self, _: True
    false = lambda self, _: False


class Parser:
    def __init__(self, pgl_filename, grammar_filename):
        self._code = open(pgl_filename, "r").read()
        self._grammar = open(grammar_filename, "r").read()

        self.parser = Lark(self._grammar,
                           parser='lalr',
                           lexer='standard',
                           propagate_positions=False,
                           maybe_placeholders=False,
                           transformer=TreeToDSL())

        self.parse_tree = self.parser.parse(self._code)

        self.variables = {}  # variables like arrays and strings here
        self.instructions = []

    def makeDot(self):
        filepath = sys.argv[0] + ".dot"
        tree.pydot__tree_to_dot(self.parser.parse(self._code), filepath)

    def define_instruction(self, instruction_tree):
        instruction = instruction_tree.children[0].data
        children = instruction_tree.children[0].children

        if instruction == 'subplot_assign':
            self.instructions.append(SubplotInstruction(children, self.variables))

        elif instruction == 'plot_assign':
            self.instructions.append(PlotInstruction(children, self.variables))

        elif instruction == 'arr_assign':
            self.instructions.append(ArrayInstruction(children, self.variables))

        elif instruction == 'input_assign':
            self.instructions.append(FileInputInstruction(children, self.variables))

        # todo: handle errors
        else:
            return

    def run(self):
        for instruction_tree in self.parse_tree.children:
            self.define_instruction(instruction_tree)

        for instruction in self.instructions:
            instruction.execute()

        plt.tight_layout()
        plt.show()  # uncomment this to see the plots
        # print(json.dumps(self.plt_vars, indent=4))
