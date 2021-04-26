import json
from consts.consts import *
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime


class Date:
    def __init__(self, name, data, variables):
        self.name = name
        self.data = data
        self.variables = variables

    def show(self):
        """DATE"""
        # print(json.dumps(self.variables, indent=4))
        # print(json.dumps(self.data, indent=4))

        plt_type = self.data[TYPE]

        date_origin = self.get_date_origin(self.data)
        date_data = self.get_date_data(self.data)
        date_strptime = self.get_date_strptime(self.data)
        date_formatter = self.get_date_formatter(self.data)


        plot_title, x_label, y_label, loc, shadow, legend_title, legend_label_color = self.get_legend()
        theme = self.get_theme()

        plt.style.use(theme)

        # subplots
        subplots = self.get_subplots()


        a, x, formatter = self.make_date_general_data(date_origin, date_strptime, date_formatter)
        print(a, x, formatter)

        # create new figure
        if len(subplots) > 0:
            a, x, formatter = self.make_date_general_data(date_origin, date_strptime, date_formatter)
            fig, axs = plt.subplots(len(subplots) + 1)
            # axs[0].xaxis.set_major_formatter(formatter)
            # plt.setp(axs[0].get_xticklabels(), rotation=90)
            # axs[0].plot(axs[0], date_data)
        else:
            a, x, formatter = self.make_date_general_data(date_origin, date_strptime, date_formatter)
            fig = plt.figure()
            axes = fig.add_subplot(1, 1, 1)
            axes.xaxis.set_major_formatter(formatter)
            plt.setp(axes.get_xticklabels(), rotation=90)
            axes.plot(x, date_data)

        # # only if subplots exists
        # for i in range(len(subplots)):
        #     # if the subplot data exists in global dict
        #     if subplots[i] in self.variables:
        #         subplot_name = subplots[i]
        #         subplot_data = self.variables[subplot_name]
        #         subplot_pie_labels = self.get_pie_labels(subplot_data)
        #         subplot_pie_divisions = self.get_pie_divisions(subplot_data)
        #         subplot_pie_autopct = self.get_pie_autopct(subplot_data)
        #         subplot_args = dict(x=subplot_pie_divisions,
        #                             labels=subplot_pie_labels,
        #                             autopct=subplot_pie_autopct,
        #                             shadow=True)
        #         axs[i + 1].pie(**subplot_args)
        #         plt.grid(True)
        #
        #     # the subplot is not defined
        #     else:
        #         raise Exception(f"The subplot: `{subplots[i]}` is not defined!")
        #
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

    def make_date_general_data(self, origin, strptime, formatter):
        a = [datetime.strptime(d, strptime) for d in origin]
        x = matplotlib.dates.date2num(a)
        formatter = matplotlib.dates.DateFormatter(formatter)
        return a, x, formatter

    @staticmethod
    def get_date_origin(data):
        return data.get(DATE_ORIGIN, [])

    @staticmethod
    def get_date_data(data):
        return data.get(DATE_DATA, [])

    @staticmethod
    def get_date_strptime(data):
        return data.get(DATE_STRPTIME, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_date_formatter(data):
        return data.get(DATE_FORMATTER, "%H:%M:%S")

    def get_subplots(self):
        subplots = self.data.get(SUBPLOTS, [])
        return subplots

    def get_legend(self):
        print(self.data)
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
