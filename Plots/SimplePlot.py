import matplotlib.pyplot as plt
from consts.consts import *


class SimplePlot:
    def __init__(self, name, data, variables):
        self.name = name
        self.data = data
        self.variables = variables

    def show(self):
        """ONLY SIMPLE AND SCATTER PLOTS HERE"""
        plt_type = self.data[TYPE]

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
            if plt_type == SCATTER:
                axs[0].scatter(x, y, color=c, linestyle=ls, marker=m, linewidth=lw, label=l)
            else:
                axs[0].plot(x, y, color=c, linestyle=ls, marker=m, linewidth=lw, label=l)
        else:
            fig, axs = plt.subplots(1)
            if plt_type == SCATTER:
                axs.scatter(x, y, color=c, linestyle=ls, marker=m, linewidth=lw, label=l)
            else:
                axs.plot(x, y, color=c, linestyle=ls, marker=m, linewidth=lw, label=l)

        # only if subplots exists
        for i in range(len(subplots)):
            # if the subplot data exists in global dict
            if subplots[i] in self.variables:
                subplot_data = self.variables[subplots[i]]
                subplot_name = subplots[i]
                x, y = self.get_xy(subplot_data)
                c, l, ls, m, lw = self.get_styles(subplot_data)
                subplot_type = self.variables[subplot_name][TYPE]
                # plot the subplot data
                if subplot_type == SCATTER:
                    axs[i + 1].scatter(x, y, color=c, linestyle=ls, marker=m, linewidth=lw, label=l)
                else:
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
        subplots = self.data.get(SUBPLOTS, [])
        return subplots

    def get_legend(self):
        x_label = self.data[LEGEND].get(X_LABEL, 'DEFAULT X LABEL')
        y_label = self.data[LEGEND].get(Y_LABEL, 'DEFAULT Y LABEL')
        title = self.data[LEGEND].get(TITLE, 'DEFAULT TITLE')
        loc = self.data[LEGEND].get(LOC, 'upper left')
        shadow = self.data[LEGEND].get(SHADOW, True)
        legend_title = self.data[LEGEND].get(LEGEND_TITLE, 'DEFAULT LEGEND')
        label_color = self.data[LEGEND].get(LEGEND_LABEL_COLOR, 'blue')
        return title, x_label, y_label, loc, shadow, legend_title, label_color

    def get_theme(self):
        t = self.data[STYLES].get(THEME, 'ggplot')
        return t

    def get_styles(self, data):
        c = data[STYLES].get(COLOR, 'red')
        l = data[STYLES].get(LABEL, 'DEFAULT LABEL')
        ls = data[STYLES].get(LINE_STYLE, '--')
        m = data[STYLES].get(MARKER, '*')
        lw = data[STYLES].get(LINE_WIDTH, 1)
        return c, l, ls, m, lw

    def get_xy(self, data):
        x, y = [], []
        x_val = data[X_AXIS]
        y_val = data[Y_AXIS]

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
