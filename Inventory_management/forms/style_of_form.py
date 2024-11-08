from PyQt5.QtWidgets import QDialog, QTabWidget

class StyleOfForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setGeometry(50, 50, 700, 700)
        self.setStyleSheet("""
            QWidget, QMainWindow {background-color:#DCDCDC; font-family:Century Gothic;}
            QLineEdit, QComboBox {padding:5px; background-color:#CCCCCC; border:2px solid #CCCCCC; border-radius:5px;}
            QLineEdit:focus, QComboBox:focus {border:2px solid #4F008C;}
            QPushButton, QDialogButtonBox {
                background-color: #4F008C;
                font-weight: bold; font-size: 15px;
                color:white; border:none; border-radius:10px; padding:5px;
            }
            QPushButton:hover, QDialogButtonBox:hover {background-color:#0056B3;}
            QLabel {font-size:14px; color:#333333;}
        """)
        self.tab_widget = QTabWidget(self)  # Adding the QTabWidget if needed in your style
