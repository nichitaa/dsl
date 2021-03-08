import matplotlib.pyplot as plt
from consts.consts import *


class Histogram:
    def __init__(self, name, data, variables):
        self.name = name
        self.data = data
        self.variables = variables

    def show(self):
        """HISTOGRAM"""
        plt_type = self.data[TYPE]
        hist_data = self.get_hist_data(self.data)
        alpha, bins, orientation = self.get_styles(self.data)
        plot_title, x_label, y_label, loc, shadow, legend_title, legend_label_color = self.get_legend()
        theme = self.get_theme()

        plt.style.use(theme)

        # subplots
        subplots = self.get_subplots()

        args = dict(bins=bins, orientation=orientation, alpha=alpha)

        # create new figure
        if len(subplots) > 0:
            fig, axs = plt.subplots(len(subplots) + 1)
            axs[0].hist(hist_data, **args)
        else:
            fix, axs = plt.subplots(1)
            axs.hist(hist_data, **args)

        # only if subplots exists
        for i in range(len(subplots)):
            # if the subplot data exists in global dict
            if subplots[i] in self.variables:
                subplot_name = subplots[i]
                subplot_data = self.variables[subplot_name]
                hist_subplot_data = self.get_hist_data(subplot_data)
                subplot_alpha, subplot_bins, subplot_orientation = self.get_styles(subplot_data)
                subplot_args = dict(bins=subplot_bins, orientation=subplot_orientation, alpha=subplot_alpha)
                axs[i + 1].hist(hist_subplot_data, **subplot_args)
                plt.grid(True)

            # the subplot is not defined
            else:
                raise Exception(f"The subplot: `{subplots[i]}` is not defined!")

        # plot title
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

        plt.show()

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
        alpha = data[STYLES].get(ALPHA, 1)
        bins = data[STYLES].get(BINS, 10)
        orientation = data[STYLES].get(ORIENTATION, 'horizontal')
        return alpha, bins, orientation

    def get_hist_data(self, data):
        hist_data = data.get(HIST_DATA, [])
        return hist_data

    def get_array_variable(self, var_name):
        pass
