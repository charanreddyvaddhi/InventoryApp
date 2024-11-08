import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QDialogButtonBox
from forms.style_of_form import StyleOfForm

class ApplicationForm(StyleOfForm):
    def __init__(self, parent=None, 
                 ApplicationID=0, AppName='', AppOwner='', AppOwnerEmail='@yahoo.com', AppVersion='', AppDepartment='', AppComments='None', AppCriticality=''):
        super().__init__(parent)
        self.setWindowTitle('Application Form')
        self.setGeometry(50, 50, 400, 300)

        layout = QFormLayout()

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

        # Add rows for Application
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
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_data(self):
        # Collect and return Application data
        return (self.appId_input.text(), self.appName_input.text(), self.appOwner_input.text(), self.appOwnerEmail_input.text(),
                self.appVersion_input.text(), self.appDepartment_input.currentText(), self.appComments_input.text(), self.appCriticality_input.text())
