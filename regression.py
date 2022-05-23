import numpy as np
import matplotlib.pyplot as plt
import random

class PolyRegression:
    def __init__(self):
        pass

    def getModel(self, x, y):
        return np.poly1d(np.polyfit(x, y, 3))

    def savePlot(self, name, x, y, model):
        line = np.linspace(min(x), max(x) + 10, 100)
        plt.scatter(x, y)
        plt.plot(line, model(line))
        plt.savefig(name + '.png')

    def predict(self, x, y, name):
        model = self.getModel(x, y)
        self.savePlot('fig', x, y, model)

if __name__ == '__main__':
    x = []
    y = []
    for i in range(100):
        y.append(20 + (random.random() * 10 - 5))
        x.append(i + 1)

    ml = PolyRegression()
    ml.predict(x, y, 'fig')
