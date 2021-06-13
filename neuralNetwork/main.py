import sys
import os
import random
import image_database
import image_filter
import visualizer

sys.path.append("/usr/lib/python3.9/site-packages")
import numpy as np


class Network:

    def __init__(self, setup, name="", learn_factor=0.1):
        self.setup = [x + 1 for x in setup]
        self.size = len(self.setup)
        self.name = name
        self.class_names = []
        self.learn_factor = learn_factor

        self.values = [np.zeros(i) for i in self.setup]
        self.derivative = [np.zeros(i) if i > 0 else None for i in self.setup]
        self.layers = [np.random.uniform(-1, 1, (self.setup[i - 1], self.setup[i]))
                       if i > 0 else None for i in range(len(self.setup))]

    def class_name_to_answer(self, class_name):
        for i in range(len(self.class_names)):
            if class_name == self.class_names[i]:
                return i
        return -1

    def answer_to_class_name(self, answer):
        return self.class_names[answer]

    def calculate(self, values):
        values.append(1)
        self.values[0] = np.array(values)

        for i in range(1, len(self.setup)):
            self.values[i - 1][len(self.values[i - 1]) - 1] = 1
            self.values[i] = self.values[i - 1].dot(self.layers[i])
            self.values[i] = 1 / (1 + np.exp(- self.values[i]))

    def cost(self, right_answer):
        answers = self.values[self.size - 1]
        size = len(answers) - 1
        result = 0
        for i in range(size):
            if i == right_answer:
                result += (1 / size) * ((1 - answers[i]) ** 2)
            else:
                result += (1 / size) * (answers[i] ** 2)
        return result

    def answer(self):
        answers = self.values[self.size - 1]
        index = 0
        maxi = 0
        for i in range(len(answers) - 1):
            if maxi < answers[i]:
                maxi = answers[i]
                index = i
        return index

    def learn(self, right_answer):
        n = self.size - 1

        for i in range(len(self.derivative[n])):
            if i == right_answer:
                self.derivative[n][i] = self.values[n][i] - 1
            else:
                self.derivative[n][i] = self.values[n][i]
            self.derivative[n][i] *= (1 - self.values[n][i]) * self.values[n][i]

            for j in range(len(self.derivative[n - 1])):
                self.layers[n][j][i] -= self.derivative[n][i] * self.values[n - 1][j] * self.learn_factor

        for step in range(n - 1, 0, -1):
            for i in range(len(self.derivative[step])):
                self.derivative[step][i] = 0
                for back in range(len(self.derivative[step + 1])):
                    self.derivative[step][i] += self.derivative[step + 1][back] * self.layers[step + 1][i][back]
                self.derivative[step][i] *= (1 - self.values[step][i]) * self.values[step][i]

                for j in range(len(self.derivative[step - 1])):
                    self.layers[step][j][i] -= self.derivative[step][i] * self.values[step - 1][j] * self.learn_factor



    def save_weights(self, add_name=""):
        file = open('weights_save' + str(self.name) + add_name + '.txt', 'w')

        for i in range(self.size):
            file.write(str(self.setup[i]) + ' ')
        file.write('\n')
        # layer 0 == None
        for layer in range(1, self.size):
            for x in range(len(self.layers[layer])):
                for y in range(len(self.layers[layer][0])):
                    file.write(str(self.layers[layer][x][y]) + '\n')
        file.close()

    def load_weights(self):
        try:
            file = open('weights_save' + str(self.name) + '.txt', 'r')
        except:
            return
        setup = file.readline().split()
        setup = [int(setup[i]) for i in range(len(setup))]

        if len(setup) == self.size:
            for i in range(len(setup)):
                if setup[i] != self.setup[i]:
                    return
        else:
            return
        # layer 0 == None
        print("LOADED")
        for layer in range(1, self.size):
            for x in range(len(self.layers[layer])):
                for y in range(len(self.layers[layer][x])):
                    self.layers[layer][x][y] = float(file.readline())
        file.close()

    def save_stats(self, string_to_save):
        file = open('stats' + str(self.name) + '.txt', 'a')
        file.write(string_to_save)
        file.write('\n')
        file.close()



input_width = 88
input_height = 88
class_names = ["car", "truck"]

first_filter = image_filter.Individual_Filter(2, 2)
first_filter.values = [[   1,   1],
                       [-0.9,-0.9]]
second_filter = image_filter.Individual_Filter(2, 2)
second_filter.values = [[1, -0.9],
                        [1, -0.9]]


set_filter = image_filter.Set_Filter([[first_filter, second_filter], [first_filter, second_filter]])


if __name__ == '__main__':
    database = image_database.Database(input_width, input_height, "train_set//", "test_set//", class_names)

    (raw_image, right_answer_name) = database.get()
    filtered_image = set_filter(raw_image)
    (width, height) = (len(filtered_image[0]), len(filtered_image))
    processed_image = database.flat_array(filtered_image, True)
    print("input: (width, height) =", (width, height))

    network = Network([width * height, 40, 2])
    network.class_names = class_names
    visualizer = visualizer.Visualizer(network)
    network.load_weights()

    age = 0
    total_train_cost = 0
    total_test_cost = 0
    total_train_success = 0
    total_test_success = 0
    best_cost = 1

    iteration = 0
    cost = 0
    success = 0

    while True:
        (raw_image, right_answer_name) = database.get()
        right_answer = network.class_name_to_answer(right_answer_name)

        filtered_image = set_filter(raw_image)
        processed_image = database.flat_array(filtered_image)
        network.calculate(processed_image)
        # without learning
        # network.learn(right_answer)

        cost += network.cost(right_answer)
        if network.answer() == right_answer:
            success += 1
        iteration += 1

        sys.stdout.write('|')
        sys.stdout.flush()

        if iteration % 1 == 0:
            print("")
            # network.save_weights()

            iteration_test = 0
            cost_test = 0
            success_test = 0

            (raw_image, right_answer_name, path) = database.check_answer(reset=True)
            right_answer = network.class_name_to_answer(right_answer_name)

            while raw_image:
                filtered_image = set_filter(raw_image)
                processed_image = database.flat_array(filtered_image)
                network.calculate(processed_image)

                cost_test += network.cost(right_answer)
                if network.answer() == right_answer:
                    success_test += 1
                iteration_test += 1

                visualizer.refresh(network, path)

                (raw_image, right_answer_name, path) = database.check_answer()
                right_answer = network.class_name_to_answer(right_answer_name)

                sys.stdout.write('|')
                sys.stdout.flush()

            age = age + iteration
            total_train_cost += cost
            total_test_cost += cost_test
            total_train_success += success
            total_test_success += success_test

            print("\nAGE:", age,\
                " *TRAIN* ",\
                "AVG COST %1.8f" % (total_train_cost / age),\
                ", AVG RATE %1.6f" % (total_train_success / age),\
                ", CUR COST %1.8f" % (cost / iteration),\
                ", CUR RATE %1.6f" % (success / iteration),\
                " *TEST* ",\
                "AVG COST %1.8f" % (total_test_cost / (age / iteration * iteration_test)),\
                ", AVG RATE %1.6f" % (total_test_success / (age / iteration * iteration_test)),\
                ", CUR COST %1.8f" % (cost_test / iteration_test),\
                ", CUR RATE %1.6f" % (success_test / iteration_test))

            network.save_stats(
                str(age) + " "
                + str(total_train_cost / age) + " "
                + str(total_train_success / age) + " "
                + str(cost / iteration) + " "
                + str(success / iteration) + " "

                + str(total_test_cost / (age / iteration * iteration_test)) + " "
                + str(total_test_success / (age / iteration * iteration_test)) + " "
                + str(cost_test / iteration_test) + " "
                + str(success_test / iteration_test) + " ")

            if cost_test / iteration_test < best_cost:
                best_cost = cost_test / iteration_test
                network.save_weights("best")

            # os.system("./plot.sh")
            iteration = 0
            cost = 0
            success = 0

    visualizer.close()
