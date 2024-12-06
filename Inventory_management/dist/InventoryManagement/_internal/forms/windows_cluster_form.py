import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QFormLayout, QLineEdit, QDialogButtonBox
from forms.style_of_form import StyleOfForm
from PyQt5.QtGui import QIcon

class WindowsClusterForm(StyleOfForm):
    def __init__(self, parent=None, 
                 WindowsClusterID=0, WindowsClusterIP='***.***.***.***', WindowsClusterName='.STC.CORP'):
        super().__init__(parent)
        self.setWindowTitle('Windows Cluster Form')
        self.setGeometry(50, 50, 400, 200)
        self.setWindowIcon(QIcon("Forms.ico"))
        layout = QFormLayout()

        # Windows Cluster inputs
        self.winId_input = QLineEdit(self)
        self.winId_input.setText(str(WindowsClusterID))
        self.WinClustIP_input = QLineEdit(self)
        self.WinClustIP_input.setText(WindowsClusterIP)
        self.WinClustName_input = QLineEdit(self)
        self.WinClustName_input.setText(WindowsClusterName)

        # Add rows for Windows Cluster inputs
        layout.addRow('WindowsClusterID', self.winId_input)
        layout.addRow('WindowsClusterIP', self.WinClustIP_input)
        layout.addRow('WindowsClusterName', self.WinClustName_input)

        # Button Box for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_data(self):
        # Collect and return Windows Cluster data
        return (self.winId_input.text(), self.WinClustIP_input.text(), self.WinClustName_input.text())
