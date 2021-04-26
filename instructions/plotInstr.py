from instructions.subplotInst import SubplotInstruction
import json
from Plots.SimplePlot import SimplePlot
from Plots.Histogram import Histogram
from Plots.Pie import Pie
from Plots.Date import Date
from consts.consts import *


class PlotInstruction(SubplotInstruction):
    def __init__(self, instruction_data, variables):
        super().__init__(instruction_data, variables)
        self.plot_name = instruction_data[0].value
        self.plot_value = instruction_data[1]
        self.plot_params = self.plot_value.children

        for param in self.plot_params:
            self.plot_param(param.children, self.plot_name)

        variables[self.plot_name] = self
        # self.variables = variables

    def execute(self):
        # get general plot data
        plot_name = self.plot_name
        plot_data = self.variables[self.plot_name]
        plot_type = plot_data[TYPE]

        # split damn plots by TYPE
        if plot_type == SIMPLE or plot_type == SCATTER:
            # new simple plot object
            simple = SimplePlot(plot_name, plot_data, self.variables)
            # update plt. reference to it
            simple.show()
            # or use like so and in __init__ call self.show()
            # SimplePlot(plot_name, plot_data, self.variables)
            # or can be even added to an array to keep track of them
            # but I dont see this need for now
        elif plot_type == HISTOGRAM:
            hist = Histogram(plot_name, plot_data, self.variables)
            hist.show()

        elif plot_type == PIE:
            pie = Pie(plot_name, plot_data, self.variables)
            pie.show()

        elif plot_type == DATE:
            date = Date(plot_name, plot_data, self.variables)
            date.show()

    def plot_param(self, p, name):
        param_type = p[0].data
        values = p[0].children
        self.subplot_param(p, name)
        if param_type == SUBPLOTS:
            subplots_arr = []
            self.__setitem__(SUBPLOTS, subplots_arr)

            for s in values:
                subplots_arr.append(s.value)
        elif param_type == LEGEND:
            self.set_legend(values, name)

        elif param_type == CONFIG:
            self.set_config(values, name)
        else:
            return

    def set_config(self, config, name):
        config_dict = {}
        self.__setitem__(CONFIG, config_dict)
        for c in config:
            config_key = c.children[0].data
            config_val = c.children[0].children[0]
            if config_key == SAVE:
                config_val = config_val[1:-1]
            config_dict[config_key] = config_val

    def set_legend(self, legend, name):
        legend_dict = {}
        self.__setitem__(LEGEND, legend_dict)
        for legend_param in legend:
            legend_param_type = legend_param.children[0].data
            if legend_param_type == X_LABEL or legend_param_type == Y_LABEL:
                label_value = legend_param.children[0].children[0].value
                legend_dict[legend_param_type] = str(label_value[1:-1])

            elif legend_param_type == TITLE:
                tok = legend_param.children[0].children[0].value
                tok_type = legend_param.children[0].children[0].type
                if tok_type == NAME:
                    str_var_value = self.get_variable(tok)
                    legend_dict[TITLE] = str_var_value
                else:
                    legend_dict[TITLE] = str(tok[1:-1])

            elif legend_param_type == LOC:
                loc = legend_param.children[0].children[0].value
                legend_dict[LOC] = str(loc[1:-1])

            elif legend_param_type == SHADOW:
                shadow = legend_param.children[0].children[0]
                legend_dict[SHADOW] = bool(shadow)

            elif legend_param_type == LEGEND_TITLE:
                tok = legend_param.children[0].children[0].value
                tok_type = legend_param.children[0].children[0].type
                if tok_type == NAME:
                    str_var_value = self.get_variable(tok)
                    legend_dict[LEGEND_TITLE] = str_var_value
                else:
                    legend_dict[LEGEND_TITLE] = str(tok[1:-1])

            elif legend_param_type == LEGEND_LABEL_COLOR:
                legend_label_color = legend_param.children[0].children[0].data
                legend_dict[LEGEND_LABEL_COLOR] = legend_label_color

            else:
                raise Exception(f"Not a valid legend argument! {legend_param_type}")

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            raise Exception(f'undeclared variable name {name}')