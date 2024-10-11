import sys
import pyodbc
from PyQt5.QtCore import (Qt)
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

        Head_layout = QVBoxLayout()
        Heading = QLabel("MS-SQL Inventory")
        Heading.setAlignment(Qt.AlignCenter)
        Heading.setStyleSheet("""font-size: 30px;
                              font-weight: bold; 
                              text-decoration: underline;
                              font-family: Century Gothic""")
        Head_layout.addWidget(Heading)

        # Create the button layout (horizontal layout)
        button_layout = QHBoxLayout()

        # CRUD Buttons
        self.refresh_button = QPushButton('Show Details')
        self.add_button = QPushButton('Add New ')
        self.update_button = QPushButton('Update ')
        self.delete_button = QPushButton('Delete ')

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

        table_layout = QVBoxLayout()
        
        
        # Create the table to display SQL Server data
        self.table1 = QTableWidget(self) #Windows Cluster
        self.table1.setColumnCount(3)
        self.table1.setHorizontalHeaderLabels(["WinClusterID","WinClusterIP","WinClusterName"])
        
        self.table2 = QTableWidget(self) #VMs/Node
        self.table2.setColumnCount(6)
        self.table2.setHorizontalHeaderLabels(["NodeID","Node-IP","Node-Name","Node-OSVersion","NodeComments","WindowsClusterID"])

        self.table3 = QTableWidget(self) #SQL Clusters
        self.table3.setColumnCount(11)
        self.table3.setHorizontalHeaderLabels(["SQLClusterID","SQLClusterIP","SQLClusterName","SQLType","SQLInstanceName","SQLPort","SQLServerVersion","NARs-Raised","SQLComments","SQLServerEdition","MSDTCIP"])
        
        self.table4 = QTableWidget(self) #Applications
        self.table4.setColumnCount(8)
        self.table4.setHorizontalHeaderLabels(["ApplicationID","AppName","AppOwner","AppOwnerEmail","AppVersion","AppDepartment","AppComments","AppCriticality"])

        table1_head = QLabel("Windows Clusters")
        table1_head.setStyleSheet("""font-size: 15px;
                              font-weight: bold; 
                              text-decoration: underline;
                              font-family: Century Gothic""")
        table_layout.addWidget(table1_head)
        table_layout.addWidget(self.table1)

        table2_head = QLabel("VMs/Nodes")
        table2_head.setStyleSheet("""font-size: 15px;
                              font-weight: bold; 
                              text-decoration: underline;
                              font-family: Century Gothic""")
        table_layout.addWidget(table2_head)
        table_layout.addWidget(self.table2)

        table3_head = QLabel("SQL Cluster")
        table3_head.setStyleSheet("""font-size: 15px;
                              font-weight: bold; 
                              text-decoration: underline;
                              font-family: Century Gothic""")
        table_layout.addWidget(table3_head)
        table_layout.addWidget(self.table3)

        table4_head = QLabel("Applications")
        table4_head.setStyleSheet("""font-size: 15px;
                              font-weight: bold; 
                              text-decoration: underline;
                              font-family: Century Gothic""")        
        table_layout.addWidget(table4_head)
        table_layout.addWidget(self.table4)

        # Add the button layout and table to the main layout
        main_layout.addLayout(Head_layout)
        main_layout.addLayout(button_layout)  # Button layout on top
        main_layout.addLayout(table_layout)  # Button layout on top


        # Adjust layout spacing and margins
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(15, 15, 15, 15)

        table_layout.setSpacing(10)
        table_layout.setContentsMargins(15, 15, 15, 15)

        # Set the main layout on the window
        self.setLayout(main_layout)

    # Define Database Connection
    def get_sql_connection(self):
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 13 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=Inv;'
            'UID=django;'
            'PWD=Charan@1999'
        )
        return conn

    def show_data(self):
        conn = self.get_sql_connection()
        cursor = conn.cursor()
    #-----------------------------------------------------------------
        cursor.execute("""SELECT * FROM [Inv].[dbo].[WindowsCluster]""")
        rows1 = cursor.fetchall()
        #self.table_name_label.setText("Table: Windows ") 
        self.table1.setRowCount(len(rows1))

        for i, row in enumerate(rows1):
            self.table1.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table1.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.table1.setItem(i, 2, QTableWidgetItem(str(row[2])))
    #-----------------------------------------------------------------
        cursor.execute("SELECT * FROM [Inv].[dbo].[Node]")
        rows2 = cursor.fetchall()
        self.table2.setRowCount(len(rows2))

        for i, row in enumerate(rows2):
            self.table2.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table2.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.table2.setItem(i, 2, QTableWidgetItem(str(row[2])))
            self.table2.setItem(i, 3, QTableWidgetItem(str(row[3])))
            self.table2.setItem(i, 4, QTableWidgetItem(str(row[4])))
            self.table2.setItem(i, 5, QTableWidgetItem(str(row[5])))                    
    #-----------------------------------------------------------------
        cursor.execute("SELECT *  FROM [Inv].[dbo].[SQLCluster]")
        rows3 = cursor.fetchall()
        self.table3.setRowCount(len(rows3))
      
        for i, row in enumerate(rows3):
            self.table3.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table3.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.table3.setItem(i, 2, QTableWidgetItem(str(row[2]))) 
            self.table3.setItem(i, 3, QTableWidgetItem(str(row[3])))
            self.table3.setItem(i, 4, QTableWidgetItem(str(row[4])))
            self.table3.setItem(i, 5, QTableWidgetItem(str(row[5]))) 
            self.table3.setItem(i, 6, QTableWidgetItem(str(row[6])))
            self.table3.setItem(i, 7, QTableWidgetItem(str(row[7])))
            self.table3.setItem(i, 8, QTableWidgetItem(str(row[8]))) 
            self.table3.setItem(i, 9, QTableWidgetItem(str(row[9])))
            self.table3.setItem(i, 10, QTableWidgetItem(str(row[10])))                     
    #-----------------------------------------------------------------
        cursor.execute("SELECT *  FROM [Inv].[dbo].[Application]")
        rows4 = cursor.fetchall()
        self.table4.setRowCount(len(rows4))

        for i, row in enumerate(rows4):
            self.table4.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table4.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.table4.setItem(i, 2, QTableWidgetItem(str(row[2])))
            self.table4.setItem(i, 3, QTableWidgetItem(str(row[3])))
            self.table4.setItem(i, 4, QTableWidgetItem(str(row[4])))
            self.table4.setItem(i, 5, QTableWidgetItem(str(row[5])))
            self.table4.setItem(i, 6, QTableWidgetItem(str(row[6])))
            self.table4.setItem(i, 7, QTableWidgetItem(str(row[7])))                   
#-----------------------------------------------------------------      
        conn.close()

    def open_add_form(self):
        form = InventoryForm(self)
        if form.exec_() == QDialog.Accepted:
            name, price = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))
            conn.commit()
            conn.close()
            self.show_data()

    def open_update_form(self):
        selected_row = self.table1.currentRow()
        if selected_row >= 0:
            id = self.table1.item(selected_row, 0).text()
            current_name = self.table1.item(selected_row, 1).text()
            current_price = float(self.table1.item(selected_row, 2).text())

            form = InventoryForm(self, current_name, current_price)
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
        selected_row = self.table1.currentRow()
        if selected_row >= 0:
            id = self.table1.item(selected_row, 0).text()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE id=?", (id,))
            conn.commit()
            conn.close()
            self.show_data()
        else:
            QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")


# Form to handle adding and updating items
class InventoryForm(QDialog):
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
        button_box.accepted.connect(self.accept) #is for Okay   
        button_box.rejected.connect(self.reject) #is for cancel  

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
