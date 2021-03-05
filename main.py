from pglParser import Parser


def run(pgl_filename, grammar_filename):
    parser = Parser(pgl_filename, grammar_filename)
    parser.makeDot()
    parser.run()


if __name__ == '__main__':
    run("demo/simple.pgl", "grammar.lark")
