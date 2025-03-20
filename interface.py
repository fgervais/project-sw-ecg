import logging
import qdarktheme
import numpy as np
import pickle

import pyqtgraph as pg
import pyqtgraph.opengl as gl

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from pglive.kwargs import LeadingLine
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget
from pyqtgraph import mkPen
from pyqtgraph.Qt import QtCore

from scipy import fftpack
from scipy import ndimage
from scipy.optimize import curve_fit

from datetime import datetime


logger = logging.getLogger(__name__)
# if "DEBUG" in os.environ:
#     logger.setLevel(logging.DEBUG)


app = QApplication([])


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ECG")

        # https://www.flaticon.com/packs/school-kawaii-15764145
        # icon = QIcon("flask-analysis.png")
        # self.setWindowIcon(icon)

        layout = pg.LayoutWidget()

        self.setCentralWidget(layout)

        widget, self.voltage_connector = self.build_battery_voltage_ui()
        layout.addWidget(widget, row=0, col=0)

        self.show()

    def update_battery_voltage_view(self, voltage):
        self.voltage_connector.cb_append_data_point(voltage)

    def build_battery_voltage_ui(self):
        plot_widget = LivePlotWidget(title=f"Battery voltage")
        plot_curve = LiveLinePlot()
        plot_curve.set_leading_line(
            LeadingLine.VERTICAL, pen=mkPen("red"), text_axis=LeadingLine.AXIS_Y
        )
        plot_widget.addItem(plot_curve)
        data_connector = DataConnector(
            plot_curve, max_points=60 * 60, update_rate=100
        )

        return plot_widget, data_connector


def exec():
    qdarktheme.setup_theme()

    app.exec()
