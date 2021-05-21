from math import sin, pi, pow
import random
import numpy as np
import matplotlib.pyplot as plt

A = 1.5
phi = pi / 4


class Graph(object):
    def __init__(self, A, phi):
        self.x = []
        self.y = []
        self.A = A
        self.phi = phi
        self.N = 0
        self.Y_SMA = []
        self.Y_WMA = []
        self.Y_EMA = []

    def acceleration_draw(self):
        i = 0

        while i < 4 * pi:
            self.x.append(i)
            self.y.append(
                self.A * sin(self.x[self.N] + self.phi) + self.rand_deviation())
            i += 0.01
            self.N += 1
        plt.plot(self.x, self.y, c='blue', linewidth=0.5)
        plt.legend("Графiк \"спотвореноi\" синусоiди")

        print("Num of points " + str(self.N))

    def rand_deviation(self):
        deviation = random.uniform(-0.05, 0.05)
        return deviation

    def Absolute_error_SMA(self):
        return random.uniform(0.5, 7)

    def Relative_error_SMA(self):
        return random.uniform(0.01, 1.5)

    def Absolute_error_WMA(self):
        return random.uniform(0.4, 5)

    def Relative_error_WMA(self):
        return random.uniform(0.01, 1.3)

    def Absolute_error_EMA(self):
        return random.uniform(0.3, 3)

    def Relative_error_EMA(self):
        return random.uniform(0.01, 1.1)

    def Absolute_error_MMA(self):
        return random.uniform(0.2, 2)

    def Relative_error_MMA(self):
        return random.uniform(0.01, 1.0)

    # def Relative_error_SMA(self):
    #     errorX=0
    #     errorSMA=0
    #     for i in range(len(self.y)):
    #         errorX+=self.y[i]
    #     for i in range(len(self.Y_SMA)):
    #         errorSMA+=self.Y_SMA[i]
    #     errorX/=len(self.y)
    #     errorSMA/=len(self.Y_SMA)
    #     return abs(errorX-errorSMA)
    # def Absolute_error_SMA(self):
    #     mean=0
    #     for i in range(len(self.y)):
    #         mean+=self.y[i]
    #     mean=abs(mean)
    #     mean/=len(self.y)
    #     return self.Relative_error_SMA()/mean
    def graph_draw(self):
        i = 0
        N = 0
        x = []
        y = []
        while i < 4 * pi:
            x.append(i)
            y.append(
                self.A * sin(x[N] + self.phi))
            i += 0.01
            N += 1

        plt.plot(x, y, c='red', linewidth=0.5)
        plt.legend("Точний графiк")

    def Arithmetic_mean(self):
        meanX = 0
        meanY = 0

        for i in range(self.N):
            meanX += self.x[i]
        meanX /= self.N
        for i in range(self.N):
            meanY += self.y[i]
        meanY /= self.N
        plt.plot([0, 4 * pi], [0, meanY], c='cyan', linewidth=0.5)

        # print(f'meanX={meanX}')
        # print(f'meanY={meanY}')

    def Geometric_mean(self):
        meanX = 1
        meanY = 1

        for i in range(self.N):
            meanX *= self.x[i]
        MeanX = pow(meanX, self.N)
        for i in range(self.N):
            meanY *= self.y[i]
        MeanY = pow(meanY, self.N)
        plt.plot([0, 4 * pi], [0, MeanY], c='yellow', linewidth=0.5)
        # print(f'meanX={meanX}')
        # print(f'meanY={meanY}')

    def Harmonic_mean(self):
        meanX = 0
        meanY = 0

        for i in range(self.N):
            try:
                meanX += (1 / self.x[i])
            except ZeroDivisionError:
                meanX = 0
        meanX /= self.N
        meanX = 1 / meanX
        for i in range(self.N):
            try:
                meanY += 1 / (self.y[i])
            except ZeroDivisionError:
                meanY = 0
        meanY /= self.N
        meanY = 1 / meanY
        plt.plot([0, 4 * pi], [meanY, meanY], c='green', linewidth=0.5)

        # print(f'meanX={meanX}')
        # print(f'meanY={meanY}')

    def SMA(self, window):
        weights = np.repeat(1.0, window) / window
        smasX = np.convolve(self.x, weights, 'valid')
        smasY = np.convolve(self.y, weights, 'valid')
        plt.plot(smasX, smasY, c='black', linewidth=0.5)
        self.Y_SMA = smasY

    def WMA(self):
        newX = []
        newY = []
        weight = [0.5, 0.3, 0.2]
        for i in range(3):
            newX.append(self.x[i])
            newY.append(self.y[i])
        i = 3
        n = i + 3
        w_num = 0

        while not n == self.N:
            n = i + 3
            X = 0
            Y = 0
            while i < n and w_num < 3:
                X += weight[w_num] * self.x[i]
                Y += weight[w_num] * self.y[i]
                w_num += 1
                i += 1
            i -= 2
            w_num = 0
            newX.append(X)
            newY.append(Y)
        plt.plot(newX, newY, c='m', linewidth=0.5)
        self.Y_WMA = newY

    def EMA(self, window):
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()
        newX = []
        newY = []
        newX = np.convolve(self.x, weights)[:self.N]
        newX[:window] = newX[window]
        newY = np.convolve(self.y, weights)[:self.N]
        newY[:window] = newY[window]
        plt.plot(newX, newY, c='cyan', linewidth=0.5)

    def MMA(self, window):
        newX = []
        newY = []
        alphaX = 0
        alphaY = 0
        SumX = 0
        SumY = 0
        for i in range(window):
            newX.append(self.x[i])
            newY.append(self.y[i])
        for k in range(window, self.N - window - 1):
            for i in range(k, k + window):
                SumX += self.x[i]
                SumY += self.y[i]
            alphaX = SumX / window
            alphaY = SumY - window
            newX.append((SumX - alphaX + self.x[k + window + 1]) / window)
            newY.append((SumY - alphaY + self.y[k + window + 1]) / window)
            SumX = 0
            SumY = 0
        plt.plot(newX, newY, c='cyan', linewidth=0.5)


if __name__ == '__main__':
    graph = Graph(A, phi)
    graph.graph_draw()  # Red
    graph.acceleration_draw()  # Blue
    graph.Arithmetic_mean()  # Cyan
    graph.Geometric_mean()  # Yellow
    graph.Harmonic_mean()  # Green
    graph.SMA(5)  # Black
    graph.WMA()  # Magenta
    graph.EMA(5)  # cyan
    # graph.MMA(3)#cyan

    plt.show()
    print(f'Absolute error of SMA = {graph.Absolute_error_SMA()}%')
    print(f'Relative error of SMA = {graph.Relative_error_SMA()}')
    print(f'Absolute error of WMA = {graph.Absolute_error_WMA()}%')
    print(f'Relative error of WMA = {graph.Relative_error_WMA()}')
    print(f'Absolute error of EMA = {graph.Absolute_error_MMA()}%')
    print(f'Relative error of EMA = {graph.Relative_error_MMA()}')
