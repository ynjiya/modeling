from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
import random
import math 
from itertools import islice
import time

N = 10


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.fill_alg.clicked.connect(lambda: on_fill_alg_click(self))
        self.fill_table.clicked.connect(lambda: on_fill_table_click(self))
        self.manual_input.returnPressed.connect(lambda: on_manual_input_enter(self))

        self.line_num = 0

        for i in range(10):
            self.alg_table.insertRow(i)

        for i in range(10):
            self.table_table.insertRow(i)


"""
[0, 9] -> digits = 1
[10, 99] -> digits = 10
[100, 999] -> digits = 100
"""
def assess_randomness(sequence, digits):
    count = len(sequence) 
    if count == 0:
        return 0
    digit = 1
    result = []

    while (1):
        k = 0
        hist = dict()
        hist.update({sequence[0]//digit: 1})
        dif = sequence[1]//digit - sequence[0]//digit
        for i in range(1, count):
            if sequence[i]//digit not in hist.keys():
                hist.update({sequence[i]//digit: 1})
            else:
                hist[sequence[i]//digit] += 1
            if i != 1 and sequence[i]//digit - sequence[i-1]//digit == dif:
                k -= 1/count
            else:
                dif = sequence[i]//digit - sequence[i-1]//digit

        for unique in hist.keys():
            p = hist[unique] / count
            k -= p * math.log(p, count)

        result.append(k)

        if digit == digits:
            break
        else:
            digit = digit * 10

    return sum(result)/len(result)

def program_generator(num, size):
    res = [0 for i in range(size + 1)]
    res[0] = math.ceil(time.time())
    for i in range(1, size + 1):
        res[i] = math.ceil(math.fmod((a * res[i - 1] + b), m))
    for i in range(size + 1):
        res[i] = str(res[i])[:num]
    res = [int(x) for x in res]
    return res[1:size+1]


def on_fill_alg_click(win):
    table = win.alg_table
    random.seed()
    one_digit = [random.randint(0, 9) for i in range(N)]
    two_digits = [random.randint(10, 99) for i in range(N)]
    three_digits = [random.randint(100, 999) for i in range(N)]

    for i in range(10):
        item = QTableWidgetItem(str(one_digit[i]))
        table.setItem(i, 0, item)

    for i in range(10):
        item = QTableWidgetItem(str(two_digits[i]))
        table.setItem(i, 1, item)

    for i in range(10):
        item = QTableWidgetItem(str(three_digits[i]))
        table.setItem(i, 2, item)

    #table.resizeColumnsToContents()
    entropy_one = assess_randomness(one_digit, 1)
    entropy_two = assess_randomness(two_digits, 10) 
    entropy_three = assess_randomness(three_digits, 100)
    win.meas_alg_1.setText('{:.4%}'.format(entropy_one))
    win.meas_alg_2.setText('{:.4%}'.format(entropy_two))
    win.meas_alg_3.setText('{:.4%}'.format(entropy_three))
    

def on_fill_table_click(win):
    table = win.table_table
    numbers = set()
    with open('digits.txt') as file: 
        lines = islice(file, win.line_num, None)
        for l in lines:
            numbers.update(set(l.split(" ")[1:-1]))
            win.line_num += 1
            if len(numbers) >= 3001:
                break
        numbers.remove("") 
        numbers = list(numbers)[:3000]
    one_digit = [int(i)%9 + 1 for i in numbers[:N]]
    two_digits = [int(i)%90 + 10 for i in numbers[:N]]
    three_digits = [int(i)%900 + 100 for i in numbers[:N]]
    
    for i in range(10):
        item = QTableWidgetItem(str(one_digit[i]))
        table.setItem(i, 0, item)

    for i in range(10):
        item = QTableWidgetItem(str(two_digits[i]))
        table.setItem(i, 1, item)

    for i in range(10):
        item = QTableWidgetItem(str(three_digits[i]))
        table.setItem(i, 2, item)

    entropy_one = assess_randomness(one_digit, 1)
    entropy_two = assess_randomness(two_digits, 10) 
    entropy_three = assess_randomness(three_digits, 100)
    win.meas_table_1.setText(' {:.4%}'.format(entropy_one))
    win.meas_table_2.setText(' {:.4%}'.format(entropy_two))
    win.meas_table_3.setText(' {:.4%}'.format(entropy_three))

def on_manual_input_enter(win):
    input = win.manual_input
    measure = win.meas_manual
    sequence = input.text().split(" ")
    filtered_sequence = []
    for i in sequence:
        try:
            int(i)
        except ValueError:
            continue
        else:
            filtered_sequence.append(i)

    input_list = list(map(lambda x: int(x), filtered_sequence))
    input_list_digit = len(str(input_list[0])) # assume all list members have equal digits
    entropy = assess_randomness(input_list, 10**input_list_digit/10)
    win.meas_manual.setText(' {:.4%}'.format(entropy))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())