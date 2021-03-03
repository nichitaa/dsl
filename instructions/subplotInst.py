from instructions.instruction import Instruction


class SubplotInstruction(Instruction):
    def __init__(self, instruction_data, variables):
        super().__init__(instruction_data, variables)
        self.plt_vars = {}
        subplot_name = instruction_data[0].value
        subplot_value = instruction_data[1]
        subplot_params = subplot_value.children
        self.plt_vars[subplot_name] = {'subplot': True}
        for param in subplot_params:
            self.subplot_param(param.children, subplot_name)

        variables[subplot_name] = self

    def execute(self):
        return

    def subplot_param(self, p, name):
        param_type = p[0].data
        values = p[0].children
        if param_type == 'types':
            plt_type = p[0].children[0].data
            self.set_plot_type(plt_type, name)
        elif param_type == 'x_axis':
            data = values[0]
            self.set_x_axis(data, name)
        elif param_type == 'y_axis':
            data = values[0]
            self.set_y_axis(data, name)
        elif param_type == 'plot_styles':
            styles = values
            self.set_styles(styles, name)
        else:
            return

    def set_styles(self, styles, name):
        self.plt_vars[name]['styles'] = {}
        for s in styles:
            style_type = s.children[0].data
            if style_type == 'color':
                c = s.children[0].children[0].data
                self.set_color(c, name)

            elif style_type == 'label':
                l = s.children[0].children[0].value
                self.set_label(l, name)

            elif style_type == 'line_style':
                ls = s.children[0].children[0].value
                self.set_line_style(ls, name)

            elif style_type == 'marker':
                m = s.children[0].children[0].value
                self.set_marker(m, name)

            elif style_type == 'line_width':
                lw = s.children[0].children[0]
                self.set_line_width(lw, name)

            elif style_type == 'theme':
                t = s.children[0].children[0].value
                self.set_theme(t, name)
                # pass

            else:
                return

    def set_line_width(self, lw, name):
        self.plt_vars[name]['styles']['line_width'] = int(lw)

    def set_line_style(self, s, name):
        self.plt_vars[name]['styles']['line_style'] = str(s[1:-1])

    def set_marker(self, m, name):
        self.plt_vars[name]['styles']['marker'] = str(m[1:-1])

    def set_label(self, l, name):
        self.plt_vars[name]['styles']['label'] = str(l[1:-1])

    def set_color(self, c, name):
        self.plt_vars[name]['styles']['color'] = c

    def set_theme(self, t, name):
        self.plt_vars[name]['styles']['theme'] = str(t[1:-1])

    def set_y_axis(self, data, name):
        self.plt_vars[name]['y_axis'] = data

    def set_x_axis(self, data, name):
        self.plt_vars[name]['x_axis'] = data

    def set_plot_type(self, type, name):
        self.plt_vars[name]['type'] = type
