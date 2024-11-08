import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QDialogButtonBox
from forms.style_of_form import StyleOfForm

class SQLClusterForm(StyleOfForm):
    def __init__(self, parent=None, 
                 SQLClusterID=0, SQLClusterIP='***.***.***.***', SQLClusterName='', SQLType='', SQLInstanceName='', SQLPort='1433', SQLServerVersion='', 
                 NARsRaised='None', SQLComments='None', SQLServerEdition='', MSDTCIP=''):
        super().__init__(parent)
        self.setWindowTitle('SQL Cluster Form')
        self.setGeometry(50, 50, 400, 300)

        layout = QFormLayout()

        # SQL Cluster inputs
        self.sqlClustId_input = QLineEdit(self)
        self.sqlClustId_input.setText(str(SQLClusterID))
        self.sqlClustIP_input = QLineEdit(self)
        self.sqlClustIP_input.setText(SQLClusterIP)
        self.sqlClustName_input = QLineEdit(self)
        self.sqlClustName_input.setText(SQLClusterName)
        self.sqlType_input = QLineEdit(self)
        self.sqlType_input.setText(SQLType)
        self.sqlInstanceName_input = QLineEdit(self)
        self.sqlInstanceName_input.setText(SQLInstanceName)
        self.sqlPort_input = QLineEdit(self)
        self.sqlPort_input.setText(str(SQLPort))
        self.sqlserverversion_input = QComboBox(self)
        self.sqlserverversion_input.addItems(["Microsoft SQL Server 2012", "Microsoft SQL Server 2014", "Microsoft SQL Server 2016", "Microsoft SQL Server 2019", "Microsoft SQL Server 2022"])
        self.sqlserverversion_input.setCurrentText(SQLServerVersion)
        self.narsRaised_input = QLineEdit(self)
        self.narsRaised_input.setText(NARsRaised)
        self.sqlComments_input = QLineEdit(self)
        self.sqlComments_input.setText(SQLComments)
        self.sqlServerEdition_input = QComboBox(self)
        self.sqlServerEdition_input.addItems(["Web", "Express Edition", "Developer Edition", "Standard Edition", "Enterprise Edition"])
        self.sqlServerEdition_input.setCurrentText(SQLServerEdition)
        self.msdtcIP_input = QLineEdit(self)
        self.msdtcIP_input.setText(MSDTCIP)

        # Add rows for SQL Cluster inputs
        layout.addRow('SQLClusterID', self.sqlClustId_input)
        layout.addRow('SQLClusterIP', self.sqlClustIP_input)
        layout.addRow('SQLClusterName', self.sqlClustName_input)
        layout.addRow('SQLType', self.sqlType_input)
        layout.addRow('SQLInstanceName', self.sqlInstanceName_input)
        layout.addRow('SQLPort', self.sqlPort_input)
        layout.addRow('SQLServerVersion', self.sqlserverversion_input)
        layout.addRow('NARsRaised', self.narsRaised_input)
        layout.addRow('SQLComments', self.sqlComments_input)
        layout.addRow('SQLServerEdition', self.sqlServerEdition_input)
        layout.addRow('MSDTCIP', self.msdtcIP_input)

        # Button Box for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_data(self):
        # Collect and return SQL Cluster data
        return (self.sqlClustId_input.text(), self.sqlClustIP_input.text(), self.sqlClustName_input.text(),
                self.sqlType_input.text(), self.sqlInstanceName_input.text(), self.sqlPort_input.text(),
                self.sqlserverversion_input.currentText(), self.narsRaised_input.text(),
                self.sqlComments_input.text(), self.sqlServerEdition_input.currentText(), self.msdtcIP_input.text())
