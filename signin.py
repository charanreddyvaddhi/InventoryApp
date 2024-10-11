import sys
import pyodbc
import hashlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,QTableWidget, QTableWidgetItem,
    QInputDialog, QMessageBox, QLineEdit,QLabel, 
    QFormLayout, QDialog, QDialogButtonBox, 
)
from PyQt5.QtGui import QIcon

class SignupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sign Up')
        self.setWindowIcon(QIcon('signup_icon.png'))  # Use an appropriate icon file

        layout = QFormLayout()
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        layout.addRow(QLabel('Username:'), self.username_edit)
        layout.addRow(QLabel('Password:'), self.password_edit)
        layout.addRow(QLabel('Confirm Password:'), self.confirm_password_edit)

        self.signup_button = QPushButton('Sign Up')
        self.signup_button.clicked.connect(self.handle_signup)

        button_box = QDialogButtonBox()
        button_box.addButton(self.signup_button, QDialogButtonBox.AcceptRole)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_signup(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        if password != confirm_password:
            QMessageBox.warning(self, 'Sign Up Failed', 'Passwords do not match')
            return

        conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};'
                              'SERVER=localhost;'
                              'DATABASE=CRUD_;'
                              'UID=django;'
                              'PWD=Charan@1999')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        QMessageBox.information(self, 'Sign Up Successful', 'Your account has been created.')
        self.accept()

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setWindowIcon(QIcon('login_icon.png'))  # Use an appropriate icon file

        layout = QFormLayout()
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addRow(QLabel('Username:'), self.username_edit)
        layout.addRow(QLabel('Password:'), self.password_edit)

        self.login_button = QPushButton('Login')
        self.signup_button = QPushButton('Sign Up')
        self.login_button.clicked.connect(self.handle_login)
        self.signup_button.clicked.connect(self.open_signup_window)

        button_box = QDialogButtonBox()
        button_box.addButton(self.login_button, QDialogButtonBox.AcceptRole)
        button_box.addButton(self.signup_button, QDialogButtonBox.ActionRole)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};'
                              'SERVER=localhost;'
                              'DATABASE=CRUD_;'
                              'UID=django;'
                              'PWD=Charan@1999')
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

        if result:
            if password == result[0]:  # Replace with actual password verification logic
                self.accept()
            else:
                QMessageBox.warning(self, 'Login Failed', 'Incorrect password')
        else:
            QMessageBox.information(self, 'User Not Found', 'User does not exist. Please sign up.')
            self.open_signup_window()

        conn.close()

    def open_signup_window(self):
        self.signup_window = SignupWindow()
        if self.signup_window.exec_() == QDialog.Accepted:
            self.handle_login()  # Retry login after sign-up

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.logged_in = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Application')
        self.setWindowIcon(QIcon('app_icon.png'))  # Use an appropriate icon file

        layout = QVBoxLayout()

        self.login_button = QPushButton('Login')
        self.logout_button = QPushButton('Logout')
        self.logout_button.setDisabled(True)

        self.login_button.clicked.connect(self.login)
        self.logout_button.clicked.connect(self.logout)

        layout.addWidget(self.login_button)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def login(self):
        self.login_window = LoginWindow()
        if self.login_window.exec_() == QDialog.Accepted:
            self.logged_in = True
            self.login_button.setDisabled(True)
            self.logout_button.setDisabled(False)
            QMessageBox.information(self, 'Logged In', 'You are now logged in.')

    def logout(self):
        self.logged_in = False
        self.login_button.setDisabled(False)
        self.logout_button.setDisabled(True)
        QMessageBox.information(self, 'Logged Out', 'You have been logged out.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
