
from numpy import *
from pyqtgraph.Qt import QtWidgets
import pyqtgraph as pg
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

ads = ADS.ADS1115(i2c, address=0x48)

ads.gain = 16

ads.data_rate = 860

chan = AnalogIn(ads, ADS.P0, ADS.P1)

app = QtWidgets.QApplication([])

win = pg.GraphicsLayoutWidget(title="Sismograf")

x_ekseni = win.addPlot(title="mm/s")
x_ekseni.showGrid(x=True, y=True, alpha=0.3)
x_ekseni_grafik = x_ekseni.plot(pen=pg.mkPen('#0f0'))

windowWidth = 10000

x_degerler = linspace(0, 0, windowWidth)

win.show()

ptr = -windowWidth


def update():
    global x_ekseni_grafik, ptr, x_degerler
    x_degerler[:-1] = x_degerler[1:]

    x_degerler[-1] = round((chan.value * 0.0078125) / 28.8, 5)
    # x_degerler[-1] = chan.value

    ptr += 1
    x_ekseni_grafik.setData(x_degerler)
    x_ekseni_grafik.setPos(ptr, 0)

    QtWidgets.QApplication.processEvents()


while True:
    update()


pg.QtGui.QApplication.exec_()
