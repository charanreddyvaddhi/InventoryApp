import sys
import pyodbc #For extenral Database Connection driver import SQL server related
from PyQt5.QtCore import (Qt,QSize)
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
    QLineEdit, QFormLayout, QDialog, QLabel, QDialogButtonBox, QMessageBox, QGridLayout, QGroupBox,QComboBox, QHeaderView, 
    QScrollArea, QTabWidget,QMainWindow,QFileDialog,  )
from PyQt5.QtGui import (QIcon) 
import pandas as pd
#==================================================================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inventory Management')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
                    QWidget, QMainWindow {background-color:#DCDCDC; font-family:Century Gothic;}
                    QLineEdit, QComboBox {padding:5px; background-color:#CCCCCC; border:2px solid #CCCCCC; border-radius:5px; }
                    QLineEdit:focus, QComboBox:focus {border:2px solid #4F008C;}
                    QPushButton {
                        background-color: #4F008C;
                        font-weight: bold; font-size: 15px;
                        color:white; border:none; border-radius:15px; padding:5px; 
                    }
                    QPushButton:hover {background-color:#0056B3;}
                    QLabel {font-size:14px; color:#333333; }
                    QTabWidget::pane { border: 1px solid #CCCCCC; }
                    QTabBar::tab {background: #E6E6E6; border: 1px solid #333333; padding: 8px 16px; border-radius: 10px; margin-right: 5px;}
                    QTabBar::tab:selected {background:#FFFFFF; border-bottom-color: #FFFFFF; }
                    QTabBar::tab:hover {background:#DCDCDC; }        
                """)    
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # Creating Tabs for each Tables 
        self.Inventory_tab = self.create_inventory_tab()
        self.windows_tab = self.create_windows_tab()
        self.node_tab = self.create_node_tab()
        self.sql_tab = self.create_sql_tab()
        self.application_tab = self.create_application_tab()

        # Add tabs to the main widget
        self.tab_widget.addTab(self.Inventory_tab, "All")
        self.tab_widget.addTab(self.windows_tab, "Windows Cluster")
        self.tab_widget.addTab(self.node_tab, "Node")
        self.tab_widget.addTab(self.sql_tab, "SQL Cluster")
        self.tab_widget.addTab(self.application_tab, "Application")

#==================================================================================================
    def create_inventory_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()#Heading Layout
        Heading = QLabel("MS-SQL Inventory")
        Heading.setAlignment(Qt.AlignCenter)
        Heading.setStyleSheet("font-size:30px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
        Head_layout.addWidget(Heading)

        button_layout = QHBoxLayout()#Button Layout
        view_button = QPushButton("View")
        add_button = QPushButton('Add')
        update_button = QPushButton("Update")
        delete_button = QPushButton("Delete")

        view_button.clicked.connect(self.view_Inventory)
        add_button.clicked.connect(self.add_Inventory)   
        update_button.clicked.connect(self.update_Inventory)
        delete_button.clicked.connect(self.delete_Inventory)

        button_layout.addWidget(view_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)

        button_size = QSize(80, 30)  # Set custom button size
        for button in [add_button, delete_button, update_button, view_button]:
            button.setFixedSize(button_size)  # Applying size to each botton 

        table_layout = QVBoxLayout()

        self.Inv_tab = QTableWidget(self)#Windows Cluster Table 
        self.Inv_tab.setColumnCount(28)
        self.Inv_tab.setHorizontalHeaderLabels(["WinClusterID","WinClusterIP","WinClusterName",
                                               "NodeID","Node-IP","Node-Name","Node-OSVersion","NodeComments","WindowsClusterID",
                                               "SQLClusterID","SQLClusterIP","SQLClusterName","SQLType","SQLInstanceName","SQLPort","SQLServerVersion","NARs-Raised","SQLComments","SQLServerEdition","MSDTCIP",
                                               "ApplicationID","AppName","AppOwner","AppOwnerEmail","AppVersion","AppDepartment","AppComments","AppCriticality"])
        table_layout.addWidget(self.Inv_tab)


        self.Inv_tab.verticalHeader().setDefaultSectionSize(400)
        self.Inv_tab.resizeRowsToContents()

        self.Inv_tab.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Inv_tab.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.Inv_tab.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.Inv_tab.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        main_layout.addLayout(Head_layout)
        main_layout.addLayout(button_layout)        
        main_layout.addLayout(table_layout) 

        tab.setLayout(main_layout)
        self.view_Inventory()#for automatically loading data when clicked on tab
        return tab
#==================================================================================================
    def create_windows_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()#Heading Layout
        Heading = QLabel("Windows Clusters")
        Heading.setAlignment(Qt.AlignCenter)
        Heading.setStyleSheet("font-size:30px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
        Head_layout.addWidget(Heading)

        button_layout = QHBoxLayout()#Button Layout
        view_button = QPushButton("View")
        add_button = QPushButton('Add')
        update_button = QPushButton("Update")
        delete_button = QPushButton("Delete")

        view_button.clicked.connect(self.view_windows_cluster)
        add_button.clicked.connect(self.add_windows_cluster)   
        update_button.clicked.connect(self.update_windows_cluster)
        delete_button.clicked.connect(self.delete_windows_cluster)

        button_layout.addWidget(view_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)

        button_size = QSize(80, 30)  # Set custom button size
        for button in [add_button, delete_button, update_button, view_button]:
            button.setFixedSize(button_size)  # Applying size to each botton 

        table_layout = QVBoxLayout()

        self.WinCTable = QTableWidget(self)#Windows Cluster Table 
        self.WinCTable.setColumnCount(3)
        self.WinCTable.setHorizontalHeaderLabels(["WinClusterID","WinClusterIP","WinClusterName"])
        table_layout.addWidget(self.WinCTable)

        main_layout.addLayout(Head_layout)
        main_layout.addLayout(button_layout)        
        main_layout.addLayout(table_layout) 

        tab.setLayout(main_layout)
        self.view_windows_cluster()#for automatically loading data when clicked on tab
        return tab
#==================================================================================================
    def create_node_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()#Heading Layout
        Heading = QLabel("VM/Nodes")
        Heading.setAlignment(Qt.AlignCenter)
        Heading.setStyleSheet("font-size:30px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
        Head_layout.addWidget(Heading)

        button_layout = QHBoxLayout()#Button Layout
        view_button = QPushButton("View")
        add_button = QPushButton('Add')
        update_button = QPushButton("Update")
        delete_button = QPushButton("Delete")

        add_button.clicked.connect(self.add_node)   
        delete_button.clicked.connect(self.delete_node)
        update_button.clicked.connect(self.update_node)
        view_button.clicked.connect(self.view_node)

        button_layout.addWidget(view_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)

        button_size = QSize(80, 30)  # Set custom button size
        for button in [add_button, delete_button, update_button, view_button]:
            button.setFixedSize(button_size)  # Applying size to each botton 

        table_layout = QVBoxLayout()

        self.NodeTable = QTableWidget(self) #VMs/Node
        self.NodeTable.setColumnCount(6)
        self.NodeTable.setHorizontalHeaderLabels(["NodeID","Node-IP","Node-Name","Node-OSVersion","NodeComments","WindowsClusterID"])
        table_layout.addWidget(self.NodeTable)

        main_layout.addLayout(Head_layout)
        main_layout.addLayout(button_layout)        
        main_layout.addLayout(table_layout) 

        tab.setLayout(main_layout)
        self.view_node()
        return tab
#==================================================================================================
    def create_sql_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()#Heading Layout
        Heading = QLabel("SQL Cluster")
        Heading.setAlignment(Qt.AlignCenter)
        Heading.setStyleSheet("font-size:30px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
        Head_layout.addWidget(Heading)

        button_layout = QHBoxLayout()#Button Layout
        view_button = QPushButton("View")
        add_button = QPushButton('Add')
        update_button = QPushButton("Update")
        delete_button = QPushButton("Delete")

        add_button.clicked.connect(self.add_sql_cluster)   
        delete_button.clicked.connect(self.delete_sql_cluster)
        update_button.clicked.connect(self.update_sql_cluster)
        view_button.clicked.connect(self.view_sql_cluster)

        button_layout.addWidget(view_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)

        button_size = QSize(80, 30)  # Set custom button size
        for button in [add_button, delete_button, update_button, view_button]:
            button.setFixedSize(button_size)  # Applying size to each botton 

        table_layout = QVBoxLayout()

        self.SQLCTable = QTableWidget(self) #SQL Clusters
        self.SQLCTable.setColumnCount(11)
        self.SQLCTable.setHorizontalHeaderLabels(["SQLClusterID","SQLClusterIP","SQLClusterName","SQLType","SQLInstanceName","SQLPort","SQLServerVersion","NARs-Raised","SQLComments","SQLServerEdition","MSDTCIP"])
        table_layout.addWidget(self.SQLCTable)

        main_layout.addLayout(Head_layout)
        main_layout.addLayout(button_layout)        
        main_layout.addLayout(table_layout) 

        tab.setLayout(main_layout)
        self.view_sql_cluster()
        return tab
#==================================================================================================
    def create_application_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()#Heading Layout
        Heading = QLabel("Applications")
        Heading.setAlignment(Qt.AlignCenter)
        Heading.setStyleSheet("font-size:30px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
        Head_layout.addWidget(Heading)

        button_layout = QHBoxLayout()#Button Layout
        view_button = QPushButton("View")
        add_button = QPushButton('Add')
        update_button = QPushButton("Update")
        delete_button = QPushButton("Delete")
        export_button = QPushButton("Export")        

        add_button.clicked.connect(self.add_application)   
        delete_button.clicked.connect(self.delete_application)
        update_button.clicked.connect(self.update_application)
        view_button.clicked.connect(self.view_application)
        export_button.clicked.connect(self.export_application_data)        

        button_layout.addWidget(view_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(export_button)

        button_size = QSize(80, 30)  # Set custom button size
        for button in [add_button, delete_button, update_button, view_button,export_button ]:
            button.setFixedSize(button_size)  # Applying size to each botton 

        table_layout = QVBoxLayout()

        self.AppTable = QTableWidget(self) #Applications
        self.AppTable.setColumnCount(8)
        self.AppTable.setHorizontalHeaderLabels(["ApplicationID","AppName","AppOwner","AppOwnerEmail","AppVersion","AppDepartment","AppComments","AppCriticality"])
        table_layout.addWidget(self.AppTable)

        main_layout.addLayout(Head_layout)
        main_layout.addLayout(button_layout)        
        main_layout.addLayout(table_layout) 

        tab.setLayout(main_layout)
        self.view_application()
        return tab
    
#==================================================================================================

    def export_application_data(self):
        data = []
            # Get the number of rows and columns in the table
        row_count = self.AppTable.rowCount()
        col_count = self.AppTable.columnCount()

        # Extract data from each cell in the table
        for row in range(row_count):
            row_data = {}
            for col in range(col_count):
                header = self.AppTable.horizontalHeaderItem(col).text()  # Get the column header
                item = self.AppTable.item(row, col)  # Get the cell item
                row_data[header] = item.text() if item else ''  # Handle empty cells
            data.append(row_data)

        # Prepare the data in dictionary format for export
        export_data = {'Application Data': data}

        # Call the export function with the collected data
        self.export_to_excel(export_data, 'Application Data')
#==================================================================================================
    def export_to_excel(self, data, sheet_name):
        # Create a pandas DataFrame
        df = pd.DataFrame(data)

        # Prompt the user for a file path
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)

        if file_path:
            # Save the DataFrame to an Excel file
            df.to_excel(file_path, sheet_name=sheet_name, index=False)
            print(f"Data exported to {file_path}")

#==================================================================================================
    def get_sql_connection(self):
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 13 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=Inv;'
            'UID=django;'
            'PWD=Charan@1999'
        )
        return conn
#==================================================================================================
    def add_Inventory(self):
        form = InventoryForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            print(f"Inserting Data: {data}")
            cursor.execute("INSERT INTO [dbo].[WindowsCluster] (WinClusterID, WinClusterIP, WinClusterName) VALUES (?, ?, ?)", data[:3])
            cursor.execute("INSERT INTO [dbo].[Node] (NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments) VALUES (?, ?, ?, ?, ?)", data[3:8])
            cursor.execute("INSERT INTO [dbo].[SQLCluster] (SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data[8:19])
            cursor.execute("INSERT INTO [dbo].[Application] ([ApplicationID],[AppName],[AppOwner],[AppOwnerEmail],[AppVersion],[AppDepartment],[AppComments],[AppCriticality]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data[19:27])
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Inventory Details added successfully.")
            self.view_Inventory()
#------------------------------------------------
    def delete_Inventory(self):
        print("functionality to be implmeeted ")
#------------------------------------------------
    def update_Inventory(self):
        print("functionality to be implmeeted ")         
#------------------------------------------------
    def view_Inventory(self):
        conn = self.get_sql_connection()    
        cursor = conn.cursor()
        cursor.execute("EXECUTE [dbo].[Select_All_Data]")
        rows1 = cursor.fetchall()        
        self.Inv_tab.setRowCount(len(rows1))
        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.Inv_tab.setItem(i, j, QTableWidgetItem(str(row[j])))
#==================================================================================================
    def add_windows_cluster(self):
        form = InventoryForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            print(f"Inserting Data: {data}")
            cursor.execute("INSERT INTO [dbo].[WindowsCluster] (WinClusterID, WinClusterIP, WinClusterName) VALUES (?, ?, ?)", data[:3])
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Windows Cluster added successfully.")
            self.view_windows_cluster()
#------------------------------------------------
    def delete_windows_cluster(self):
        del_selected_row = self.WinCTable.currentRow()
        if del_selected_row < 0:
            QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
            return
        conn = self.get_sql_connection()
        cursor = conn.cursor()
        try:
            current_WindowsClusterID = self.WinCTable.item(del_selected_row, 0).text() 
            print(f"Deleting WindowsCluster with ID: {current_WindowsClusterID}")
            cursor.execute("DELETE FROM [dbo].[WindowsCluster] WHERE WinClusterID=?", (current_WindowsClusterID,))
            conn.commit()
            QMessageBox.information(self, "Success", "Windows Cluster deleted successfully.")
            self.view_windows_cluster()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            conn.close()
#------------------------------------------------            
    def update_windows_cluster(self):
        del_selected_row = self.WinCTable.currentRow() 
        if del_selected_row < 0:
            QMessageBox.warning(self, "Update Item", "Please select an item to update.")
            return
        form = InventoryForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()  
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            print(f"Updating Data {data}")
            cursor.execute("UPDATE [dbo].[WindowsCluster] SET WinClusterIP=?, WinClusterName=? WHERE WinClusterID=?", (data[1], data[2], data[0]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Windows Cluster updated successfully.")
            self.view_node()
#------------------------------------------------
    def view_windows_cluster(self):
        conn = self.get_sql_connection()    
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [Inv].[dbo].[WindowsCluster]")
        rows1 = cursor.fetchall()        
        self.WinCTable.setRowCount(len(rows1))
        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.WinCTable.setItem(i, j, QTableWidgetItem(str(row[j])))
#==================================================================================================
    def add_node(self):
        form = InventoryForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            print(f"Inserting Data: {data}")
            cursor.execute("INSERT INTO [dbo].[Node] (NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments) VALUES (?, ?, ?, ?, ?)", data[3:8])
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Node added successfully.")
            self.view_node()
#------------------------------------------------
    def delete_node(self):
        del_selected_row = self.NodeTable.currentRow() 
        if del_selected_row < 0:
            QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
            return
        conn = self.get_sql_connection()
        cursor = conn.cursor()
        try:
            current_NodeID = self.NodeTable.item(del_selected_row, 0).text()
            print(f"Deleting WindowsCluster with ID: {current_NodeID}")
            cursor.execute("DELETE FROM [dbo].[Node] WHERE NodeID=?", (current_NodeID,))
            conn.commit()
            QMessageBox.information(self, "Success", "Node deleted successfully.")
            self.view_node()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            conn.close()
#------------------------------------------------
    def update_node(self):
        del_selected_row = self.NodeTable.currentRow() 
        if del_selected_row < 0:
            QMessageBox.warning(self, "Update Item", "Please select an item to update.")
            return
        form = InventoryForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            print(f"Updating Data {data}")
            cursor.execute("UPDATE [dbo].[Node] SET NodeIP=?, NodeName=?, NodeOSVersion=?, NodeComments=? WHERE NodeID=?", (data[4], data[5], data[6], data[7], data[3]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Node updated successfully.")
            self.view_windows_cluster()
#------------------------------------------------
    def view_node(self):
        conn = self.get_sql_connection()    
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [Inv].[dbo].[Node]")
        rows1 = cursor.fetchall()        
        self.NodeTable.setRowCount(len(rows1))
        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.NodeTable.setItem(i, j, QTableWidgetItem(str(row[j])))
#==================================================================================================
    def add_sql_cluster(self):
        form = InventoryForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO [dbo].[SQLCluster] (SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data[8:19])
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "SQL Cluster added successfully.")
            self.view_sql_cluster()
#------------------------------------------------
    def delete_sql_cluster(self):
        del_selected_row = self.SQLCTable.currentRow()
        if del_selected_row < 0:
            QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
            return
        conn = self.get_sql_connection()
        cursor = conn.cursor()
        try:
            current_SQLClusterID = self.SQLCTable.item(del_selected_row, 0).text()
            print(f"Deleting SQLCluster with ID: {del_selected_row}")
            cursor.execute("DELETE FROM [dbo].[SQLCluster] WHERE SQLClusterID=?", (current_SQLClusterID,))
            conn.commit()
            QMessageBox.information(self, "Success", "SQL Cluster deleted successfully.")
            self.view_sql_cluster()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            conn.close()
#------------------------------------------------
    def update_sql_cluster(self):
        del_selected_row = self.SQLCTable.currentRow()
        if del_selected_row < 0:
            QMessageBox.warning(self, "Update Item", "Please select an item to update.")
            return
        form = InventoryForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            print(f"Updating Data {data}")
            cursor.execute("UPDATE [dbo].[SQLCluster] SET SQLClusterIP=?, SQLClusterName=?, SQLType=?, SQLInstanceName=?, SQLPort=?, SQLServerVersion=?, NARsRaised=?, SQLComments=?, SQLServerEdition=?, MSDTCIP=? WHERE SQLClusterID=?", (data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[8]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "SQL Cluster updated successfully.")
            self.view_sql_cluster()
#------------------------------------------------
    def view_sql_cluster(self):
        conn = self.get_sql_connection()    
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [Inv].[dbo].[SQLCluster]")
        rows1 = cursor.fetchall()        
        self.SQLCTable.setRowCount(len(rows1))
        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.SQLCTable.setItem(i, j, QTableWidgetItem(str(row[j])))
#==================================================================================================
    def add_application(self):
        form = InventoryForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            print(f"Inserting Data: {data}")            
            cursor.execute("INSERT INTO [dbo].[Application] ([ApplicationID],[AppName],[AppOwner],[AppOwnerEmail],[AppVersion],[AppDepartment],[AppComments],[AppCriticality]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data[19:27])
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Application added successfully.")
            self.view_application()
#------------------------------------------------
    def delete_application(self):
        del_selected_row = self.AppTable.currentRow()
        if del_selected_row < 0:
            QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
            return
        conn = self.get_sql_connection()
        cursor = conn.cursor()
        try:
            current_AppID = self.AppTable.item(del_selected_row, 0).text() 
            print(f"Deleting WindowsCluster with ID: {current_AppID}")
            cursor.execute("DELETE FROM [dbo].[Application] WHERE ApplicationID=?", (current_AppID,))
            conn.commit()
            QMessageBox.information(self, "Success", "Application deleted successfully.")
            self.view_application()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            conn.close()
#------------------------------------------------
    def update_application(self):
        del_selected_row = self.AppTable.currentRow()
        if del_selected_row < 0:
            QMessageBox.warning(self, "Update Item", "Please select an item to update.")
            return
        form = InventoryForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            print(f"Updating Data {data}")            
            cursor.execute("UPDATE [dbo].[Application] SET AppName=?, AppOwner=?, AppOwnerEmail=?, AppVersion=?, AppDepartment=?, AppComments=?, AppCriticality=? WHERE ApplicationID=?", (data[20], data[21], data[22], data[23], data[24], data[25], data[26], data[19]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Application updated successfully.")
            self.view_application()
#------------------------------------------------
    def view_application(self):
        conn = self.get_sql_connection()    
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [Inv].[dbo].[Application]")
        rows1 = cursor.fetchall()        
        self.AppTable.setRowCount(len(rows1))
        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.AppTable.setItem(i, j, QTableWidgetItem(str(row[j])))
#==================================================================================================
class InventoryForm(QDialog):
    def __init__(self, parent=None, 
                 WindowsClusterID=0, WindowsClusterIP='***.***.***.***', WindowsClusterName='.stc.corp',
                 NodeID=0, NodeIP='***.***.***.***', NodeName='.stc.corp', NodeOSVersion='', NodeComments='None', 
                 SQLClusterID=0, SQLClusterIP='***.***.***.***', SQLClusterName='', SQLType='', SQLInstanceName='', SQLPort='1433', SQLServerVersion='Microsft SQL Server ***',  NARsRaised='', SQLComments='None', SQLServerEdition='', MSDTCIP='',
                 ApplicationID=0, AppName='', AppOwner='', AppOwnerEmail='', AppVersion='', AppDepartment='', AppComments='None', AppCriticality=''):
        super().__init__(parent)
        self.setWindowTitle('Inventory Form')
        self.setGeometry(50, 50, 700, 700)
        self.setStyleSheet("""
                    QWidget, QMainWindow {background-color:#DCDCDC; font-family:Century Gothic;}
                    QLineEdit, QComboBox {padding:5px; background-color:#CCCCCC; border:2px solid #CCCCCC; border-radius:5px;}
                    QLineEdit:focus, QComboBox:focus {border:2px solid #4F008C;}
                    QPushButton,QDialogButtonBox {
                    background-color: #4F008C;
                    font-weight: bold; font-size: 15px;
                    color:white; border:none; border-radius:10px; padding:5px;
                    }
                    QPushButton:hover,QDialogButtonBox:hover {background-color:#0056B3;}
                    QLabel {font-size:14px; color:#333333; }
                    """)         
        self.tab_widget = QTabWidget(self)#for seperae Tab 

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
