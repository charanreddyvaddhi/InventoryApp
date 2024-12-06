from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from widgets import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowIcon(QIcon('app_icon.ico'))
    window.show()
    sys.exit(app.exec_())
