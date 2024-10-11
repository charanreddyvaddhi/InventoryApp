import sys
import pyodbc
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QFormLayout, QDialog, QLabel, QDialogButtonBox, QMessageBox
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Inventory-V1')

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

        # Sizes of CRUD Buttons
        self.refresh_button.setFixedSize(100, 30)
        self.add_button.setFixedSize(100, 30)
        self.update_button.setFixedSize(100, 30)
        self.delete_button.setFixedSize(100, 30)

        # Connect buttons to methods
        self.refresh_button.clicked.connect(self.show_data)
        self.add_button.clicked.connect(self.open_add_form)
        self.update_button.clicked.connect(self.open_update_form)
        self.delete_button.clicked.connect(self.delete_item)

        # Add buttons to the button layout
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        # Create the table to display SQL Server data
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price"])

        # Add the button layout and table to the main layout
        main_layout.addLayout(button_layout)  # Button layout on top
        main_layout.addWidget(self.table)      # Table below buttons

        # Adjust layout spacing and margins
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(15, 15, 15, 15)

        # Set the main layout on the window
        self.setLayout(main_layout)

    # Define Database Connection
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

    def open_add_form(self):
        form = ItemForm(self)
        if form.exec_() == QDialog.Accepted:
            name, price = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))
            conn.commit()
            conn.close()
            self.show_data()

    def open_update_form(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            id = self.table.item(selected_row, 0).text()
            current_name = self.table.item(selected_row, 1).text()
            current_price = float(self.table.item(selected_row, 2).text())

            form = ItemForm(self, current_name, current_price)
            if form.exec_() == QDialog.Accepted:
                name, price = form.get_data()
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


# Form to handle adding and updating items
class ItemForm(QDialog):
    def __init__(self, parent=None, name='', price=0.0):
        super().__init__(parent)
        self.setWindowTitle('Item Form')
        self.setGeometry(400, 200, 300, 150)

        # Form Layout
        layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setText(name)

        self.price_input = QLineEdit(self)
        self.price_input.setText(str(price))

        layout.addRow('Name:', self.name_input)
        layout.addRow('Price:', self.price_input)

        # Button Box for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_data(self):
        name = self.name_input.text()
        price = float(self.price_input.text())
        return name, price


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
