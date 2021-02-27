import sys
import json
import matplotlib.pyplot as plt
from lark import Lark, Transformer, tree, v_args


# set some defaults terminals instead of plain strings
class TreeToDSL(Transformer):
    array = list
    number = v_args(inline=True)(float)
    true = lambda self, _: True
    false = lambda self, _: False


class Parser:

    def __init__(self, program):
        # actual dsl code
        self._program = program
        # get grammar rules
        self._grammar = self.getGrammar("grammar.txt")
        self.parser = Lark(self._grammar,
                           parser='lalr',
                           lexer='standard',
                           propagate_positions=False,
                           maybe_placeholders=False,
                           transformer=TreeToDSL())
        self.parse_tree = self.parser.parse(self._program)
        self.plt_vars = {}

    @staticmethod
    def getGrammar(filename):
        grammar = open(filename, "r").read()
        return grammar

    def makeDot(self):
        filepath = sys.argv[0] + ".dot"
        tree.pydot__tree_to_dot(self.parser.parse(self._program), filepath)

    def run_assignment(self, t):
        if t.children[0].data == 'subplot_assign':
            self.subplot_assign(t.children[0].children)

        elif t.children[0].data == 'plot_assign':
            self.plot_assign(t.children[0].children)

    #########################################################################
    #                                   PLOT                                #
    #########################################################################

    def plot_assign(self, plot):
        plot_name = plot[0].value
        plot_value = plot[1]
        plot_params = plot_value.children
        self.plt_vars[plot_name] = {'plot': True}
        for param in plot_params:
            self.plot_param(param.children, plot_name)

    def plot_param(self, p, name):
        param_type = p[0].data
        values = p[0].children
        if param_type == 'types':
            plt_type = p[0].children[0].data
            self.set_plot_type(plt_type, name)
        elif param_type == 'x_axis':
            data = values[0]
            self.x_axis(data, name)
        elif param_type == 'y_axis':
            data = values[0]
            self.y_axis(data, name)
        elif param_type == 'plot_styles':
            self.plot_styles(values, name)
        elif param_type == 'legend':
            self.plot_legend(values, name)
        elif param_type == 'config':
            self.plot_config(values, name)
        elif param_type == 'subplots':
            self.plot_set_subplots(values, name)
        else:
            return

    def plot_set_subplots(self, subplots, name):
        self.plt_vars[name]['subplots'] = []
        for s in subplots:
            self.plt_vars[name]['subplots'].append(s.value)

    def plot_config(self, config, name):
        self.plt_vars[name]['config'] = {}
        for c in config:
            config_key = c.children[0].data
            config_val = c.children[0].children[0]
            if config_key == 'save':
                config_val = config_val[1:-1]
            self.plt_vars[name]['config'][config_key] = config_val

    def plot_legend(self, legend, name):
        self.plt_vars[name]['legend'] = {}
        for legend_param in legend:
            legend_param_type = legend_param.children[0].data
            if legend_param_type == 'x_label' or legend_param_type == 'y_label':
                label_value = legend_param.children[0].children[0].value
                self.plot_legend_label(legend_param_type, label_value, name)

            elif legend_param_type == 'title':
                title = legend_param.children[0].children[0].value
                self.plot_legend_title(title, name)

            elif legend_param_type == 'loc':
                loc = legend_param.children[0].children[0].value
                self.plot_legend_loc(loc, name)

            elif legend_param_type == 'shadow':
                shadow = legend_param.children[0].children[0]
                self.plot_legend_shadow(shadow, name)

    def plot_legend_shadow(self, shadow, name):
        self.plt_vars[name]['legend']['shadow'] = bool(shadow)

    def plot_legend_loc(self, loc, name):
        self.plt_vars[name]['legend']['loc'] = str(loc[1:-1])

    def plot_legend_title(self, title, name):
        self.plt_vars[name]['legend']['title'] = str(title[1:-1])

    def plot_legend_label(self, axis, value, name):
        self.plt_vars[name]['legend'][axis] = str(value[1:-1])

    #########################################################################
    #                                SUBPLOT                                #
    #########################################################################

    def subplot_assign(self, subplot):
        subplot_name = subplot[0].value
        subplot_value = subplot[1]
        subplot_params = subplot_value.children
        self.plt_vars[subplot_name] = {'subplot': True}
        for param in subplot_params:
            self.subplot_param(param.children, subplot_name)

    def subplot_param(self, p, name):
        param_type = p[0].data
        values = p[0].children
        if param_type == 'types':
            plt_type = p[0].children[0].data
            self.set_plot_type(plt_type, name)
        elif param_type == 'x_axis':
            data = values[0]
            self.x_axis(data, name)
        elif param_type == 'y_axis':
            data = values[0]
            self.y_axis(data, name)
        elif param_type == 'plot_styles':
            styles = values
            self.plot_styles(styles, name)
        else:
            return

    #########################################################################
    #                               COMMON                                  #
    #########################################################################

    def plot_styles(self, styles, name):
        self.plt_vars[name]['styles'] = {}
        for s in styles:
            style_type = s.children[0].data
            if style_type == 'color':
                c = s.children[0].children[0].data
                self.color(c, name)

            elif style_type == 'label':
                l = s.children[0].children[0].value
                self.label(l, name)

            elif style_type == 'line_style':
                ls = s.children[0].children[0].value
                self.line_style(ls, name)

            elif style_type == 'marker':
                m = s.children[0].children[0].value
                self.marker(m, name)

            elif style_type == 'line_width':
                lw = s.children[0].children[0]
                self.line_width(lw, name)

            elif style_type == 'theme':
                pass

            else:
                return

    def line_width(self, lw, name):
        self.plt_vars[name]['styles']['line_width'] = int(lw)

    def line_style(self, s, name):
        self.plt_vars[name]['styles']['line_style'] = str(s[1:-1])

    def marker(self, m, name):
        self.plt_vars[name]['styles']['marker'] = str(m[1:-1])

    def label(self, l, name):
        self.plt_vars[name]['styles']['label'] = str(l[1:-1])

    def color(self, c, name):
        self.plt_vars[name]['styles']['color'] = c

    def y_axis(self, data, name):
        self.plt_vars[name]['y_axis'] = data

    def x_axis(self, data, name):
        self.plt_vars[name]['x_axis'] = data

    def set_plot_type(self, type, name):
        self.plt_vars[name]['type'] = type

    ##################################################################
    #                 MATPLOTLIB CODE WILL BE HERE                   #
    ##################################################################

    # todo: clean and split this shit up and find a better logic!

    def plt_simple(self, plt_params):
        subplots = []
        if 'subplot' in plt_params:
            subplot = True
        elif 'plot' in plt_params:
            subplot = False
            if 'subplots' in plt_params:
                subplots = plt_params['subplots']
            if 'legend' in plt_params:
                legend_x = plt_params['legend']['x_label']
                legend_y = plt_params['legend']['x_label']
                title = plt_params['legend']['title']
                loc = plt_params['legend']['loc']
                shadow = plt_params['legend']['shadow']

        gx = plt_params['x_axis']
        gy = plt_params['y_axis']
        gc = plt_params['styles']['color']
        glabel = plt_params['styles']['label']
        gl_style = plt_params['styles']['line_style']
        gm = plt_params['styles']['marker']
        gl_width = plt_params['styles']['line_width']
        # fig = plt.figure()
        # todo: return figure instance or some plot ref idk


        # just to see if values are getting applied
        if len(subplots) > 0:
            for subplot in subplots:
                if subplot in self.plt_vars:
                    subplot = self.plt_vars[subplot]
                    x = subplot['x_axis']
                    y = subplot['y_axis']
                    c = subplot['styles']['color']
                    label = subplot['styles']['label']
                    l_style = subplot['styles']['line_style']
                    m = subplot['styles']['marker']
                    l_width = subplot['styles']['line_width']
                    plt.plot(x, y, color=c, linestyle=l_style, marker=m, linewidth=l_width, label=label)
                    plt.plot(gx, gy, color=gc, linestyle=gl_style, marker=gm, linewidth=gl_width, label=glabel)
                    plt.xlabel(legend_x)
                    plt.ylabel(legend_y)
                    plt.title(title)
                    plt.legend()
                    plt.grid(True)
                    plt.tight_layout()
        plt.show()

    def plt_type(self, plt_type, plt_params):
        # print(plt_type)
        # print(plt_params)
        if plt_type == 'simple':
            self.plt_simple(plt_params)

    def run(self):
        for instruction in self.parse_tree.children:
            self.run_assignment(instruction)

        for key, val in self.plt_vars.items():
            plot_ref = key
            plot_params = val
            for param_type, param in plot_params.items():
                if param_type == 'type':
                    self.plt_type(param, val)

        print(json.dumps(self.plt_vars, indent=4))


def test():
    program = open("demo.txt", "r").read()
    # print(program)
    parser = Parser(program)
    parser.makeDot()
    parser.run()


if __name__ == '__main__':
    test()
