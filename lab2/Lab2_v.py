import math
import random
import sys
import matplotlib.pyplot as plt

PI = math.pi
PHASE = PI / 4
AMPLITUDE = 10
STEP = PI / 200
MAX_LENGTH = 1000


class Sequence:
    sequence = []
    timeSequence = []
    simpleMA = []
    weightedMA = []
    exponentialMA = []
    modifiedMA = []
    length = 0

    def init(self, length):
        timeValue = 0
        self.length = length
        self.simpleMA = [0] * length
        self.weightedMA = [0] * length
        index = 0

        while index < length:
            deviation = random.uniform(-0.01 * AMPLITUDE, 0.01 * AMPLITUDE)
            value = AMPLITUDE * (math.sin(PI * 2 * timeValue + PHASE) + deviation)
            self.timeSequence.append(timeValue + PHASE)
            self.sequence.append(value)
            timeValue += STEP
            index += 1

            # def findArithmeticA(self):

    #     elemSum = 0
    #     for elem in self.sequence:
    #         elemSum += elem

    #     return elemSum / self.length

    # def findHarmonicA(self):
    #     reversedSum = 0
    #     for elem in self.sequence:
    #         reversedSum += 1 / elem

    #     return self.length / reversedSum

    # TODO: fix this method
    def findGeometricA(self):
        logSum = 0

        # using logarithm addition to multiply extra small numbers
        for elem in self.sequence:
            if elem < sys.float_info.min:
                logSum += math.log(sys.float_info.min)
            else:
                logSum += math.log(elem)

                # print("log sum ", logSum)
        # a * b = e ^ (ln a + ln b)
        elemProduct = math.pow(math.e, logSum)
        # print(elemPrнеoduct)
        return math.pow(elemProduct, 1 / self.length)

    def findSimpleMA(self, ):

        i = 0
        j = 10
        while i < (self.length - 10):
            sum = 0
            k = 0
            while k < j:
                sum += self.sequence[i + k]
                k += 1
            self.simpleMA[i] = sum / (10)

            i += 1

    def findWeightedMA(self):
        i = 0
        while i < (self.length - 10):
            j = 10
            sum = 0
            k = 0
            while k < j:
                sum += self.sequence[i - k + 9] * (j - k)
                k += 1
            self.weightedMA[i] = 2 * sum / (j * (j + 1))
            i += 1

    def findExponentialMA(self):
        ALPHA = 0.3
        i = 1
        temp = self.sequence[0]
        self.exponentialMA.append(temp)
        while i < self.length:
            newtemp = (ALPHA * self.sequence[i]) + ((1 - ALPHA) * temp)
            self.exponentialMA.append(newtemp)
            temp = newtemp
            i += 1

    def findModifiedMA(self):
        i = 1
        j = 5
        temp = self.sequence[0]
        self.modifiedMA.append(temp)
        while i < self.length:
            newtemp = (self.sequence[i] + (j - 1) * temp) / j
            self.modifiedMA.append(newtemp)
            temp = newtemp
            i += 1


def main():
    mySequence = Sequence(MAX_LENGTH)
    print("Sequence: ", mySequence.sequence)

    mySequence.findSimpleMA()
    print("SimpleMA:", mySequence.simpleMA)

    mySequence.findWeightedMA()
    print("WeightedMA: ", mySequence.weightedMA)

    mySequence.findExponentialMA()
    print("ExpMA: ", mySequence.exponentialMA)

    mySequence.findModifiedMA()
    print("modifiedMA: ", mySequence.modifiedMA)

    plt.plot(mySequence.sequence, 'b--',
             mySequence.simpleMA, 'r-',
             mySequence.weightedMA, 'g-',
             mySequence.exponentialMA, 'y-',
             mySequence.modifiedMA, 'b-')
    plt.xlim(0, 400)
    plt.show()


main()