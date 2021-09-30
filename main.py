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


def kWNN(learningData, learningSize, testData, testSize, k):

    q = 0.999
    q_control = True

    while(q_control):
        for i in range(testSize):
            sort(learningData, learningSize, testData[i], k)

            weightRed = 0
            weightGreen = 0

            for j in range(k):
                if learningData[j][2] == "Red":
                    weightRed = weightRed + q ** (j + 1)
                elif learningData[j][2] == "Green":
                    weightGreen = weightGreen + q ** (j + 1)

            if weightRed > weightGreen and testData[i][2] == 1:
                q_control = False
                break

            elif weightGreen > weightRed and testData[i][2] == 0:
                q_control = False
                break

            if q_control:
                q = q - 0.001

            if q < 0:
                print("FATAL ERROR")
                break

    return q + 0.001


def main():
    filename = "data4.csv"
    x_cords_red = []
    y_cords_red = []
    x_cords_green = []
    y_cords_green = []

    data = data_reader(filename)
    data.pop(0)

    k = 9
    dataSize = len(data)
    learningSize = int(dataSize / 3)
    testSize = dataSize - learningSize

    for i in range(dataSize):
        data[i][0] = int(data[i][0])
        data[i][1] = int(data[i][1])
        if data[i][2] == '0':
            data[i][2] = "Red"
        else:
            data[i][2] = "Green"

    learningData = []
    testData = []

    for i in range(learningSize):
        learningData.append(data[i])

    for i in range(learningSize, dataSize):
        testData.append(data[i])

    q = kWNN(learningData, learningSize, testData, testSize, k)

    xLabel = "q = " + str(q)

    for i in range(dataSize):
        if data[i][2] == 0:
            x_cords_red.append(data[i][0])
            y_cords_red.append(data[i][1])
        else:
            x_cords_green.append(data[i][0])
            y_cords_green.append(data[i][1])

    plt.scatter(x_cords_red, y_cords_red, c="red", s=5)
    plt.scatter(x_cords_green, y_cords_green, c="green", s=5)

    plt.xlabel(xLabel)

    plt.show()

    return 0


if __name__ == '__main__':
    main()
