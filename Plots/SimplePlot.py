import matplotlib.pyplot as plt


class SimplePlot:
    def __init__(self, name, data, variables):
        self.name = name
        self.data = data
        self.variables = variables

    def show(self):
        # ONLY simple plot configs here

        # data tb plotted
        x, y = self.get_xy(self.data)

        # styles
        c, l, ls, m, lw = self.get_styles(self.data)
        theme = self.get_theme()
        plot_title, x_label, y_label, loc, shadow, legend_title, legend_label_color = self.get_legend()

        # subplots
        subplots = self.get_subplots()

        # actual plot
        plt.style.use(theme)

        # create new figure
        if len(subplots) > 0:
            fig, axs = plt.subplots(len(subplots) + 1)
            axs[0].plot(x, y, color=c, linestyle=ls, marker=m, linewidth=lw, label=l)
        else:
            fig, axs = plt.subplots(1)
            axs.plot(x, y, color=c, linestyle=ls, marker=m, linewidth=lw, label=l)

        # only if subplots exists
        for i in range(len(subplots)):
            # if the subplot data exists in global dict
            if subplots[i] in self.variables:
                subplot_data = self.variables[subplots[i]]
                x, y = self.get_xy(subplot_data)
                c, l, ls, m, lw = self.get_styles(subplot_data)
                subplot_type = self.variables[subplots[i]]['type']
                """if subplot_type !== main_plot_type => they are not compatible"""
                if subplot_type != 'simple':
                    raise Exception(
                        f"The subplot `{subplots[i]}` must be of type: `{'simple'}` (not `{subplot_type}`)!")
                # plot the subplot data
                axs[i + 1].plot(x, y, color=c, linestyle=ls, marker=m, linewidth=lw, label=l)
                plt.grid(True)

            # the subplot is not defined
            else:
                raise Exception(f"The subplot: `{subplots[i]}` is not defined!")

        # # plot title
        fig.suptitle(plot_title)
        plt.grid(True)
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

    def get_subplots(self):
        subplots = self.data.get('subplots', [])
        return subplots

    def get_legend(self):
        x_label = self.data['legend'].get('x_label', 'DEFAULT X LABEL')
        y_label = self.data['legend'].get('y_label', 'DEFAULT Y LABEL')
        title = self.data['legend'].get('title', 'DEFAULT TITLE')
        loc = self.data['legend'].get('loc', 'upper left')
        shadow = self.data['legend'].get('shadow', True)
        legend_title = self.data['legend'].get('legend_title', 'DEFAULT LEGEND')
        label_color = self.data['legend'].get('legend_label_color', 'blue')
        return title, x_label, y_label, loc, shadow, legend_title, label_color

    def get_theme(self):
        t = self.data.get('theme', 'ggplot')
        return t

    def get_styles(self, data):
        c = data['styles'].get('color', 'red')
        l = data['styles'].get('label', 'DEFAULT LABEL')
        ls = data['styles'].get('line_style', '--')
        m = data['styles'].get('marker', '*')
        lw = data['styles'].get('line_width', 1)
        return c, l, ls, m, lw

    def get_xy(self, data):
        x, y = [], []
        x_val = data['x_axis']
        y_val = data['y_axis']

        if type(x_val) == list:
            x = x_val
        else:
            x = self.get_array_variable(x_val)

        if type(y_val) == list:
            y = y_val
        else:
            y = self.get_array_variable(y_val)
        return x, y

    def get_array_variable(self, var_name):
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            # undefined variable error
            raise Exception(f'Undefined array: {var_name}')
