import json
import matplotlib.pyplot as plt
from consts.consts import *


class Pie:
    def __init__(self, name, data, variables):
        self.name = name
        self.data = data
        self.variables = variables

    def show(self):
        """PIE"""
        # print(json.dumps(self.variables, indent=4))
        # print(json.dumps(self.data, indent=4))

        plt_type = self.data[TYPE]

        pie_labels = self.get_pie_labels(self.data)
        pie_divisions = self.get_pie_divisions(self.data)
        pie_autopct = self.get_pie_autopct(self.data)

        plot_title, x_label, y_label, loc, shadow, legend_title, legend_label_color = self.get_legend()
        theme = self.get_theme()

        plt.style.use(theme)

        # subplots
        subplots = self.get_subplots()

        args = dict(x=pie_divisions, labels=pie_labels, autopct=pie_autopct, shadow=True)

        # create new figure
        if len(subplots) > 0:
            fig, axs = plt.subplots(len(subplots) + 1)
            axs[0].pie(**args)
        else:
            fig, axs = plt.subplots(1)
            axs.pie(**args)

        # only if subplots exists
        for i in range(len(subplots)):
            # if the subplot data exists in global dict
            if subplots[i] in self.variables:
                subplot_name = subplots[i]
                subplot_data = self.variables[subplot_name]
                subplot_pie_labels = self.get_pie_labels(subplot_data)
                subplot_pie_divisions = self.get_pie_divisions(subplot_data)
                subplot_pie_autopct = self.get_pie_autopct(subplot_data)
                subplot_args = dict(x=subplot_pie_divisions,
                                    labels=subplot_pie_labels,
                                    autopct=subplot_pie_autopct,
                                    shadow=True)
                axs[i + 1].pie(**subplot_args)
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

    @staticmethod
    def get_pie_labels(data):
        return data.get(PIE_LABELS, [])

    @staticmethod
    def get_pie_divisions(data):
        return data.get(PIE_DIVISIONS, [])

    @staticmethod
    def get_pie_autopct(data):
        return data.get(PIE_AUTOPCT, "%1.2f%%")

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

    def get_array_variable(self, var_name):
        pass
