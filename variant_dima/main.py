import sys

from PyQt5 import QtCore

sys.path.append("..")
from PyQt5.QtWidgets import QApplication
import Windows

if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    state_list_widget = [Windows.MainWindow(),
                         Windows.Registration(),
                         Windows.Login(),
                         Windows.Director(),
                         Windows.Manager(),
                         Windows.Keeper(),
                         Windows.Customer()]

    main = Windows.MyMainWindow(state_list_widget)
    main.resize(500, 300)
    main.setWindowTitle("ИнфоСистема заказчика")
    main.show()
    qapp.exec()