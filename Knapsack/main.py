import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QComboBox, QLabel, QPushButton

class Knapsack:

    def __init__(self, capacity, weights, prices):
        self.capacity = capacity
        self.weights = weights
        self.prices = prices

    def max_val_first(self, tuples_list, k_index, v_index):
        """"
        Insertion sort for dictionary, when keys are equal put the tuple with max. value first.
        """
        j = 0
        for i in range(1, len(tuples_list)):
            key = tuples_list[i]
            j = i - 1
            while j >= 0 and key[k_index] == tuples_list[j][k_index] and key[v_index] > tuples_list[j][v_index]:
                tuples_list[j + 1] = tuples_list[j]
                j -= 1

            tuples_list[j + 1] = key

        return tuples_list

    def min_val_first(self, tuples_list, k_index, v_index):
        """"
        Insertion sort for dictionary, when keys are equal put the tuple with min. value first.
        """
        j = 0
        for i in range(1, len(tuples_list)):
            key = tuples_list[i]
            j = i - 1
            while j >= 0 and key[k_index] == tuples_list[j][k_index] and key[v_index] < tuples_list[j][v_index]:
                tuples_list[j + 1] = tuples_list[j]
                j -= 1

            tuples_list[j + 1] = key

        return tuples_list

    def max_profit_0_1(self):
        def value(val):
            return val[1]

        # sort desc. according to profit
        weights_prices = sorted(list(zip(self.weights, self.prices)), reverse=True, key=value)
        weights_prices = self.max_val_first(weights_prices, 0, 1)
        reached_capacity, profit, iterator = 0, 0, 0
        items = ""
        while reached_capacity < self.capacity:

            if weights_prices[iterator][0] <= abs(reached_capacity-self.capacity):
                profit += weights_prices[iterator][1]
                reached_capacity += weights_prices[iterator][0]
                items += "item" + str(self.prices.index(weights_prices[iterator][1])+1)+" "
            if iterator < len(self.weights)-1:
                iterator = iterator + 1

            else:
                break

        result = "Items: " + items + " Profit: " + str(profit) + " Weight: " + str(reached_capacity) + "\n"
        return result

    def min_weight_0_1(self):
        def value(val):
            return val[0]

        # sort asc. according to weight
        weights_prices = sorted(list(zip(self.weights, self.prices)), key=value)
        weights_prices = self.max_val_first(weights_prices, 0, 1)
        reached_capacity, profit, iterator = 0, 0, 0
        items = ""

        while reached_capacity < self.capacity:
            if weights_prices[iterator][0] <= abs(reached_capacity - self.capacity):
                profit += weights_prices[iterator][1]
                reached_capacity += weights_prices[iterator][0]
                items += "item" + str(self.prices.index(weights_prices[iterator][1]) + 1) + " "

            if iterator < len(weights_prices) - 1:
                iterator = iterator + 1
            else:
                break

        result = "Items: " + items + " Profit: " + str(profit) + " Weight: " + str(reached_capacity) + "\n"
        return result

    def max_profit_per_weight_0_1(self):
        def value(val):
            return val[0]

        prices_per_weights = np.array(self.prices) / np.array(self.weights)
        ratios_prices_weights = sorted(list(zip(prices_per_weights, self.prices, self.weights)), reverse=True, key=value)
        ratios_prices_weights = self.max_val_first(ratios_prices_weights, 0, 1)
        reached_capacity, profit, iterator = 0, 0, 0
        items = ""

        while reached_capacity < self.capacity:

            if ratios_prices_weights[iterator][2] <= abs(reached_capacity - self.capacity):
                profit += ratios_prices_weights[iterator][1]
                reached_capacity += ratios_prices_weights[iterator][2]
                items += "item" + str(self.prices.index(ratios_prices_weights[iterator][1]) + 1) + " "

            if iterator < len(self.weights) - 1:
                iterator = iterator + 1
            else:
                break

        result = "Items: " + items + " Profit: " + str(profit) + " Weight: " + str(reached_capacity) + "\n"
        return result

    def max_profit_fractional(self):
        def value(val):
            return val[1]

        prices_per_weights = np.array(self.prices) / np.array(self.weights)
        ratios_prices_weights = sorted(list(zip(prices_per_weights, self.prices, self.weights)), reverse=True, key=value)
        ratios_prices_weights = self.min_val_first(ratios_prices_weights, 1, 2)
        reached_weight, profit, iterator = 0, 0, 0
        items = ""

        while reached_weight < self.capacity:

            if ratios_prices_weights[iterator][2] <= abs(reached_weight-self.capacity):
                profit += ratios_prices_weights[iterator][1]
                reached_weight += ratios_prices_weights[iterator][2]
                items += "item" + str(self.prices.index(ratios_prices_weights[iterator][1]) + 1) + " "

            else:
                profit += ratios_prices_weights[iterator][0]*abs(reached_weight-self.capacity)
                items += "item" + str(self.prices.index(ratios_prices_weights[iterator][1]) + 1) + " "
                reached_weight += abs(reached_weight-self.capacity)

            if iterator < len(self.weights) - 1:
                iterator = iterator + 1
            else:
                break

        result = "Items: " + items + " Profit: " + str(profit) + " Weight: " + str(reached_weight) + "\n"
        return result

    def min_weight_fractional(self):
        def value(val):
            return val[2]

        # sort desc. according to ratio
        prices_per_weights = np.array(self.prices) / np.array(self.weights)
        ratios_prices_weights = sorted(list(zip(prices_per_weights, self.prices, self.weights)), key=value)
        ratios_prices_weights = self.max_val_first(ratios_prices_weights, 2, 1)
        reached_capacity, profit, iterator = 0, 0, 0
        items = ""

        while reached_capacity < self.capacity:
            if ratios_prices_weights[iterator][2] <= abs(reached_capacity - self.capacity):
                profit += ratios_prices_weights[iterator][1]
                reached_capacity += ratios_prices_weights[iterator][2]
                items += "item" + str(self.prices.index(ratios_prices_weights[iterator][1]) + 1) + " "

            else:
                profit += abs(reached_capacity-self.capacity) * ratios_prices_weights[iterator][0]
                reached_capacity += abs(reached_capacity-self.capacity)
                items += "item" + str(self.prices.index(ratios_prices_weights[iterator][1]) + 1) + " "

            if iterator < len(ratios_prices_weights) - 1:
                iterator = iterator + 1
            else:
                break

        result = "Items: " + items + " Profit: " + str(profit) + " Weight: " + str(reached_capacity) + "\n"
        return result

    def max_profit_per_weight_fractional(self):
        def value(val):
            return val[0]

        prices_per_weights = np.array(self.prices) / np.array(self.weights)
        ratios_prices_weights = sorted(list(zip(prices_per_weights, self.prices, self.weights)), reverse=True, key=value)
        ratios_prices_weights = self.max_val_first(ratios_prices_weights, 0, 1)
        reached_capacity, profit, iterator = 0, 0, 0
        items = ""

        while reached_capacity < self.capacity:

            if ratios_prices_weights[iterator][2] <= abs(reached_capacity - self.capacity):
                profit += ratios_prices_weights[iterator][1]
                reached_capacity += ratios_prices_weights[iterator][2]
                items += "item" + str(self.prices.index(ratios_prices_weights[iterator][1]) + 1) + " "

            else:
                profit += ratios_prices_weights[iterator][0] * abs(reached_capacity - self.capacity)
                reached_capacity += abs(reached_capacity - self.capacity)
                items += "item" + str(self.prices.index(ratios_prices_weights[iterator][1]) + 1) + " "

            if iterator < len(self.weights) - 1:
                iterator = iterator + 1
            else:
                break

        result = "Items: " + items + " Profit: " + str(profit) + " Weight: " + str(reached_capacity) + "\n"
        return result


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(800, 800)

        self.mainLayout = QVBoxLayout()

        # knapsack mode selection label
        self.modeLabel = QLabel()
        self.modeLabel.setText("Select Knapsack Mode:")
        self.mainLayout.addWidget(self.modeLabel)

        # knapsack mode selection selection box
        self.modeSelect = QComboBox()
        self.modeSelect.setFixedHeight(50)
        self.modeSelect.addItem("0-1 Knapsack")
        self.modeSelect.addItem("Fractional Knapsack")
        self.mainLayout.addWidget(self.modeSelect)

        # cost function label
        self.costFn = QLabel()
        self.costFn.setText("Select Cost Function:")
        self.mainLayout.addWidget(self.costFn)

        # knapsack cost fn. selection selection box
        self.costSelect = QComboBox()
        self.costSelect.setFixedHeight(50)
        self.costSelect.addItem("Maximum Profit")
        self.costSelect.addItem("Minimum Weight")
        self.costSelect.addItem("Maximum Profit/Weight")
        self.costSelect.addItem("All")
        self.mainLayout.addWidget(self.costSelect)

        # knapsack capacity label
        self.capacity = QLabel()
        self.capacity.setText("Enter Knapsack Capacity:")
        self.mainLayout.addWidget(self.capacity)

        # knapsack capacity input field
        self.capInput = QLineEdit()
        self.capInput.setFixedHeight(50)
        self.mainLayout.addWidget(self.capInput)

        # knapsack items weights label
        self.weights = QLabel()
        self.weights.setText("Enter Items' weights e.g. 100,200,400..")
        self.mainLayout.addWidget(self.weights)

        # knapsack items weights input field
        self.weightsInput = QLineEdit()
        self.weightsInput.setFixedHeight(50)
        self.mainLayout.addWidget(self.weightsInput)

        # knapsack items prices label
        self.prices = QLabel()
        self.prices.setText("Enter Items' prices e.g. 100,200,400..")
        self.mainLayout.addWidget(self.prices)

        # knapsack items prices input field
        self.pricesInput = QLineEdit()
        self.pricesInput.setFixedHeight(50)
        self.mainLayout.addWidget(self.pricesInput)

        # Button to display results
        self.submit = QPushButton('Display Results', self)
        self.submit.clicked.connect(self.on_click)
        self.mainLayout.addWidget(self.submit)

        # Result label
        self.result = QLabel()
        self.result.setText("Result: ")
        self.mainLayout.addWidget(self.result)

        # Output label
        self.output = QLabel()
        self.output.setText("")
        self.mainLayout.addWidget(self.output)

        self.setLayout(self.mainLayout)

    def on_click(self):

        # Construct knapsack object
        capacity = float(self.capInput.text())
        weights = [float(weight) for weight in self.weightsInput.text().split(',')]
        prices = [float(price) for price in self.pricesInput.text().split(',')]
        knapsack = Knapsack(capacity, weights, prices)

        # Choose knapsack function according to user selected mode
        mode = self.modeSelect.currentText()
        cost = self.costSelect.currentText()

        if mode == "0-1 Knapsack" and cost == "Maximum Profit":
            self.output.setText(knapsack.max_profit_0_1())

        elif mode == "0-1 Knapsack" and cost == "Minimum Weight":
            self.output.setText(str(knapsack.min_weight_0_1()))

        elif mode == "0-1 Knapsack" and cost == "Maximum Profit/Weight":
            self.output.setText(str(knapsack.max_profit_per_weight_0_1()))

        elif mode == "0-1 Knapsack" and cost == "All":
            self.output.setText(' Max. Profit: '+knapsack.max_profit_0_1()+\
                                ' Min. Weight: '+knapsack.min_weight_0_1()+\
                                ' Max. Profit/Weight: '+knapsack.max_profit_per_weight_0_1())

        elif mode == "Fractional Knapsack" and cost == "Maximum Profit":
            self.output.setText(knapsack.max_profit_fractional())

        elif mode == "Fractional Knapsack" and cost == "Minimum Weight":
            self.output.setText(knapsack.min_weight_fractional())

        elif mode == "Fractional Knapsack" and cost == "Maximum Profit/Weight":
            self.output.setText(knapsack.max_profit_per_weight_fractional())

        elif mode == "Fractional Knapsack" and cost == "All":
            self.output.setText(' Max. Profit: '+knapsack.max_profit_fractional()+\
                                ' Min. Weight: '+knapsack.min_weight_fractional()+\
                                ' Max. Profit/Weight: '+knapsack.max_profit_per_weight_fractional())

app = QApplication(sys.argv)
demo = App()
demo.show()
sys.exit(app.exec_())

