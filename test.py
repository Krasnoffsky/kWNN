import random
import numpy as np
from csv import reader
from matplotlib import pyplot as plt


def data_reader(filename):
    with open(filename, newline='') as row:
        return list(reader(row, delimiter=','))


def euclideRange(a, b):
    x = abs(b[0] - a[0]) * 100 / 14
    y = abs(b[1] - a[1]) * 100 / 25000
    c = (x ** 2 + y ** 2) ** 0.5

    return c


def sort(learningData, learningSize, u, k):
    def swap(i, j):
        learningData[i], learningData[j] = learningData[j], learningData[i]

    min_i = 0

    for i in range(k):
        min_i = i
        for j in range(i + 1, learningSize):
            if euclideRange(learningData[j], u) < euclideRange(learningData[min_i], u):
                min_i = j
        if i != min_i:
            swap(i, min_i)

def findQ(learningData, learningSize, k, q):

    miss = 0

    for i in range(learningSize):
        sort(learningData, learningSize, learningData[i], k + 1)

        weightRed = 0
        weightGreen = 0

        for j in range(1, k + 1):
            if learningData[j][2] == 0:
                weightRed = weightRed + q ** (j + 1)
            elif learningData[j][2] == 1:
                weightGreen = weightGreen + q ** (j + 1)

        if weightRed > weightGreen and learningData[i][2] == 1:
            miss = miss + 1

        elif weightGreen > weightRed and learningData[i][2] == 0:
            miss = miss + 1

    return miss


def kWNN(learningData, learningSize, testData, testSize, k, q):

    miss = 0

    for i in range(testSize):
        sort(learningData, learningSize, testData[i], k)

        weightRed = 0
        weightGreen = 0

        for j in range(k):
            if learningData[j][2] == 0:
                weightRed = weightRed + q ** (j + 1)
            elif learningData[j][2] == 1:
                weightGreen = weightGreen + q ** (j + 1)

        if weightRed > weightGreen:
            testData[i][2] = 0

        elif weightGreen > weightRed:
            testData[i][2] = 1

    return miss


def main():
    filename = "data4.csv"
    x_cords_red = []
    y_cords_red = []
    x_cords_green = []
    y_cords_green = []

    data = data_reader(filename)
    data.pop(0)

    k = 9
    dataSize = 1000
    testSize = int(dataSize / 3)
    learningSize = dataSize - testSize

    learningData = []
    testData = []
    randomRed = []
    randomGreen = []

    for i in range(dataSize):
        data[i][0] = int(data[i][0])
        data[i][1] = int(data[i][1])
        data[i][2] = int(data[i][2])

        testData.append(data[i])

        if data[i][2] == 0:
            randomRed.append(data[i])
        else:
            randomGreen.append(data[i])


    f_color = 0

    for i in range(learningSize):
        if (len(randomGreen) == 0):
            index = random.randint(0, len(randomRed) - 1)
            learningData.append(randomRed[index])
            testData.remove(randomRed[index])
            randomRed.pop(index)
        elif i % 2 == 0:
            index = random.randint(0, len(randomRed) - 1)
            learningData.append(randomRed[index])
            testData.remove(randomRed[index])
            randomRed.pop(index)
        else:
            index = random.randint(0, len(randomGreen) - 1)
            learningData.append(randomGreen[index])
            testData.remove(randomGreen[index])
            randomGreen.pop(index)

    miss = []

    for q in np.arange(0.9, 0.0, -0.1):
        miss.append(findQ(learningData, learningSize, k, q) * 100 / dataSize)

    min_miss = 0

    for i in range(1, len(miss)):
        if miss[i] < miss[min_miss]:
            min_miss = i

    q = 0.9 - 0.1 * min_miss

    kWNN(learningData, learningSize, testData, testSize, k, q)

    for i in range(len(miss)):
        print(miss[i])

    xLabel = "q = " + str(q) + " miss = " + str(miss[min_miss]) + "%"

    for i in range(learningSize):
        if learningData[i][2] == 0:
            x_cords_red.append(learningData[i][0])
            y_cords_red.append(learningData[i][1])
        else:
            x_cords_green.append(learningData[i][0])
            y_cords_green.append(learningData[i][1])

    for i in range(testSize):
        if testData[i][2] == 0:
            x_cords_red.append(testData[i][0])
            y_cords_red.append(testData[i][1])
        else:
            x_cords_green.append(testData[i][0])
            y_cords_green.append(testData[i][1])

    plt.scatter(x_cords_red, y_cords_red, c="red", s=5)
    plt.scatter(x_cords_green, y_cords_green, c="green", s=5)

    plt.xlabel(xLabel)

    plt.show()

    return 0


if __name__ == '__main__':
    main()
