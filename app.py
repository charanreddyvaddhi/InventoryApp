import sys
import pyodbc
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QInputDialog, QMessageBox
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        #self.show_data()

 #related to layout of application when its opening initially 
    def initUI(self):
        self.setWindowTitle('Inventory')

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

        #Sizes of CRUD Buttons 
        self.refresh_button.setFixedSize(100, 30)
        self.add_button.setFixedSize(100, 30)
        self.update_button.setFixedSize(100, 30)
        self.delete_button.setFixedSize(100, 30)

        #Connect buttons to methods
        self.refresh_button.clicked.connect(self.show_data)
        self.add_button.clicked.connect(self.add_item)
        self.update_button.clicked.connect(self.update_item)
        self.delete_button.clicked.connect(self.delete_item)

        # Add buttons to the button layout
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        # Create the table to display SQL Server data
        self.table1 = QTableWidget(self)
        self.table1.setColumnCount(3)
        self.table1.setHorizontalHeaderLabels(["ID", "Name", "Price"])

        self.table2 = QTableWidget(self)
        self.table2.setColumnCount(3)
        self.table2.setHorizontalHeaderLabels(["ID", "Name", "Price"])

        # Add the button layout and table to the main layout
        main_layout.addLayout(button_layout)  # Button layout on top
        main_layout.addWidget(self.table1)      # Table below buttons
        main_layout.addWidget(self.table2)      # Table below buttons

        # Adjust layout spacing and margins
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(15, 15, 15, 15)

        # Set the main layout on the window
        self.setLayout(main_layout)

    #defining Database Connection
    def get_sql_connection(self):
        # Adjust these settings based on your SQL Server configuration
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
        rows1 = cursor.fetchall()
        
        cursor.execute("SELECT id, username FROM users")   
        rows2 = cursor.fetchall()

        #total_rows = len(rows1) + len(rows2)
        #self.table.setRowCount(total_rows)

        self.table1.setRowCount(len(rows1)+len(rows2))

        for i, row in enumerate(rows1):
            self.table1.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table1.setItem(i, 1, QTableWidgetItem(row[1]))
            self.table1.setItem(i, 2, QTableWidgetItem(str(row[2])))

        self.table2.setRowCount(len(rows1)+len(rows2))
        for i, row in enumerate(rows2,start=len(rows1)):
            self.table2.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table2.setItem(i, 1, QTableWidgetItem(row[1]))
            self.table2.setItem(i, 2, QTableWidgetItem(''))

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
