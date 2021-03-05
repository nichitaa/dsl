from instructions.subplotInst import SubplotInstruction
import json
from Plots.SimplePlot import SimplePlot


class PlotInstruction(SubplotInstruction):
    def __init__(self, instruction_data, variables):
        super().__init__(instruction_data, variables)
        self.plot_name = instruction_data[0].value
        self.plot_value = instruction_data[1]
        self.plot_params = self.plot_value.children

        for param in self.plot_params:
            self.plot_param(param.children, self.plot_name)

        variables[self.plot_name] = self
        self.variables = variables

    def execute(self):
        # get general plot data
        plot_name = self.plot_name
        plot_data = self.variables[self.plot_name]
        plot_type = plot_data['type']

        # split damn plots by TYPE
        if plot_type == 'simple':
            # new simple plot object
            simple = SimplePlot(plot_name, plot_data, self.variables)
            # update plt. reference to it
            simple.show()
            # or use like so and in __init__ call self.show()
            # SimplePlot(plot_name, plot_data, self.variables)
            # or can be even added to an array to keep track of them
            # but I dont see this need for now

    def plot_param(self, p, name):
        param_type = p[0].data
        values = p[0].children
        self.subplot_param(p, name)
        if param_type == 'subplots':
            subplots_arr = []
            self.__setitem__('subplots', subplots_arr)

            for s in values:
                subplots_arr.append(s.value)
        elif param_type == 'legend':
            self.set_legend(values, name)

        elif param_type == 'config':
            self.set_config(values, name)
        else:
            return

    def set_config(self, config, name):
        config_dict = {}
        self.__setitem__('config', config_dict)
        for c in config:
            config_key = c.children[0].data
            config_val = c.children[0].children[0]
            if config_key == 'save':
                config_val = config_val[1:-1]
            config_dict[config_key] = config_val

    def set_legend(self, legend, name):
        legend_dict = {}
        self.__setitem__('legend', legend_dict)
        for legend_param in legend:
            legend_param_type = legend_param.children[0].data
            if legend_param_type == 'x_label' or legend_param_type == 'y_label':
                label_value = legend_param.children[0].children[0].value
                legend_dict[legend_param_type] = str(label_value[1:-1])

            elif legend_param_type == 'title':
                title = legend_param.children[0].children[0].value
                legend_dict['title'] = str(title[1:-1])

            elif legend_param_type == 'loc':
                loc = legend_param.children[0].children[0].value
                legend_dict['loc'] = str(loc[1:-1])

            elif legend_param_type == 'shadow':
                shadow = legend_param.children[0].children[0]
                legend_dict['shadow'] = bool(shadow)

            elif legend_param_type == 'legend_title':
                legend_title = legend_param.children[0].children[0]
                legend_dict['legend_title'] = str(legend_title[1:-1])

            elif legend_param_type == 'legend_label_color':
                legend_label_color = legend_param.children[0].children[0].data
                legend_dict['legend_label_color'] = legend_label_color

            else:
                raise Exception(f"Not a valid legend argument! {legend_param_type}")
