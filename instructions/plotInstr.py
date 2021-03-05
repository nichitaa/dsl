from instructions.subplotInst import SubplotInstruction
import matplotlib.pyplot as plt


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
        # get plot data
        plot_data = self.variables[self.plot_name]
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
        axs[0].plot(x, y, color=c, linestyle=ls, marker=m, linewidth=lw, label=l) #change type here

        for i in range(len(_subplots)):
            # if the subplot data exists in global dict
            if _subplots[i] in self.variables:
                subplot_data = self.variables[_subplots[i]]
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
        self.subplot_param(p,name)
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

    def get_array_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            # undefined variable error
            raise Exception(f'Undefined array: {name}')

    def get_xy(self, d):
        x, y = [], []
        x_val = d['x_axis']
        y_val = d['y_axis']

        if type(x_val) == list:
            x = x_val
        else:
            x = self.get_array_variable(x_val)

        if type(y_val) == list:
            y = y_val
        else:
            y = self.get_array_variable(y_val)
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
