import sys
import json
import matplotlib.pyplot as plt
from lark import Lark, Transformer, tree, v_args

from pglParser import Parser

def run(pgl_filename, grammar_filename):
    parser = Parser(pgl_filename, grammar_filename)
    #parser.makeDot()
    parser.run()


if __name__ == '__main__':
    run("demo.pgl", "grammar.lark")
