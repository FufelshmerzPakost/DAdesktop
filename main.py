import sys
from UI import ui_statistic, ui_start, ui_information
from AnalyzeTools import AnalyzeTool
import pyqtgraph as pg
from pyqtgraph import ScatterPlotItem
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout

class StartWindow(QMainWindow, ui_start.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_file)

    def get_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "","All Files (*);;Python Files (*.py)", options=options)
        if file:
            self.open_analyze(file)

    def open_analyze(self, file):
        self.newWindow = StatisticWindow(file)
        self.newWindow.show()

class StatisticWindow(QMainWindow, ui_statistic.Ui_MainWindow):
    def __init__(self, file):
        super().__init__()
        self.setupUi(self)
        self.dt = AnalyzeTool(file)
        self.plot = pg.PlotWidget()
        self.plot.setBackground(QColor(240, 240, 240))
        self.plot.setLabel('bottom', 'X')
        self.plot.setLabel('left', 'Y')
        self.plot.setLabel('right', 'Y')
        self.plot.showGrid(x=True, y=True)
        self.view = QtWidgets.QGraphicsView()
        self.view.setScene(self.plot.plotItem.vb.scene())
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.plot)
        self.centralwidget.setLayout(self.layout)
        self.plot_graph()

    def plot_graph(self):
        points = self.dt.scatterXY
        item = ScatterPlotItem()
        item.setData(points[0], points[1])
        self.plot.addItem(item)
        self.ux = [self.dt.df['x'].min(), self.dt.df['x'].max()]
        self.uy = [self.dt.a * i + self.dt.b for i in self.ux]
        line = self.plot.plot(self.ux, self.uy)
        pen = QPen(QColor('green'))
        pen.setWidthF(0.1)
        line.setPen(pen)
        self.analizeWindow = AnalyzeWindow(self)
        self.analizeWindow.show()

class AnalyzeWindow(QMainWindow, ui_information.Ui_Form):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        self.setupUi(self)
        self.reload()
        self.pushButton.clicked.connect(self.analyze)
        self.pushButton_2.clicked.connect(self.add_new_val)
        self.pushButton_3.clicked.connect(self.reset)

    def analyze(self):
        x = float(self.lineEdit.text())
        y = round(self.obj.dt.equation(float(x)), 2)
        self.lineEdit_2.setText(str(y))

        if self.checkBox.isChecked():
            self.obj.dt.add_elem(x, y)
            sct = ScatterPlotItem(pen=QColor(0, 255, 0), brush=QColor(0, 255, 0))
            sct.setData([x], [y])
            self.obj.plot.addItem(sct)
            self.reload()
            self.obj.dt.counter += 1

    def add_new_val(self):
        x = float(self.lineEdit_11.text())
        y = float(self.lineEdit_12.text())
        self.obj.dt.add_elem(x, y)
        sct = ScatterPlotItem(pen=QColor(255, 0, 0), brush=QColor(255, 0, 0))
        sct.setData([x], [y])
        self.obj.plot.addItem(sct)
        self.reload()
        self.obj.dt.counter += 1

    def reset(self):
        self.obj.dt.df = self.obj.dt.df.drop([i for i in range(len(self.obj.dt.df) - self.obj.dt.counter, len(self.obj.dt.df))])
        print(self.obj.dt.df)
        self.obj.dt.counter = 0
        self.obj.plot.clear()
        self.obj.plot_graph()
        self.reload()

    def reload(self):
        self.label.setText(self.obj.dt.graph_equation())
        self.lineEdit_3.setText(str(round(self.obj.dt.appr_error, 2)))
        self.lineEdit_4.setText(str(round(self.obj.dt.elasticity, 2)))
        self.lineEdit_5.setText(str(round(self.obj.dt.factor_r, 2)))
        self.lineEdit_6.setText(str(round(self.obj.dt.factor_r ** 2, 2)))
        self.lineEdit_7.setText(str(round(self.obj.dt.t_student, 2)))
        self.lineEdit_8.setText(str(round(self.obj.dt.critical_ts, 2)))
        self.lineEdit_9.setText(str(round(self.obj.dt.factor_F, 2)))
        self.lineEdit_10.setText(str(round(4.67, 2)))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = StartWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()

