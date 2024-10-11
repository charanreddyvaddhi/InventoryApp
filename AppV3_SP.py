import sys
import pyodbc
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QFormLayout, QDialog, QLabel, QDialogButtonBox, QMessageBox, QGridLayout, QGroupBox,QComboBox  
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show_data()

    def initUI(self):
        self.setWindowTitle('Inventory-V3') #Setting Crud BUttons for Windows Cluster using stored Procedures
        
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
        self.refresh_button = QPushButton('Refresh ')
        self.add_button = QPushButton('Add New ')
        self.update_button = QPushButton('Update Existing ')
        self.delete_button = QPushButton('Delete ')

        # Sizes of CRUD Buttons
        self.refresh_button.setFixedSize(100, 30)
        self.add_button.setFixedSize(100, 30)
        self.update_button.setFixedSize(100, 30)
        self.delete_button.setFixedSize(100, 30)

        # Connect buttons to methods
        #self.refresh_button.clicked.connect(self.show_data)
        #self.add_button.clicked.connect(self.open_add_form)
        #self.update_button.clicked.connect(self.open_update_form)
        #self.delete_button.clicked.connect(self.delete_item)

        # Add buttons to the button layout
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        table_layout = QVBoxLayout()
        
        
        # Create the table to display SQL Server data
        self.table1 = QTableWidget(self) #Windows Cluster
        self.table1.setColumnCount(28)
        self.table1.setHorizontalHeaderLabels(["WinClusterID","WinClusterIP","WinClusterName",
                                               "NodeID","Node-IP","Node-Name","Node-OSVersion","NodeComments","WindowsClusterID",
                                               "SQLClusterID","SQLClusterIP","SQLClusterName","SQLType","SQLInstanceName","SQLPort","SQLServerVersion","NARs-Raised","SQLComments","SQLServerEdition","MSDTCIP",
                                               "ApplicationID","AppName","AppOwner","AppOwnerEmail","AppVersion","AppDepartment","AppComments","AppCriticality"])
        
        table1_head = QLabel("Inventory")
        table1_head.setStyleSheet("""font-size: 15px;
                              font-weight: bold; 
                              text-decoration: underline;
                              font-family: Century Gothic""")
        table_layout.addWidget(table1_head)
        table_layout.addWidget(self.table1)

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

        # Execute the stored procedure to fetch all records
        cursor.execute("""EXECUTE [dbo].[Select_All_Data]""")
        rows1 = cursor.fetchall()

        # Set the row count to match the number of fetched rows
        self.table1.setRowCount(len(rows1))

        # Add items to the table
        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.table1.setItem(i, j, QTableWidgetItem(str(row[j])))

        # Now implement the merging logic
        def merge_cells(col_index):
            """Helper function to merge cells in a specific column when values are the same."""
            previous_text = None
            start_row = 0
            span_count = 1

            for row in range(self.table1.rowCount()):
                current_text = self.table1.item(row, col_index).text()
            
                # If the current cell is the same as the previous one, increase the span
                if current_text == previous_text:
                    span_count += 1
                else:
                    # If span count > 1, merge the previous cells
                    if span_count > 1:
                        self.table1.setSpan(start_row, col_index, span_count, 1)
                        # Clear redundant items in the merged rows
                        for clear_row in range(start_row + 1, start_row + span_count):
                            self.table1.setItem(clear_row, col_index, None)
                
                    # Reset span tracking
                    start_row = row
                    span_count = 1
                    previous_text = current_text

            # Final merge for the last set of cells
            if span_count > 1:
                self.table1.setSpan(start_row, col_index, span_count, 1)
                for clear_row in range(start_row + 1, start_row + span_count):
                    self.table1.setItem(clear_row, col_index, None)

        # Specify the columns you want to merge cells for (e.g., WinClusterID and WinClusterName)
        columns_to_merge = [0,1,2,3,4,5,6,8,9]  # Adjust column indices as needed

        #columns_to_merge = range(self.table1.columnCount())

        # Apply the merge logic for each column specified
        for col in columns_to_merge:
            merge_cells(col)

        conn.close()


    
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
