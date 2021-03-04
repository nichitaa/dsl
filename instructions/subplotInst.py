from instructions.instruction import Instruction


class SubplotInstruction(Instruction, dict):
    def __init__(self, instruction_data, variables):
        super(SubplotInstruction, self).__init__(instruction_data, variables)
        self.styles = {}
        subplot_name = instruction_data[0].value
        subplot_value = instruction_data[1]
        subplot_params = subplot_value.children
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
            super().__setitem__('type', plt_type)
        elif param_type == 'x_axis':
            data = values[0]
            super().__setitem__('x_axis', data)
        elif param_type == 'y_axis':
            data = values[0]
            super().__setitem__('y_axis', data)
        elif param_type == 'plot_styles':
            styles = values
            self.set_styles(styles, name)
        else:
            return

    def set_styles(self, styles, name):
        super().__setitem__('styles', {})
        self.styles = super().__getitem__('styles')
        for s in styles:
            style_type = s.children[0].data
            if style_type == 'color':
                c = s.children[0].children[0].data
                self.styles['color'] = c

            elif style_type == 'label':
                l = s.children[0].children[0].value
                self.styles['label'] = str(l[1:-1])

            elif style_type == 'line_style':
                ls = s.children[0].children[0].value
                self.styles['line_style'] = str(ls[1:-1])

            elif style_type == 'marker':
                m = s.children[0].children[0].value
                self.styles['marker'] = str(m[1:-1])

            elif style_type == 'line_width':
                lw = s.children[0].children[0]
                self.styles['line_width'] = int(lw)

            elif style_type == 'theme':
                t = s.children[0].children[0].value
                self.styles['theme'] = str(t[1:-1])
            else:
                return

