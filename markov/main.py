import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget,  QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from markov import *


class TimeGCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot()
        super(TimeGCanvas, self).__init__(self.fig)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("window.ui", self)
        self.tableWidgetMatrix.itemChanged.connect(lambda x: self._item_changed(x))
        self.spinBoxStatesCount.setValue(3)

        self.chooseMethod.setCurrentIndex(0)
        self.methods = [self.chooseMethod.itemText(i) for i in range(self.chooseMethod.count())]
        self.method = self.methods[1]
        self.time_graph = TimeGCanvas(self, width=5, height=4, dpi=100)

        self.figure = plt.figure()
        # plt.rcParams["figure.figsize"] = [7.50, 3.50]
        # plt.rcParams["figure.autolayout"] = True
        self.graph = FigureCanvasQTAgg(self.figure)
        self.vlStateGraph.addWidget(self.graph)


    def _item_changed(self, value):
        try:
            if value.text() != "":
                float(value.text())
        except ValueError:
            QtWidgets.QMessageBox.critical(None, "Invalid input", "Enter a float number!\nSum of the values per row must be equal to 1")
            value.setText("")


    @pyqtSlot()
    def on_chooseMethod_valueChanged(self, value):
        self.method = value


    @pyqtSlot()
    def on_pushButtonCalc_clicked(self):
        tm = self._get_matrix_from_table()
        # tm = np.array([[0.2, 0.6, 0.2], [0.3, 0, 0.7], [0.5, 0, 0.5]])
        tm = np.array(tm)
        n = len(tm)
        self.ui.resultTable.clear()
        self.method = self.chooseMethod.currentText()
        print("self.method", self.method)


        if self._check_transition_matrix(tm) is False:
            return

        if self.method == self.methods[0]: # Repeated matrix multiplication
            pi, probs, stable_time = repeated_mult(tm, n)
            print(pi, probs, stable_time)
        else:
            pi, probs, stable_time = left_eigenvector(tm, n)
            print(pi, probs, stable_time)

        xlen = int(max(stable_time)*GRAPH_OX)
        x = [i * TIME_DELTA / xlen for i in range(xlen)]
        stable_time = [i * TIME_DELTA / xlen for i in stable_time]

        currentRowCount = self.resultTable.rowCount() 
        for i in range(n):
            self.resultTable.insertRow(currentRowCount)


        # Result Table
        for state in range(n):
            # QListWidgetItem("{n}: {time:0.5f}".format(n = i, time = round(state, 5)), self.ui.resultTable)
            self.resultTable.setItem(state,0, QTableWidgetItem(str(round(pi[state], 6))))
            self.resultTable.setItem(state,1, QTableWidgetItem(str(round(stable_time[state], 3))))

        self.time_graph.close()
        self.time_graph = TimeGCanvas(self, width=5, height=4, dpi=100)

        # Time graph
        for i in range(n):
            self.time_graph.axes.plot(x, probs[i], label = 'S' + str(i))
            self.time_graph.axes.scatter(stable_time[i], pi[i], color='orange', s=40, marker='o')
        self.time_graph.axes.legend()
        self.time_graph.axes.set_xlabel('Time')
        self.time_graph.axes.set_ylabel('Probability')
        self.vlTimeGraph.addWidget(self.time_graph)


        # Weighed graph
        self.figure.clf()
        print(tm)
        DG = nx.DiGraph(tm, format='weighted_adjacency_matrix')  
        pos = nx.circular_layout(DG)
        pos_nodes = self._nudge(pos, 0, 0.23)     
        DG.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}

        nx.draw(DG, pos, with_labels=True, connectionstyle='arc3, rad=0.15', node_size=700, node_color='green', )
        labels = nx.get_edge_attributes(DG, 'weight')
        print(labels)
        nx.draw_networkx_edge_labels(DG, pos_nodes, edge_labels=labels, label_pos=0.75, font_size=13, bbox=dict(alpha=0))
        self.graph.draw_idle()


    @pyqtSlot('int')
    def on_spinBoxStatesCount_valueChanged(self, value):
        self.ui.tableWidgetMatrix.setRowCount(value)
        self.ui.tableWidgetMatrix.setColumnCount(value)
        self.ui.tableWidgetMatrix.clearContents()
            

    def _get_matrix_from_table(self):
        res = []
        try:
            for i in range(self.ui.tableWidgetMatrix.rowCount()):
                row = []
                for j in range(self.ui.tableWidgetMatrix.columnCount()):
                    item  = self.ui.tableWidgetMatrix.item(i, j)
                    val =  item.text() if item and item.text() != "" else "0"
                    row.append(float(val))
                res.append(row)
        except KeyError:
            print(res)
            QtWidgets.QMessageBox.critical(None, "Invalid input", "Enter a float number!\nSum of the values per row must be equal to 1")
        return res


    def _check_transition_matrix(self, matrix):
        for i in range(len(matrix)):
            if sum(matrix[i]) != 1 or sum(matrix[i]) != 0.9999999999999999:
                
                print("in _check_transition_matrix")
                print(sum(matrix[i]))
                print(matrix)
                QtWidgets.QMessageBox.critical(None, "Invalid input", "Enter a float number!\nSum of the values per row must be equal to 1")
                return False
        return True


    def _matrix_to_nx(self, matrix):
        result = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                result.append((i, j, matrix[i][j]))
        return result


    def _nudge(self, pos, x_shift, y_shift):
        return {n:(x + x_shift, y + y_shift) for n,(x,y) in pos.items()}


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
