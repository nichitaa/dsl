from instructions.subplotInst import SubplotInstruction
import matplotlib.pyplot as plt


class PlotInstruction(SubplotInstruction):
    def __init__(self, instruction_data, variables):
        super().__init__(instruction_data, variables)
        self.plt_vars = {}
        self.plot_name = instruction_data[0].value
        self.plot_value = instruction_data[1]
        self.plot_params = self.plot_value.children
        self.plt_vars[self.plot_name] = {'plot': True}
        for param in self.plot_params:
            self.plot_param(param.children, self.plot_name)

        variables[self.plot_name] = self
        self.variables = variables

    def execute(self):
        # get plot data
        plot_data = self.plt_vars[self.plot_name]
        _subplots = plot_data['subplots']
        x, y = self.get_xy(plot_data)
        c, l, ls, m, lw = self.get_styles(plot_data)
        theme = self.get_plot_theme(plot_data)
        plot_type = self.get_plot_type(plot_data)
        plot_title, x_label, y_label, loc, shadow, legend_title, legend_label_color = self.get_legend(plot_data)

        # set theme
        if theme is not None:
            plt.style.use(theme)

        # create subplots
        fig, axs = plt.subplots(len(_subplots) + 1)

        # plot main plot first
        axs[0].plot(x, y, color=c, linestyle=ls, marker=m, linewidth=lw, label=l)

        for i in range(len(_subplots)):
            # if the subplot data exists in global dict
            if _subplots[i] in self.variables:
                plt_vars = self.variables[_subplots[i]].plt_vars
                subplot_data = plt_vars[_subplots[i]]
                x, y = self.get_xy(subplot_data)
                c, l, ls, m, lw = self.get_styles(subplot_data)
                subplot_type = self.get_plot_type(subplot_data)
                """if subplot_type !== main_plot_type => they are not compatible"""
                if subplot_type != plot_type:
                    raise Exception(
                        f"The subplot `{_subplots[i]}` must be of type: `{plot_type}` (not `{subplot_type}`)!")
                # plot the subplot data
                axs[i + 1].plot(x, y, color=c, linestyle=ls, marker=m, linewidth=lw, label=l)
                # plt.grid(True)

            # the subplot is not defined
            else:
                raise Exception(f"The subplot: `{_subplots[i]}` is not defined!")

        # plot title
        fig.suptitle(plot_title)
        # plt.grid(True)
        # legend
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        fig.legend(
            loc=loc,
            shadow=shadow,
            fontsize='small',
            title=legend_title,
            framealpha=1,
            frameon=True,
            labelcolor=legend_label_color,
        )
        # plt.show(block=False)


    def plot_param(self, p, name):
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
            self.set_styles(values, name)
        elif param_type == 'legend':
            self.set_legend(values, name)
        elif param_type == 'config':
            self.set_config(values, name)
        elif param_type == 'subplots':
            self.set_subplots(values, name)
        else:
            return

    def set_subplots(self, subplots, name):
        self.plt_vars[name]['subplots'] = []
        for s in subplots:
            self.plt_vars[name]['subplots'].append(s.value)

    def set_config(self, config, name):
        self.plt_vars[name]['config'] = {}
        for c in config:
            config_key = c.children[0].data
            config_val = c.children[0].children[0]
            if config_key == 'save':
                config_val = config_val[1:-1]
            self.plt_vars[name]['config'][config_key] = config_val

    def set_legend(self, legend, name):
        self.plt_vars[name]['legend'] = {}
        for legend_param in legend:
            legend_param_type = legend_param.children[0].data
            if legend_param_type == 'x_label' or legend_param_type == 'y_label':
                label_value = legend_param.children[0].children[0].value
                self.set_legend_label(legend_param_type, label_value, name)

            elif legend_param_type == 'title':
                title = legend_param.children[0].children[0].value
                self.set_plot_title(title, name)

            elif legend_param_type == 'loc':
                loc = legend_param.children[0].children[0].value
                self.set_legend_loc(loc, name)

            elif legend_param_type == 'shadow':
                shadow = legend_param.children[0].children[0]
                self.set_legend_shadow(shadow, name)

            elif legend_param_type == 'legend_title':
                legend_title = legend_param.children[0].children[0]
                self.set_legend_title(legend_title, name)

            elif legend_param_type == 'legend_label_color':
                legend_label_color = legend_param.children[0].children[0].data
                self.set_legend_label_color(legend_label_color, name)

            else:
                raise Exception(f"Not a valid legend argument! {legend_param_type}")

    def set_plot_title(self, title, name):
        self.plt_vars[name]['legend']['legend_title'] = str(title[1:-1])

    def set_legend_title(self, title, name):
        self.plt_vars[name]['legend']['title'] = str(title[1:-1])

    def set_legend_shadow(self, shadow, name):
        self.plt_vars[name]['legend']['shadow'] = bool(shadow)

    def set_legend_loc(self, loc, name):
        self.plt_vars[name]['legend']['loc'] = str(loc[1:-1])

    def set_legend_label(self, axis, value, name):
        self.plt_vars[name]['legend'][axis] = str(value[1:-1])

    def set_legend_label_color(self, color, name):
        self.plt_vars[name]['legend']['legend_label_color'] = color


    def get_array_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            # undefined variable error
            raise Exception(f'Undefined array: {name}')

    def get_xy(self, d):
        x, y = [], []
        if type(d['x_axis']) == list:
            x = d['x_axis']

        if type(d['x_axis']) != list:
            x = self.get_array_variable(d['x_axis'])

        if type(d['y_axis']) == list:
            y = d['y_axis']

        if type(d['y_axis']) != list:
            y = self.get_array_variable(d['y_axis'])
        return x, y

    @staticmethod
    def get_plot_type(d):
        return d['type']

    @staticmethod
    def get_legend(d):
        x_label = d['legend'].get('x_label')
        y_label = d['legend'].get('y_label')
        title = d['legend'].get('title')
        loc = d['legend'].get('loc')
        shadow = d['legend'].get('shadow')
        legend_title = d['legend'].get('legend_title')
        label_color = d['legend'].get('legend_label_color')
        return title, x_label, y_label, loc, shadow, legend_title, label_color

    @staticmethod
    def get_styles(d):
        c = d['styles'].get('color')
        l = d['styles'].get('label')
        ls = d['styles'].get('line_style')
        m = d['styles'].get('marker')
        lw = d['styles'].get('line_width')
        return c, l, ls, m, lw

    @staticmethod
    def get_plot_theme(d):
        return d['styles'].get('theme')