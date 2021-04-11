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
        print("PLOT THIS DATA")
        print(json.dumps(self.data, indent=4))
        # plot here


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
