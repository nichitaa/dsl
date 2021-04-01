import json
import os
from lark import Lark, Transformer, tree, v_args
import matplotlib.pyplot as plt
from consts.consts import *

# Import instructions
from instructions.arrayInstr import ArrayInstruction
from instructions.fileInputInstr import FileInputInstruction
from instructions.plotInstr import PlotInstruction
from instructions.subplotInst import SubplotInstruction
from instructions.stringInstr import StringInstruction
from instructions.printInstruction import PrintInstruction


class TreeToDSL(Transformer):
    array = list
    number = v_args(inline=True)(float)
    true = lambda self, _: True
    false = lambda self, _: False


def get_grammar():
    instructions = open('grammar/instruction.lark', 'r').read()
    variables = open('grammar/variables.lark', 'r').read()
    plot = open('./grammar/plot.lark', 'r').read()
    styles = open('./grammar/styles.lark', 'r').read()
    legend = open('./grammar/legend.lark', 'r').read()
    config = open('./grammar/config.lark', 'r').read()
    common = open('grammar/common.lark', 'r').read()
    grammar = instructions + variables + plot + styles + legend + config + common
    return grammar


class Parser:
    def __init__(self, pgl_filename):
        self._code = open(pgl_filename, "r").read()
        self._grammar = get_grammar()

        self.parser = Lark(self._grammar,
                           parser='lalr',
                           lexer='standard',
                           propagate_positions=False,
                           maybe_placeholders=False,
                           transformer=TreeToDSL())

        self.parse_tree = self.parser.parse(self._code)

        self.plt_vars = {}  # plots data here
        self.variables = {}  # variables like arrays and strings here
        self.instructions = []
        self.instruction_dict = {SUBPLOT_ASSIGN: SubplotInstruction, PLOT_ASSIGN: PlotInstruction,
                                 ARR_ASSIGN: ArrayInstruction, INPUT_ASSIGN: FileInputInstruction,
                                 STR_ASSIGN: StringInstruction, PRINT_ASSIGN: PrintInstruction}

    def makeDot(self):
        tree.pydot__tree_to_dot(self.parser.parse(self._code), os.path.join('./parseTree/', "parseTree.dot"))

    def define_instruction(self, instruction_tree):
        instruction = instruction_tree.children[0].data
        children = instruction_tree.children[0].children
        if instruction in self.instruction_dict:
            self.instructions.append(self.instruction_dict[instruction](children, self.variables))

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
