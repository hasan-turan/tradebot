from abc import ABCMeta, abstractmethod


class Plotter():
    def __init__(self, title, plot_width, plot_height, tools, toolbar_location="above"):
        self.title = title
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.tools = tools
        self.toolbar_location = toolbar_location
        

    @abstractmethod
    def plot(self, data):
        pass
