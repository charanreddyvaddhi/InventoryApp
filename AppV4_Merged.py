import sys
import pyodbc
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
    QLineEdit, QFormLayout, QDialog, QLabel, QDialogButtonBox, QMessageBox, QGridLayout, QGroupBox,QComboBox, QHeaderView, 
    QScrollArea, QTabWidget,   
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        #self.show_data()

    def initUI(self):
        self.setWindowTitle('Inventory-V4') #Setting Crud BUttons for Windows Cluster 
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
                    QWidget {background-color:#DCDCDC; font-family:Century Gothic;}
                    QLineEdit, QComboBox {padding:5px; background-color:#CCCCCC; border:2px solid #CCCCCC; border-radius:5px;}
                    QLineEdit:focus, QComboBox:focus {border:2px solid #4F008C;}
                    QPushButton {
                        background-color: #4F008C;
                        font-weight: bold; font-size: 15px;
                        color:white; border:none; border-radius:10px; padding:5px;
                    }
                    QPushButton:hover {background-color:#0056B3;}
                    QLabel {font-size:14px; color:#333333; }
                """)

        # Create the main vertical layout
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()
        Heading = QLabel("MS-SQL Inventory")
        Heading.setAlignment(Qt.AlignCenter)
        Heading.setStyleSheet("font-size:30px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
        Head_layout.addWidget(Heading)

        # Create the button layout (horizontal layout)
        button_layout = QHBoxLayout()

        # CRUD Buttons
        self.refresh_button = QPushButton('Refresh')
        self.add_button = QPushButton('Add')
        self.update_button = QPushButton('Update')
        self.delete_button = QPushButton('Delete')

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

        self.table5 = QTableWidget(self) #ALL
        self.table5.setColumnCount(28)
        self.table5.setHorizontalHeaderLabels(["WinClusterID","WinClusterIP","WinClusterName",
                                               "NodeID","Node-IP","Node-Name","Node-OSVersion","NodeComments","WindowsClusterID",
                                               "SQLClusterID","SQLClusterIP","SQLClusterName","SQLType","SQLInstanceName","SQLPort","SQLServerVersion","NARs-Raised","SQLComments","SQLServerEdition","MSDTCIP",
                                               "ApplicationID","AppName","AppOwner","AppOwnerEmail","AppVersion","AppDepartment","AppComments","AppCriticality"])

        self.table5.verticalHeader().setDefaultSectionSize(400)
        self.table5.resizeRowsToContents()

        self.table5.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table5.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table5.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table5.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        scroll_area = QScrollArea(self) #For Scroll   
        scroll_area.setWidgetResizable(True)  #For Scroll
        
        scroll_area.setStyleSheet("QScrollArea { border:none; border-radius:10px}")

        main_widget = QWidget() #For Scroll
        main_widget.setLayout(main_layout) #For Scroll

        scroll_area.setWidget(main_widget) #For Scroll

        self.setLayout(QVBoxLayout()) #For Scroll
        self.layout().addWidget(scroll_area) #For Scroll

        table1_head = QLabel("Windows Clusters")
        table1_head.setStyleSheet("font-size:15px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
        table_layout.addWidget(table1_head)
        table_layout.addWidget(self.table1)

        table2_head = QLabel("VMs/Nodes")
        table2_head.setStyleSheet("font-size:15px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
        table_layout.addWidget(table2_head)
        table_layout.addWidget(self.table2)

        table3_head = QLabel("SQL Cluster")
        table3_head.setStyleSheet("font-size:15px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
        table_layout.addWidget(table3_head)
        table_layout.addWidget(self.table3)

        table4_head = QLabel("Applications")
        table4_head.setStyleSheet("font-size:15px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")        
        table_layout.addWidget(table4_head)
        table_layout.addWidget(self.table4)

        table5_head = QLabel("Inventory -- ALL")
        table5_head.setStyleSheet("font-size:15px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
        table_layout.addWidget(table5_head)
        table_layout.addWidget(self.table5)

        # Add the button layout and table to the main layout
        main_layout.addLayout(Head_layout)
        main_layout.addLayout(button_layout)  # Button layout on top
        main_layout.addLayout(table_layout)  # Button layout on top


        # Adjust layout spacing and margins
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(15, 15, 15, 15)

        table_layout.setSpacing(10)
        table_layout.setContentsMargins(30, 30, 30, 30)

        # Set the main layout on the window
        self.setLayout(main_layout)
        self.table5.resizeRowsToContents()
        self.table5.horizontalHeader().setStretchLastSection(True)
        self.table5.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
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
        cursor.execute("SELECT * FROM [Inv].[dbo].[WindowsCluster]")
        rows1 = cursor.fetchall()
        #self.table_name_label.setText("Table: Windows ") 
        self.table1.setRowCount(len(rows1))

        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.table1.setItem(i, j, QTableWidgetItem(str(row[j])))
    #-----------------------------------------------------------------
        cursor.execute("SELECT * FROM [Inv].[dbo].[Node]")
        rows2 = cursor.fetchall()
        self.table2.setRowCount(len(rows2))

        for i, row in enumerate(rows2):
            for j in range(len(row)):
                self.table2.setItem(i, j, QTableWidgetItem(str(row[j])))                   
    #-----------------------------------------------------------------
        cursor.execute("SELECT *  FROM [Inv].[dbo].[SQLCluster]")
        rows3 = cursor.fetchall()
        self.table3.setRowCount(len(rows3))
      
        for i, row in enumerate(rows3):
            for j in range(len(row)):
                self.table3.setItem(i, j, QTableWidgetItem(str(row[j])))                    
    #-----------------------------------------------------------------
        cursor.execute("SELECT *  FROM [Inv].[dbo].[Application]")
        rows4 = cursor.fetchall()
        self.table4.setRowCount(len(rows4))

        for i, row in enumerate(rows4):
            for j in range(len(row)):
                self.table4.setItem(i, j, QTableWidgetItem(str(row[j]))) 
    #-----------------------------------------------------------------   
        cursor.execute("EXECUTE [dbo].[Select_All_Data]")
        rows5 = cursor.fetchall()
        self.table5.setRowCount(len(rows5))

        # Add items to the table
        for i, row in enumerate(rows5):
            for j in range(len(row)):
                self.table5.setItem(i, j, QTableWidgetItem(str(row[j])))
#-----------------------------------------------------------------      
        conn.close()

    def open_add_form(self):
        form = InventoryForm(self)
        if form.exec_() == QDialog.Accepted:
            (WindowsClusterID, WindowsClusterIP, WindowsClusterName, 
            NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments,
            SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP,
            ApplicationID, AppName, AppOwner, AppOwnerEmail, AppVersion, AppDepartment, AppComments, AppCriticality) = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                        INSERT INTO [dbo].[WindowsCluster] (WinClusterID,WinClusterIP,WinClusterName) 
                        VALUES (?, ?, ?)""", (WindowsClusterID, WindowsClusterIP, WindowsClusterName))
            cursor.execute("""
                        INSERT INTO [dbo].[Node] (NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments) 
                        VALUES (?, ?, ?, ?, ?)""", (NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments))
            cursor.execute("""
                        INSERT INTO [dbo].[SQLCluster] (SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP))
            cursor.execute("""
                        INSERT INTO [dbo].[Application] (ApplicationID, AppName, AppOwner, AppOwnerEmail, AppVersion, AppDepartment, AppComments, AppCriticality) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (ApplicationID, AppName, AppOwner, AppOwnerEmail, AppVersion, AppDepartment, AppComments, AppCriticality))
            
            conn.commit()
            conn.close()
            self.show_data()

    def open_update_form(self):
        selected_row1 = self.table1.currentRow()
        selected_row2 = self.table2.currentRow()
        selected_row3 = self.table3.currentRow()
        selected_row4 = self.table4.currentRow()
        
        if selected_row1 >= 0:
            #id = self.table1.item(selected_row, 0).text()
            current_WindowsClusterID = self.table1.item(selected_row1, 0).text()if self.table1.item(selected_row1, 0) else ""
            current_WindowsClusterIP = self.table1.item(selected_row1, 1).text()if self.table1.item(selected_row1, 0) else ""
            current_WindowsClusterName = self.table1.item(selected_row1, 2).text()if self.table1.item(selected_row1, 0) else ""

            current_NodeID = self.table2.item(selected_row2, 0).text()if self.table2.item(selected_row2, 0) else ""
            current_NodeIP = self.table2.item(selected_row2, 1).text()if self.table2.item(selected_row2, 1) else ""
            current_NodeName = self.table2.item(selected_row2, 2).text()if self.table2.item(selected_row2, 2) else ""
            current_NodeOSVersion = self.table2.item(selected_row2, 3).currentText()if self.table2.item(selected_row2, 3) else ""
            current_NodeComments = self.table2.item(selected_row2, 4).text() if self.table2.item(selected_row2, 4) else ""

            current_SQLClusterID = self.table3.item(selected_row3, 0).text()if self.table3.item(selected_row3, 0) else ""
            current_SQLClusterIP = self.table3.item(selected_row3, 1).text()if self.table3.item(selected_row3, 1) else ""
            current_SQLClusterName = self.table3.item(selected_row3, 2).text()if self.table3.item(selected_row3, 2) else "" 
            current_SQLType = self.table3.item(selected_row3, 3).text()if self.table3.item(selected_row3, 3) else "" 
            current_SQLInstanceName = self.table3.item(selected_row3, 4).text()if self.table3.item(selected_row3, 4) else "" 
            current_SQLPort = self.table3.item(selected_row3, 5).text()if self.table3.item(selected_row3, 5) else "" 
            current_SQLServerVersion = self.table3.item(selected_row3, 6).currentText()if self.table3.item(selected_row3, 6) else "" 
            current_NARsRaised = self.table3.item(selected_row3, 7).text()if self.table3.item(selected_row3, 7) else "" 
            current_SQLComments = self.table3.item(selected_row3, 8).text()if self.table3.item(selected_row3, 8) else "" 
            current_SQLServerEdition = self.table3.item(selected_row3, 9).currentText()if self.table3.item(selected_row3, 9) else "" 
            current_MSDTCIP = self.table3.item(selected_row3, 10).text()if self.table3.item(selected_row3, 10) else ""

            current_ApplicationID = self.table4.item(selected_row4, 0).text()if self.table4.item(selected_row4, 0) else "" 
            current_AppName = self.table4.item(selected_row4, 1).text()if self.table4.item(selected_row4, 1) else "" 
            current_AppOwner = self.table4.item(selected_row4, 2).text()if self.table4.item(selected_row4, 2) else "" 
            current_AppOwnerEmail = self.table4.item(selected_row4, 3).text()if self.table4.item(selected_row4, 3) else "" 
            current_AppVersion = self.table4.item(selected_row4, 4).text()if self.table4.item(selected_row4, 4) else "" 
            current_AppDepartment = self.table4.item(selected_row4, 5).currentText()if self.table4.item(selected_row4, 5) else "" 
            current_AppComments = self.table4.item(selected_row4, 6).text()if self.table4.item(selected_row4, 6) else "" 
            current_AppCriticality = self.table2.item(selected_row4, 7).text()if self.table4.item(selected_row4, 7) else ""

            form = InventoryForm(self, current_WindowsClusterID, current_WindowsClusterIP,current_WindowsClusterName,
                                 current_NodeID, current_NodeIP,current_NodeName, current_NodeOSVersion, current_NodeComments,
                                 current_SQLClusterID, current_SQLClusterIP, current_SQLClusterName, current_SQLType, current_SQLInstanceName, current_SQLPort, current_SQLServerVersion, current_NARsRaised, current_SQLComments, current_SQLServerEdition, current_MSDTCIP,
                                 current_ApplicationID, current_AppName, current_AppOwner, current_AppOwnerEmail, current_AppVersion, current_AppDepartment, current_AppComments, current_AppCriticality,)
            if form.exec_() == QDialog.Accepted:
                (WindowsClusterID, WindowsClusterIP, WindowsClusterName, 
                NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments,
                SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP,
                ApplicationID, AppName, AppOwner, AppOwnerEmail, AppVersion, AppDepartment, AppComments, AppCriticality) = form.get_data()
                try:
                    conn = self.get_sql_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE [dbo].[WindowsCluster] SET WinClusterID=?, WinClusterIP=?, WinClusterName =? WHERE WinClusterID=?", (WindowsClusterID, WindowsClusterIP, WindowsClusterName, current_WindowsClusterID))
                    cursor.execute("UPDATE [dbo].[Node] SET NodeID=?, NodeIP=?, NodeName=?, NodeOSVersion=?, NodeComments=? WHERE NodeID=?", (NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments, current_NodeID))
                    cursor.execute("UPDATE [dbo].[SQLCluster] SET SQLClusterID=?, SQLClusterIP=?, SQLClusterName=?, SQLType=?, SQLInstanceName=?, SQLPort=?, SQLServerVersion=?, NARsRaised=?, SQLComments=?, SQLServerEdition=?, MSDTCIP=? WHERE SQLClusterID=?", (SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP, current_SQLClusterID))
                    cursor.execute("UPDATE [dbo].[Application] SET ApplicationID=?, AppName=?, AppOwner=?, AppOwnerEmail=?, AppVersion=?, AppDepartment=?, AppComments=?, AppCriticality=? where ApplicationID=?", (ApplicationID, AppName, AppOwner, AppOwnerEmail, AppVersion, AppDepartment, AppComments, AppCriticality,current_ApplicationID))
                    
                    conn.commit()
                except Exception as e:
                    QMessageBox.critical(self, "Database Error", str(e))
                finally:    
                    conn.close()
                self.show_data()
        else:
            QMessageBox.warning(self, "Update Item", "Please select an item to update.")

    def delete_item(self):
        del_selected_row1 = self.table1.currentRow()
        #print(del_selected_row1)
        del_selected_row2 = self.table2.currentRow()
        #print(del_selected_row2)
        del_selected_row3 = self.table3.currentRow()
        #print(del_selected_row3)
        del_selected_row4 = self.table4.currentRow()
        #print(del_selected_row4)
    # Check if any row is selected
        if del_selected_row1 < 0 and del_selected_row2 < 0 and del_selected_row3 < 0 and del_selected_row4 < 0:
            QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
            return  # Early exit if no rows are selected

        conn = self.get_sql_connection()
        cursor = conn.cursor()
        try:
        # Delete from WindowsCluster if selected
            if del_selected_row1 >= 0:
                current_WindowsClusterID = self.table1.item(del_selected_row1, 0).text() 
                print(f"Deleting WindowsCluster with ID: {current_WindowsClusterID}")
                cursor.execute("DELETE FROM [dbo].[WindowsCluster] WHERE WinClusterID=?", (current_WindowsClusterID,))
                #del_selected_row1 = -1; del_selected_row2 = -1; del_selected_row3 = -1; del_selected_row4 = -1 #resetting the value for next occurance 
        # Delete from Node if selected
            if del_selected_row2 >= 0:
                current_NodeID = self.table2.item(del_selected_row2, 0).text() 
                print(f"Deleting Node with ID: {current_NodeID}")
                cursor.execute("DELETE FROM [dbo].[Node] WHERE NodeID=?", (current_NodeID,))
                #del_selected_row1 = -1; del_selected_row2 = -1; del_selected_row3 = -1; del_selected_row4 = -1#resetting the value for next occurance
        # Delete from SQLCluster if selected
            if del_selected_row3 >= 0:
                current_SQLClusterID = self.table3.item(del_selected_row3, 0).text() 
                print(f"Deleting SQLCluster with ID: {current_SQLClusterID}")
                cursor.execute("DELETE FROM [dbo].[SQLCluster] WHERE SQLClusterID=?", (current_SQLClusterID,))
                #del_selected_row1 = -1; del_selected_row2 = -1; del_selected_row3 = -1; del_selected_row4 = -1#resetting the value for next occurance
        # Delete from Application if selected
            if del_selected_row4 >= 0:
                current_ApplicationID = self.table4.item(del_selected_row4, 0).text()
                print(f"Deleting Application with ID: {current_ApplicationID}")
                cursor.execute("DELETE FROM [dbo].[Application] WHERE ApplicationID=?", (current_ApplicationID,))
                #del_selected_row1 = -1; del_selected_row2 = -1; del_selected_row3 = -1; del_selected_row4 = -1#resetting the value for next occurance
            conn.commit()
            self.show_data()  # Refresh the table data
            print("Deletion completed successfully.")
            del_selected_row1 = -1; del_selected_row2 = -1; del_selected_row3 = -1; del_selected_row4 = -1#resetting the value for next occurance
        
        except Exception as e:
            print(f"Exception occurred: {e}")  # Log the exception to the console
            QMessageBox.critical(self, "Database Error", str(e)) 

        finally:
            conn.close()


# Form to handle adding and updating items
class InventoryForm(QDialog):
    def __init__(self, parent=None, 
                 WindowsClusterID=0, WindowsClusterIP='***.***.***.***', WindowsClusterName='.stc.corp',
                 NodeID=0, NodeIP='***.***.***.***', NodeName='.stc.corp', NodeOSVersion='', NodeComments='None', 
                 SQLClusterID=0, SQLClusterIP='***.***.***.***', SQLClusterName='', SQLType='', SQLInstanceName='', SQLPort='1433', SQLServerVersion='Microsft SQL Server ***',  NARsRaised='', SQLComments='None', SQLServerEdition='', MSDTCIP='',
                 ApplicationID=0, AppName='', AppOwner='', AppOwnerEmail='', AppVersion='', AppDepartment='', AppComments='None', AppCriticality=''):
        super().__init__(parent)
        self.setWindowTitle('Inventory Form')
        #self.setGeometry(40, 20, 50, 60)  # Adjusted size for more fields
        self.setGeometry(50, 50, 700, 700)
        
        self.tab_widget = QTabWidget(self)#for seperae Tab 

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()

        # Form Layout
        layout = QFormLayout(scroll_widget)

        # WindowsCluster inputs
        self.windows_tab = QWidget()# Tab for Windows Cluster
        self.windows_layout = QFormLayout(self.windows_tab)# Tab for Windows Cluster
        self.winId_input = QLineEdit(self)
        self.winId_input.setText(str(WindowsClusterID))
        self.WinClustIP_input = QLineEdit(self)
        self.WinClustIP_input.setText(str(WindowsClusterIP))
        self.WinClustName_input = QLineEdit(self)
        self.WinClustName_input.setText(str(WindowsClusterName))
        self.windows_tab.setLayout(self.windows_layout)# Tab for Windows Cluster
        self.tab_widget.addTab(self.windows_tab, "Windows Cluster")# Tab for Windows Cluster

        # Node inputs
        self.node_tab = QWidget()# Tab for Node
        self.node_layout = QFormLayout(self.node_tab)# Tab for Node
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
        self.node_tab.setLayout(self.node_layout)# Tab for Node
        self.tab_widget.addTab(self.node_tab, "Node")# Tab for Node

        # SQL Cluster inputs-11
        self.sql_tab = QWidget()# Tab for SQL Cluster
        self.sql_layout = QFormLayout(self.sql_tab)# Tab for SQL Cluster
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
        self.sql_tab.setLayout(self.sql_layout)# Tab for SQL Cluster
        self.tab_widget.addTab(self.sql_tab, "SQL Cluster")# Tab for SQL Cluster

        # Application inputs
        self.application_tab = QWidget() # Tab for Application
        self.application_layout = QFormLayout(self.application_tab) # Tab for Application
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
        self.application_tab.setLayout(self.application_layout)# Tab for Application
        self.tab_widget.addTab(self.application_tab, "Application")# Tab for Application

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

        self.setLayout(layout)

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
