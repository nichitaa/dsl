from pglParser import Parser


def run(pgl_filename):
    parser = Parser(pgl_filename)
    parser.makeDot()
    parser.run()


if __name__ == '__main__':
    # run("demo/hist.pgl")
    # run("demo/simple.pgl")
    # run("demo/demo.pgl")
    run("demo/pie.pgl")


