import sys
import pyodbc
import hashlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QInputDialog, QMessageBox, QLineEdit, QLabel, QFormLayout, QDialog, QDialogButtonBox
)
from PyQt5.QtGui import QIcon

# Hash password function for better security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup Window for new users
class SignupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sign Up')

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

    def get_sql_connection(self):
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 13 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=CRUD_;'
            'UID=django;'
            'PWD=Charan@1999'
        )
        return conn

    def handle_signup(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        if password != confirm_password:
            QMessageBox.warning(self, 'Sign Up Failed', 'Passwords do not match')
            return

        conn = self.get_sql_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

        if result:
            QMessageBox.warning(self, 'Sign Up Failed', 'Username already exists.')
        else:
            password_hash = hash_password(password)
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
            conn.close()
            QMessageBox.information(self, 'Sign Up Successful', 'Your account has been created.')
            self.accept()

# Login Window for returning users
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')

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

    def get_sql_connection(self):
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 13 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=CRUD_;'
            'UID=django;'
            'PWD=Charan@1999'
        )
        return conn

    def handle_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        conn = self.get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

        if result:
            if hash_password(password) == result[0]:
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
            self.handle_login()  # Retry login after successful sign-up

# Main Window for inventory management
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Inventory Management')
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = int((screen_geometry.width() - 600) / 2)
        y = int((screen_geometry.height() - 400) / 2)
        self.setGeometry(x, y, 600, 400)

        # Create the main vertical layout
        main_layout = QVBoxLayout()

        # Create the button layout (horizontal layout)
        button_layout = QHBoxLayout()

        # CRUD Buttons
        self.refresh_button = QPushButton('Show Data')
        self.add_button = QPushButton('Add New Item')
        self.update_button = QPushButton('Update Item')
        self.delete_button = QPushButton('Delete Item')
        self.logout_button = QPushButton('Logout')

        self.refresh_button.setFixedSize(100, 30)
        self.add_button.setFixedSize(100, 30)
        self.update_button.setFixedSize(100, 30)
        self.delete_button.setFixedSize(100, 30)
        self.logout_button.setFixedSize(100, 30)

        # Connect buttons to methods
        self.refresh_button.clicked.connect(self.show_data)
        self.add_button.clicked.connect(self.add_item)
        self.update_button.clicked.connect(self.update_item)
        self.delete_button.clicked.connect(self.delete_item)
        self.logout_button.clicked.connect(self.handle_logout)

        # Add buttons to the button layout
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.logout_button)

        # Create the table to display SQL Server data
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price"])

        # Add the button layout and table to the main layout
        main_layout.addLayout(button_layout)  # Button layout on top
        main_layout.addWidget(self.table)      # Table below buttons

        # Set the main layout on the window
        self.setLayout(main_layout)

    def get_sql_connection(self):
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 13 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=CRUD_;'
            'UID=django;'
            'PWD=Charan@1999'
        )
        return conn

    def show_data(self):
        conn = self.get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM items")
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(row[1]))
            self.table.setItem(i, 2, QTableWidgetItem(str(row[2])))

        conn.close()

    def add_item(self):
        name, ok1 = QInputDialog.getText(self, 'Add Item', 'Enter item name:')
        if ok1:
            price, ok2 = QInputDialog.getDouble(self, 'Add Item', 'Enter item price:')
            if ok2:
                conn = self.get_sql_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))
                conn.commit()
                conn.close()
                self.show_data()

    def update_item(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            id = self.table.item(selected_row, 0).text()
            name, ok1 = QInputDialog.getText(self, 'Update Item', 'Enter new item name:')
            if ok1:
                price, ok2 = QInputDialog.getDouble(self, 'Update Item', 'Enter new item price:')
                if ok2:
                    conn = self.get_sql_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE items SET name=?, price=? WHERE id=?", (name, price, id))
                    conn.commit()
                    conn.close()
                    self.show_data()
        else:
            QMessageBox.warning(self, "Update Item", "Please select an item to update.")

    def delete_item(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            id = self.table.item(selected_row, 0).text()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE id=?", (id,))
            conn.commit()
            conn.close()
            self.show_data()
        else:
            QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")

    def handle_logout(self):
        QMessageBox.information(self, 'Logged Out', 'You have been logged out.')
        self.close()  # Close the main window after logout

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Start with the login window
    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        # Open the main window after successful login
        mainWindow = MainWindow()
        mainWindow.show()

    sys.exit(app.exec_())
