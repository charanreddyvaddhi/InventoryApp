import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import (QFormLayout, QLineEdit, QComboBox, QDialogButtonBox, QScrollArea, QWidget, QVBoxLayout)
from forms.style_of_form import StyleOfForm

class InventoryForm(StyleOfForm):
    def __init__(self, parent=None, 
                 WindowsClusterID=5, WindowsClusterIP='192.168.1.5', WindowsClusterName='Cluster5.stc.corp',
                 NodeID=109, NodeIP='192.168.1.51', NodeName='NodeI', NodeOSVersion='', NodeComments='Main Node', 
                 SQLClusterID=1007, SQLClusterIP='192.168.1.151', SQLClusterName='SQLCluster7', SQLType='FCI', SQLInstanceName='MSSQLServer', SQLPort='1433', SQLServerVersion='',  NARsRaised='None', SQLComments='None', SQLServerEdition='', MSDTCIP='',
                 ApplicationID=10005, AppName='App5', AppOwner='Ram', AppOwnerEmail='Ram@yahoo.com', AppVersion='1.1.1.', AppDepartment='', AppComments='None', AppCriticality=''):
        super().__init__(parent)
        self.setWindowTitle('Inventory Form')
        
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        # Form Layout
        layout = QFormLayout(scroll_widget)

        # WindowsCluster inputs
        self.winId_input = QLineEdit(self)
        self.winId_input.setText(str(WindowsClusterID))
        self.WinClustIP_input = QLineEdit(self)
        self.WinClustIP_input.setText(str(WindowsClusterIP))
        self.WinClustName_input = QLineEdit(self)
        self.WinClustName_input.setText(str(WindowsClusterName))

        # Node inputs
        self.nodeId_input = QLineEdit(self)
        self.nodeId_input.setText(str(NodeID))
        self.nodeIP_input = QLineEdit(self)
        self.nodeIP_input.setText(str(NodeIP))
        self.nodeName_input = QLineEdit(self)
        self.nodeName_input.setText(str(NodeName))
        self.nodeOS_input = QComboBox(self)
        self.nodeOS_input.addItems(["Windows Server 2012", "Windows Server 2012 R2" ,"Windows Server 2016", "Windows Server 2019", "Windows Server 2022"])
        self.nodeOS_input.setCurrentText(NodeOSVersion)
        self.nodeComments_input = QLineEdit(self)
        self.nodeComments_input.setText(str(NodeComments))

        # SQL Cluster inputs-11
        self.sqlClustId_input = QLineEdit(self)
        self.sqlClustId_input.setText(str(SQLClusterID))
        self.sqlClustIP_input = QLineEdit(self)
        self.sqlClustIP_input.setText(str(SQLClusterIP))
        self.sqlClustName_input = QLineEdit(self)
        self.sqlClustName_input.setText(str(SQLClusterName))
        self.sqlType_input = QLineEdit(self)
        self.sqlType_input.setText(SQLType)
        self.sqlInstanceName_input = QLineEdit(self)
        self.sqlInstanceName_input.setText(SQLInstanceName)
        self.sqlPort_input = QLineEdit(self)
        self.sqlPort_input.setText(SQLPort)
        self.sqlserverversion_input = QComboBox(self)
        self.sqlserverversion_input.addItems(["Microsoft SQL Server 2012", "Microsoft SQL Server 2014", "Microsoft SQL Server 2016", "Microsoft SQL Server 2019", "Microsoft SQL Server 2022"])
        self.sqlserverversion_input.setCurrentText(SQLServerVersion)
        self.narsRaised_input = QLineEdit(self)
        self.narsRaised_input.setText(NARsRaised)
        self.sqlComments_input = QLineEdit(self)
        self.sqlComments_input.setText(SQLComments)
        self.sqlServerEdition_input = QComboBox(self)
        self.sqlServerEdition_input.addItems(["Web","Express Edition","Developer Edition", "Standard Edition", "Enterprise Edition"])
        self.sqlServerEdition_input.setCurrentText(SQLServerEdition)
        self.msdtcIP_input = QLineEdit(self)
        self.msdtcIP_input.setText(MSDTCIP)


        # Application inputs
        self.appId_input = QLineEdit(self)
        self.appId_input.setText(str(ApplicationID))
        self.appName_input = QLineEdit(self)
        self.appName_input.setText(AppName)
        self.appOwner_input = QLineEdit(self)
        self.appOwner_input.setText(AppOwner)
        self.appOwnerEmail_input = QLineEdit(self)
        self.appOwnerEmail_input.setText(AppOwnerEmail)
        self.appVersion_input = QLineEdit(self)
        self.appVersion_input.setText(AppVersion)
        self.appDepartment_input = QComboBox(self)
        self.appDepartment_input.addItems(["AIO", "BIO", "CIO", "DIO", "EIO", "FIO"])
        self.appDepartment_input.setCurrentText(AppDepartment)
        self.appComments_input = QLineEdit(self)
        self.appComments_input.setText(AppComments)
        self.appCriticality_input = QLineEdit(self)
        self.appCriticality_input.setText(AppCriticality)

        # Add rows for WindowsCluster-3
        layout.addRow('WindowsClusterID', self.winId_input)
        layout.addRow('WindowsClusterIP', self.WinClustIP_input)
        layout.addRow('WindowsClusterName', self.WinClustName_input)

        # Add rows for Node-5
        layout.addRow('NodeID', self.nodeId_input)
        layout.addRow('NodeIP', self.nodeIP_input)
        layout.addRow('NodeName', self.nodeName_input)
        layout.addRow('NodeOSVersion', self.nodeOS_input)
        layout.addRow('NodeComments', self.nodeComments_input)

        # Add rows for SQL Cluster -11
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

        # Add rows for Application-8 
        layout.addRow('ApplicationID', self.appId_input)
        layout.addRow('AppName', self.appName_input)
        layout.addRow('AppOwner', self.appOwner_input)
        layout.addRow('AppOwnerEmail', self.appOwnerEmail_input)
        layout.addRow('AppVersion', self.appVersion_input)
        layout.addRow('AppDepartment', self.appDepartment_input)
        layout.addRow('AppComments', self.appComments_input)
        layout.addRow('AppCriticality', self.appCriticality_input)

        # Button Box for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)  # OK button
        button_box.rejected.connect(self.reject)  # Cancel button

        layout.addWidget(button_box)

        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.setLayout(main_layout)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def get_data(self):
        # Collect all the input data
        WindowsClusterID = self.winId_input.text()
        WindowsClusterIP = self.WinClustIP_input.text()
        WindowsClusterName = self.WinClustName_input.text()

        NodeID = self.nodeId_input.text()
        NodeIP = self.nodeIP_input.text()
        NodeName = self.nodeName_input.text()
        NodeOSVersion = self.nodeOS_input.currentText() #as we are using drop down 
        NodeComments = self.nodeComments_input.text()

        SQLClusterID = self.sqlClustId_input.text()
        SQLClusterIP = self.sqlClustIP_input.text()
        SQLClusterName = self.sqlClustName_input.text()
        SQLType = self.sqlType_input.text()
        SQLInstanceName = self.sqlInstanceName_input.text()
        SQLPort = self.sqlPort_input.text()
        SQLServerVersion = self.sqlserverversion_input.currentText() #as we are using drop down 
        NARsRaised = self.narsRaised_input.text()
        SQLComments = self.sqlComments_input.text()
        SQLServerEdition = self.sqlServerEdition_input.currentText() #as we are using drop down 
        MSDTCIP = self.msdtcIP_input.text()

        ApplicationID = self.appId_input.text()
        AppName = self.appName_input.text()
        AppOwner = self.appOwner_input.text()
        AppOwnerEmail = self.appOwnerEmail_input.text()
        AppVersion = self.appVersion_input.text()
        AppDepartment = self.appDepartment_input.currentText() #as we are using drop down 
        AppComments = self.appComments_input.text()
        AppCriticality = self.appCriticality_input.text()

        # Return all collected data as a tuple
        return (WindowsClusterID, WindowsClusterIP, WindowsClusterName,
                NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments,
                SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP,
                ApplicationID, AppName, AppOwner, AppOwnerEmail, AppVersion, AppDepartment, AppComments, AppCriticality)
