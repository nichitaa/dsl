from instructions.instruction import Instruction
from consts.consts import *


class SubplotInstruction(Instruction, dict):
    def __init__(self, instruction_data, variables):
        super(SubplotInstruction, self).__init__(instruction_data, variables)
        self.styles = {}
        self.variables = variables
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

        if param_type == TYPES:
            plt_type = p[0].children[0].data
            super().__setitem__(TYPE, plt_type)

        elif param_type == X_AXIS:
            data = values[0]
            super().__setitem__(X_AXIS, data)

        elif param_type == Y_AXIS:
            data = values[0]
            super().__setitem__(Y_AXIS, data)

        elif param_type == PLOT_STYLES:
            styles = values
            self.set_styles(styles, name)

        elif param_type == HIST_DATA:
            self.set_hist_data(values[0])

        elif param_type == PIE_LABELS:
            self.set_pie_labels(values[0])

        elif param_type == PIE_DIVISIONS:
            self.set_pie_divisions(values[0])

        elif param_type == PIE_AUTOPCT:
            self.set_pie_autopct(values[0])

        elif param_type == DATE_ORIGIN:
            self.set_date_arr_var(values[0], DATE_ORIGIN)

        elif param_type == DATE_DATA:
            self.set_date_arr_var(values[0], DATE_DATA)

        elif param_type == DATE_STRPTIME:
            self.set_date_str_var(values[0], DATE_STRPTIME)

        elif param_type == DATE_FORMATTER:
            self.set_date_str_var(values[0], DATE_FORMATTER)

        else:
            return

    def set_date_str_var(self, data, name):
        tok = data
        tok_type = data.type
        if tok_type == NAME:
            str_var_name = data.value
            str_var_value = self.get_variable(str_var_name)
            self[name] = str_var_value
        else:
            self[name] = str(tok[1:-1])

    def set_date_arr_var(self, data, name):
        self[name] = []
        if type(data) == list:
            for i in data:
                self[name].append(str(i[1:-1]))
        # variable reference
        else:
            arr_var_name = data.value
            arr_var_value = self.get_variable(arr_var_name)
            self[name] = arr_var_value

    def set_pie_autopct(self, data):
        if data.type == 'STRING':
            self[PIE_AUTOPCT] = data[1:-1]
        elif data.type == NAME:
            self[PIE_AUTOPCT] = self.get_variable(data.value)

    def set_pie_divisions(self, data):
        self[PIE_DIVISIONS] = []
        if type(data) == list:
            for i in data:
                self[PIE_DIVISIONS].append(float(i.value))
        # variable reference
        else:
            arr_var_name = data.value
            arr_var_value = self.get_variable(arr_var_name)
            self[PIE_DIVISIONS] = arr_var_value

    def set_pie_labels(self, data):
        self[PIE_LABELS] = []
        if type(data) == list:
            for i in data:
                self[PIE_LABELS].append(str(i[1:-1]))
        # variable reference
        else:
            arr_var_name = data.value
            arr_var_value = self.get_variable(arr_var_name)
            self[PIE_LABELS] = arr_var_value

    def set_hist_data(self, data):
        self[HIST_DATA] = []
        for i in range(len(data)):
            tok_type = data[i].type
            tok_value = data[i].value
            if tok_type == NAME:
                arr_var_name = tok_value
                arr_var_value = self.get_variable(arr_var_name)
                self[HIST_DATA].append(arr_var_value)

    def set_styles(self, styles, name):
        super().__setitem__(STYLES, {})
        self.styles = super().__getitem__(STYLES)
        for s in styles:
            style_type = s.children[0].data
            if style_type == COLOR:
                c = s.children[0].children[0].data
                self.styles[COLOR] = c

            elif style_type == LABEL:
                tok = s.children[0].children[0].value
                tok_type = s.children[0].children[0].type
                if tok_type == NAME:
                    str_var_name = s.children[0].children[0].value
                    str_var_value = self.get_variable(str_var_name)
                    self.styles[LABEL] = str_var_value
                else:
                    self.styles[LABEL] = str(tok[1:-1])

            elif style_type == LINE_STYLE:
                ls = s.children[0].children[0].value
                self.styles[LINE_STYLE] = str(ls[1:-1])

            elif style_type == MARKER:
                m = s.children[0].children[0].value
                self.styles[MARKER] = str(m[1:-1])

            elif style_type == LINE_WIDTH:
                lw = s.children[0].children[0]
                self.styles[LINE_WIDTH] = int(lw)

            elif style_type == THEME:
                tok = s.children[0].children[0].value
                tok_type = s.children[0].children[0].type
                if tok_type == NAME:
                    str_var_name = s.children[0].children[0].value
                    str_var_value = self.get_variable(str_var_name)
                    self.styles[THEME] = str_var_value
                else:
                    self.styles[THEME] = str(tok[1:-1])

            elif style_type == ALPHA:
                tok = s.children[0].children[0].value
                self.styles[ALPHA] = float(tok)

            elif style_type == SIZE:
                tok = s.children[0].children[0].value
                self.styles[SIZE] = float(tok)

            elif style_type == ORIENTATION:
                tok = s.children[0].children[0].data
                self.styles[ORIENTATION] = str(tok)
                # print(tok)

            elif style_type == BINS:
                tok = s.children[0].children[0].value
                self.styles[BINS] = int(tok)
                # print(tok)

            else:
                return

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            raise Exception(f'undeclared variable name {name}')