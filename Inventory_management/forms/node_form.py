import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QDialogButtonBox
from database import get_osVersion
from forms.style_of_form import StyleOfForm
from PyQt5.QtGui import QIcon

class NodeForm(StyleOfForm):
    def __init__(self, parent=None, 
                 NodeID=000, NodeIP='***.***.***.***', NodeName='.STC.CORP', NodeOSVersion='', NodeComments='Main Node', WinClusterID=0):
        super().__init__(parent)
        self.setWindowTitle('Node Form')
        self.setGeometry(50, 50, 400, 300)
        self.setWindowIcon(QIcon("Forms.ico"))
        layout = QFormLayout()

        # Node inputs
        self.nodeId_input = QLineEdit(self)
        self.nodeId_input.setText(str(NodeID))
        self.nodeIP_input = QLineEdit(self)
        self.nodeIP_input.setText(NodeIP)
        self.nodeName_input = QLineEdit(self)
        self.nodeName_input.setText(NodeName)
        self.nodeOS_input = QComboBox(self)
        self.nodeOS_input.addItems(get_osVersion())
        self.nodeOS_input.setCurrentText(NodeOSVersion)
        self.nodeComments_input = QLineEdit(self)
        self.nodeComments_input.setText(NodeComments)
        self.windowsclusterId_input = QLineEdit(self)
        self.windowsclusterId_input.setText(str(WinClusterID))

        # Add rows for Node inputs
        layout.addRow('NodeID', self.nodeId_input)
        layout.addRow('NodeIP', self.nodeIP_input)
        layout.addRow('NodeName', self.nodeName_input)
        layout.addRow('NodeOSVersion', self.nodeOS_input)
        layout.addRow('NodeComments', self.nodeComments_input)
        layout.addRow('WinClusterID', self.windowsclusterId_input)

        # Button Box for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_data(self):
        # Collect and return Node data
        return (self.nodeId_input.text(), self.nodeIP_input.text(), self.nodeName_input.text(),
                self.nodeOS_input.currentText(), self.nodeComments_input.text(), self.windowsclusterId_input.text())
