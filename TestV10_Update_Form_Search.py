import sys
import pyodbc #For extenral Database Connection driver import SQL server related
from PyQt5.QtCore import (Qt,QSize)
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
    QLineEdit, QFormLayout, QDialog, QLabel, QDialogButtonBox, QMessageBox, QGridLayout, QGroupBox,QComboBox, QHeaderView, 
    QScrollArea, QTabWidget,QMainWindow, QStyle, QAction,QFileDialog )
#from PyQt5.QtGui import (QIcon) 
import pandas as pd

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#Style Of Application Is Set As Below 
class StyleOfForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
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
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
STYLESHEET = ("""
                QWidget, QMainWindow {background-color:#DCDCDC; font-family:Century Gothic;}
                QLineEdit, QComboBox {padding:5px; background-color:#CCCCCC; border:2px solid #CCCCCC; border-radius:5px; }
                QLineEdit:focus, QComboBox:focus {border:2px solid #4F008C;}
                QPushButton,QDialogButtonBox {
                    background-color: #4F008C;
                    font-weight: bold; font-size: 15px;
                    color:white; border:none; border-radius:15px; padding:5px; 
                }
                QPushButton:hover {background-color:#0056B3;}
                QLabel {font-size:14px; color:#333333; }
                QTabWidget::pane { border: 5px solid #CCCCCC; }
                QTabBar::tab {background: #E6E6E6; border: 1px solid #000000; padding: 8px 16px; border-radius: 10px; margin-right: 5px;}
                QTabBar::tab:selected {background:#FFFFFF; border-bottom-color: #FFFFFF; }
                QTabBar::tab:hover {background:#DCDCDC; }        
            """)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#Database Connection declaration 
def get_sql_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=Inv;'
        'UID=django;'
        'PWD=Charan@1999'
    )
    return conn

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#Function To Fetch Records From Node Table For Mapping 
def get_nodes():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT NODEID, NODENAME FROM [INV].[DBO].[NODE]")
    nodes = cursor.fetchall()
    conn.close()
    return nodes

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Function To Fetch Records From SQLCluster table For Mapping
def get_sql_clusters():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SQLCLUSTERID, SQLCLUSTERNAME FROM [INV].[DBO].[SQLCLUSTER]")
    sql_clusters = cursor.fetchall()
    conn.close()
    return sql_clusters

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Function To Fetch Records From Application Table For Mapping
def get_applications():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT APPLICATIONID, APPNAME FROM [INV].[DBO].[APPLICATION]")
    applications = cursor.fetchall()
    conn.close()
    return applications

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Insert into NodeSQLCluster For Mapping
def insert_node_sql_cluster(node_id, sql_cluster_id):
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO NodeSQLCluster (NodeID, SQLClusterID) VALUES (?, ?)", (node_id, sql_cluster_id))
        conn.commit()
        conn.close()
        QMessageBox.information(None, "éxito", "Mapping Between Node And SQLCluster Is Sucessfull !!!")
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Insert into SQLClusterApplication For Mapping
def insert_sql_cluster_application(sql_cluster_id, application_id):
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO SQLClusterApplication (SQLClusterID, ApplicationID) VALUES (?, ?)", (sql_cluster_id, application_id))
        conn.commit()
        conn.close()
        QMessageBox.information(None, "éxito", "Mapping Between SQLCluster And Application  Is Sucessfull !!!")
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Delete from NodeSQLCluster (For Unmappig)
def delete_node_sql_cluster(node_id, sql_cluster_id):
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM NodeSQLCluster WHERE NodeID = ? AND SQLClusterID = ?", (node_id, sql_cluster_id))
        conn.commit()
        conn.close()
        QMessageBox.information(None, "Success", "Record unmapped from NodeSQLCluster table!")
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Delete from SQLClusterApplication (For Unmappig)
def delete_sql_cluster_application(sql_cluster_id, application_id):
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SQLClusterApplication WHERE SQLClusterID = ? AND ApplicationID = ?", (sql_cluster_id, application_id))
        conn.commit()
        conn.close()
        QMessageBox.information(None, "Success", "Record unmapped from SQLClusterApplication table!")
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inventory Management')
        self.setGeometry(100, 100, 800, 600)

        # Menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('Action')
        
        # Add actions to the menu
        add_windows_cluster_action = QAction('Add Windows Cluster', self)
        add_windows_cluster_action.triggered.connect(self.open_windows_cluster_form)
        file_menu.addAction(add_windows_cluster_action)

        add_node_action = QAction('Add Node', self)
        add_node_action.triggered.connect(self.open_node_form)
        file_menu.addAction(add_node_action)

        add_sql_cluster_action = QAction('Add SQL Cluster', self)
        add_sql_cluster_action.triggered.connect(self.open_sql_cluster_form)
        file_menu.addAction(add_sql_cluster_action)

        add_application_action = QAction('Add Application', self)
        add_application_action.triggered.connect(self.open_application_form)
        file_menu.addAction(add_application_action)

        Map_Winc_Node_Action = QAction('Map WinC-Node', self)
        Map_Winc_Node_Action.triggered.connect(self.open_Wind_Node_Map_Form)
        file_menu.addAction(Map_Winc_Node_Action)

        Map_Node_SQLC_action = QAction('Map Node-SQLC', self)
        Map_Node_SQLC_action.triggered.connect(self.open_Node_SQL_Map_Form)
        file_menu.addAction(Map_Node_SQLC_action)

        Map_SQLC_App_action = QAction('Map SQLC-App', self)
        Map_SQLC_App_action.triggered.connect(self.open_SQL_App_Map_Form)
        file_menu.addAction(Map_SQLC_App_action)
        
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        
        # Add an export button (Highlighted)
        #self.exportButton = QPushButton("Export",self)
        #self.exportButton.setGeometry(50, 500, 200, 40)  # **Button setup**
        #self.exportButton.clicked.connect(self.export_data)  # **Button event connection**
        
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

    def open_windows_cluster_form(self):
        form = WindowsClusterForm(self)
        form.exec_()

    def open_node_form(self):
        form = NodeForm(self)
        form.exec_()

    def open_sql_cluster_form(self):
        form = SQLClusterForm(self)
        form.exec_()

    def open_application_form(self):
        form = ApplicationForm(self)
        form.exec_()
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Method To Export Data into Excel Files 
    def export_data(self):
        try:
            connection = get_sql_connection() # Connect To SQL Server Database Declared
            query = "EXECUTE [dbo].[Select_All_Data]" #Will Fetch All The Data As Mentioned In SP 
            df = pd.read_sql_query(query, connection)
            connection.close() #Will Close The Connection To Database 

            # Prompt user to select a save location
            options = QFileDialog.Options()
            filePath, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx)", options=options)

            if filePath:
                # Export DataFrame to Excel
                df.to_excel(filePath, index=False)
                QMessageBox.information(self, "Success", "Data exported successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to export data: {e}")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Search Method  
    def Search_Inventory(self):
        search_term_Inv = self.searchInput_INV.text()
        print(search_term_Inv)
        if not search_term_Inv: #if search is null or empty gives all Data
            self.view_Inventory()  # Display all data if search term is empty
            return
        try:
            conn = get_sql_connection()
            cursor = conn.cursor()
            query = "exec [dbo].[Search_All_Clusters] ? "
            cursor.execute(query, (search_term_Inv,))
            rows1 = cursor.fetchall()
            conn.close()
            #rows1 = cursor.fetchall()    
            self.Inv_tab.setRowCount(len(rows1))
            for i, row in enumerate(rows1):
                for j in range(len(row)):
                  self.Inv_tab.setItem(i, j, QTableWidgetItem(str(row[j])))

        except Exception as e:
            QMessageBox.warning(self, "Search Error", f"Failed to execute search: {e}")

    def Search_WinC(self):
        search_term_winc = self.searchInput_Winc.text()
        print(search_term_winc)
        if not search_term_winc: #if search is null or empty gives all Data
            self.view_windows_cluster()  # Display all data if search term is empty
            return
        try:
            conn = get_sql_connection()
            cursor = conn.cursor()
            query = "exec [dbo].[Search_WinClusters] ? "
            cursor.execute(query, (search_term_winc,))
            rows1 = cursor.fetchall()
            conn.close()
            #rows1 = cursor.fetchall()    
            self.WinCTable.setRowCount(len(rows1))
            for i, row in enumerate(rows1):
                for j in range(len(row)):
                  self.WinCTable.setItem(i, j, QTableWidgetItem(str(row[j])))

        except Exception as e:
            QMessageBox.warning(self, "Search Error", f"Failed to execute search: {e}")        

    def Search_Node(self):
        search_term_Node = self.searchInput_Node.text()
        print(search_term_Node)
        if not search_term_Node: #if search is null or empty gives all Data
            self.view_node()  # Display all data if search term is empty
            return
        try:
            conn = get_sql_connection()
            cursor = conn.cursor()
            query = "exec [dbo].[Search_Nodes] ? "
            cursor.execute(query, (search_term_Node,))
            rows1 = cursor.fetchall()
            conn.close()
            #rows1 = cursor.fetchall()    
            self.NodeTable.setRowCount(len(rows1))
            for i, row in enumerate(rows1):
                for j in range(len(row)):
                  self.NodeTable.setItem(i, j, QTableWidgetItem(str(row[j])))

        except Exception as e:
            QMessageBox.warning(self, "Search Error", f"Failed to execute search: {e}")

    def Search_SQLC(self):
        search_term_SQLC = self.searchInput_SQLC.text()
        print(search_term_SQLC) 
        if not search_term_SQLC: #if search is null or empty gives all Data
            self.view_sql_cluster()  # Display all data if search term is empty
            return
        try:
            conn = get_sql_connection()
            cursor = conn.cursor()
            query = "exec [dbo].[Search_SQLC] ? "
            cursor.execute(query, (search_term_SQLC,))
            rows1 = cursor.fetchall()
            conn.close()
            #rows1 = cursor.fetchall()    
            self.SQLCTable.setRowCount(len(rows1))
            for i, row in enumerate(rows1):
                for j in range(len(row)):
                  self.SQLCTable.setItem(i, j, QTableWidgetItem(str(row[j])))

        except Exception as e:
            QMessageBox.warning(self, "Search Error", f"Failed to execute search: {e}")
    
    def Search_App(self):
        search_term_App = self.searchInput_App.text()
        print(search_term_App)
        if not search_term_App: #if search is null or empty gives all Data
            self.view_application()  # Display all data if search term is empty
            return
        try:
            conn = get_sql_connection()
            cursor = conn.cursor()
            query = "exec [dbo].[Search_App] ? "
            cursor.execute(query, (search_term_App,))
            rows1 = cursor.fetchall()
            conn.close()
            #rows1 = cursor.fetchall()    
            self.AppTable.setRowCount(len(rows1))
            for i, row in enumerate(rows1):
                for j in range(len(row)):
                  self.AppTable.setItem(i, j, QTableWidgetItem(str(row[j])))

        except Exception as e:
            QMessageBox.warning(self, "Search Error", f"Failed to execute search: {e}")
        

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Mapping Meathods  
    def open_Node_SQL_Map_Form(self):
        self.form_window = Node_SQL_Map_Window()
        self.form_window.show()    

    def open_SQL_App_Map_Form(self):
        self.form_window = SQL_App_Map_Window()
        self.form_window.show()    
        #print(" open_SQL_App_Map_Form to be implemaneted")

    def open_Wind_Node_Map_Form(self):
        #self.form_window = SQL_App_Map_Window()
        #self.form_window.show()    
        print(" Shall be implmented in later stages adjust with Update button in Node tab")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def Headings(self, Head_layout, Heading):
        Heading.setAlignment(Qt.AlignCenter)
        Heading.setStyleSheet("font-size:30px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
        Head_layout.addWidget(Heading)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def Buttons(self):
        button_layout = QHBoxLayout()#Button Layout
        view_button = QPushButton()
        add_button = QPushButton('Add')
        update_button = QPushButton("Update")
        delete_button = QPushButton()
        exportButton = QPushButton()
        search_button = QPushButton("Search")  
        #Map_button = QPushButton("Map")
        #Wind_Node_Map = QPushButton("Map Win-Node")
        #Node_SQL_Map = QPushButton("Map Node-SQL")
        #SQL_App_Map = QPushButton("Map SQL-App")

        view_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        exportButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton)) 

        return button_layout,view_button,add_button,update_button,delete_button, exportButton, search_button
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def create_inventory_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()#Heading Layout
        Heading = QLabel("MS-SQL Inventory")
        self.Headings(Head_layout, Heading)

        self.searchInput_INV = QLineEdit()
        self.searchInput_INV.setPlaceholderText("Enter To search")
        

        button_layout, view_button, add_button, update_button, delete_button, exportButton, search_button = self.Buttons()
              
        view_button.clicked.connect(self.view_Inventory)
        add_button.clicked.connect(self.add_Inventory)  
        exportButton.clicked.connect(self.export_data)
        search_button.clicked.connect(self.Search_Inventory)
        #Wind_Node_Map.clicked.connect(self.open_Wind_Node_Map_Form)
        #Node_SQL_Map.clicked.connect(self.open_Node_SQL_Map_Form) 
        #SQL_App_Map.clicked.connect(self.open_SQL_App_Map_Form) 
        
        button_layout.addWidget(view_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(exportButton)
        button_layout.addStretch(3)
        button_layout.addWidget(self.searchInput_INV)
        button_layout.addWidget(search_button)
        #button_layout.addWidget(Wind_Node_Map)
        #button_layout.addWidget(Node_SQL_Map)
        #button_layout.addWidget(SQL_App_Map)
        
        button_size = QSize(80, 30)  # Set custom button size
        for button in [add_button, view_button, exportButton, search_button]:
            button.setFixedSize(button_size)  # Applying size to each botton 
        button_layout.addStretch() 
        
        table_layout = QVBoxLayout()

        self.Inv_tab = QTableWidget(self)#Windows Cluster Table 
        self.Inv_tab.setColumnCount(28)
        #self.Inv_tab.setHorizontalHeaderLabels(["WinClusterID","WinClusterIP","WinClusterName",
         #                                      "NodeID","Node-IP","Node-Name","Node-OSVersion","NodeComments","WindowsClusterID",
          #                                     "SQLClusterID","SQLClusterIP","SQLClusterName","SQLType","SQLInstanceName","SQLPort","SQLServerVersion","NARs-Raised","SQLComments","SQLServerEdition","MSDTCIP",
           #                                    "ApplicationID","AppName","AppOwner","AppOwnerEmail","AppVersion","AppDepartment","AppComments","AppCriticality"])
        self.Inv_tab.setHorizontalHeaderLabels(["WinCluster_IP","WinCluster_Name","Device_IP","Hostname","DB_IP", "SQLCluster_Name","SQLInstance_Name","DB_Port",
                                                "SQL_Type","Application_Name","AppOwner","AppOwnerEmail","AppVersion","AppDepartment","AppCriticality","OS_Version",
                                                 "SQL_Version","SQL_Edition","MSDTCIP","NARsRaised","NodeComments","SQLComments","AppComments","WinClusterID","NodeID",
                                                  "WinClusterID_Node","SQLClusterID","ApplicationID" ])
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
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def create_windows_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()#Heading Layout
        Heading = QLabel("Windows Clusters")
        self.Headings(Head_layout, Heading)

        self.searchInput_Winc = QLineEdit()
        self.searchInput_Winc.setPlaceholderText("Enter To search")

        button_layout, view_button, add_button, update_button, delete_button, exportButton, search_button = self.Buttons()

        view_button.clicked.connect(self.view_windows_cluster)
        add_button.clicked.connect(self.add_windows_cluster)   
        update_button.clicked.connect(self.update_windows_cluster)
        delete_button.clicked.connect(self.delete_windows_cluster)
        search_button.clicked.connect(self.Search_WinC)

        
        button_layout.addWidget(view_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addStretch(3)
        button_layout.addWidget(self.searchInput_Winc)
        button_layout.addWidget(search_button)

        
        button_size = QSize(80, 30)  # Set custom button size
        for button in [add_button, delete_button, update_button, view_button , search_button]:
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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def create_node_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()#Heading Layout
        Heading = QLabel("VM/Nodes")
        self.Headings(Head_layout, Heading)

        self.searchInput_Node = QLineEdit()
        self.searchInput_Node.setPlaceholderText("Enter To search")

        button_layout, view_button, add_button, update_button, delete_button, exportButton, search_button = self.Buttons()

        add_button.clicked.connect(self.add_node)   
        delete_button.clicked.connect(self.delete_node)
        update_button.clicked.connect(self.update_node)
        view_button.clicked.connect(self.view_node)
        search_button.clicked.connect(self.Search_Node)
        #Wind_Node_Map.clicked.connect(self.open_Wind_Node_Map_Form)

        button_layout.addWidget(view_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addStretch(3)
        button_layout.addWidget(self.searchInput_Node)
        button_layout.addWidget(search_button)
        #button_layout.addWidget(Wind_Node_Map)

        button_size = QSize(80, 30)  # Set custom button size
        for button in [add_button, delete_button, update_button, view_button,search_button]:
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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def create_sql_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()#Heading Layout
        Heading = QLabel("SQL Cluster")
        self.Headings(Head_layout, Heading)

        self.searchInput_SQLC = QLineEdit()
        self.searchInput_SQLC.setPlaceholderText("Enter To search")

        button_layout, view_button, add_button, update_button, delete_button, exportButton, search_button = self.Buttons()

        add_button.clicked.connect(self.add_sql_cluster)   
        delete_button.clicked.connect(self.delete_sql_cluster)
        update_button.clicked.connect(self.update_sql_cluster)
        view_button.clicked.connect(self.view_sql_cluster)
        search_button.clicked.connect(self.Search_SQLC)
        #Node_SQL_Map.clicked.connect(self.open_Node_SQL_Map_Form)

        button_layout.addWidget(view_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addStretch(3)
        button_layout.addWidget(self.searchInput_SQLC)
        button_layout.addWidget(search_button)
        #button_layout.addWidget(Node_SQL_Map)

        button_size = QSize(80, 30)  # Set custom button size
        for button in [add_button, delete_button, update_button, view_button, search_button]:
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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def create_application_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()#Heading Layout
        Heading = QLabel("Applications")
        self.Headings(Head_layout, Heading)

        self.searchInput_App = QLineEdit()
        self.searchInput_App.setPlaceholderText("Enter To search")

        button_layout, view_button, add_button, update_button, delete_button, exportButton, search_button = self.Buttons()

        add_button.clicked.connect(self.add_application)   
        delete_button.clicked.connect(self.delete_application)
        update_button.clicked.connect(self.update_application)
        view_button.clicked.connect(self.view_application)
        search_button.clicked.connect(self.Search_App)
        #SQL_App_Map.clicked.connect(self.open_SQL_App_Map_Form)

        button_layout.addWidget(view_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addStretch(3)
        button_layout.addWidget(self.searchInput_App)
        button_layout.addWidget(search_button)
        #button_layout.addWidget(SQL_App_Map)

        button_size = QSize(80, 30)  # Set custom button size
        for button in [add_button, delete_button, update_button, view_button, search_button]:
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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def add_Inventory(self):
        form = InventoryForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = get_sql_connection()
            cursor = conn.cursor()
            #print(f"Inserting Data: {data}")
            #cursor.execute("INSERT INTO [dbo].[WindowsCluster] (WinClusterID, WinClusterIP, WinClusterName) VALUES (?, ?, ?)", data[:3])
            #cursor.execute("INSERT INTO [dbo].[Node] (NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments) VALUES (?, ?, ?, ?, ?)", data[3:8])
            #cursor.execute("INSERT INTO [dbo].[SQLCluster] (SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data[8:19])
            #cursor.execute("INSERT INTO [dbo].[Application] ([ApplicationID],[AppName],[AppOwner],[AppOwnerEmail],[AppVersion],[AppDepartment],[AppComments],[AppCriticality]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data[19:27])
            try :   
                cursor.execute(
                    """
                    EXEC InsertOrMapData @WinClusterID = ?, @WinClusterIP = ?, @WinClusterName = ?, 
					@NodeID = ?, @NodeIP = ?, @NodeName = ?, @NodeOSVersion = ?,@NodeComments = ?, 
					@SQLClusterID = ?, @SQLClusterIP = ?, @SQLClusterName = ?, @SQLType = ?, @SQLInstanceName = ?, @SQLPort = ?, @SQLServerVersion = ?, 
					@NARsRaised = ?, @SQLComments = ?, @SQLServerEdition = ?, @MSDTCIP = ?, 
					@ApplicationID = ?, @AppName = ?, @AppOwner = ?, @AppOwnerEmail = ?, @AppVersion = ?, @AppDepartment = ?, @AppComments = ?, @AppCriticality = ?
                    """, data)
                conn.commit()
                QMessageBox.information(self, "Success", "Inventory Details added successfully.")
                self.view_Inventory()
            except Exception as e:
                #print(e)
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            finally:
                conn.close()
            #QMessageBox.information(self, "Success", "Inventory Details added successfully.")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def view_Inventory(self):
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("EXECUTE [dbo].[Select_All_Data]")
        rows1 = cursor.fetchall()        
        self.Inv_tab.setRowCount(len(rows1))
        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.Inv_tab.setItem(i, j, QTableWidgetItem(str(row[j])))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def add_windows_cluster(self):
        form = WindowsClusterForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = get_sql_connection()
            cursor = conn.cursor()
            print(f"Inserting Data: {data}")
            cursor.execute("INSERT INTO [dbo].[WindowsCluster] (WinClusterID, WinClusterIP, WinClusterName) VALUES (?, ?, ?)", data[:3])
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Windows Cluster added successfully.")
            self.view_windows_cluster()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def delete_windows_cluster(self):
        del_selected_row = self.WinCTable.currentRow()
        if del_selected_row < 0:
            QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
            return
        conn = get_sql_connection()
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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%           
    def update_windows_cluster(self):
        del_selected_row = self.WinCTable.currentRow() 
        if del_selected_row < 0:
            QMessageBox.warning(self, "Update Item", "Please select an item to update.")
            return
        form = WindowsClusterForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()  
            conn = get_sql_connection()
            cursor = conn.cursor()
            print(f"Updating Data {data}")
            cursor.execute("UPDATE [dbo].[WindowsCluster] SET WinClusterIP=?, WinClusterName=? WHERE WinClusterID=?", (data[1], data[2], data[0]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Windows Cluster updated successfully.")
            self.view_node()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def view_windows_cluster(self):
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [Inv].[dbo].[WindowsCluster]")
        rows1 = cursor.fetchall()        
        self.WinCTable.setRowCount(len(rows1))
        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.WinCTable.setItem(i, j, QTableWidgetItem(str(row[j])))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def add_node(self):
        form = NodeForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = get_sql_connection()
            cursor = conn.cursor()
            print(f"Inserting Data: {data}")
            cursor.execute("INSERT INTO [dbo].[Node] (NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments, WinClusterID) VALUES (?, ?, ?, ?, ?, ?)", data[:6])
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Node added successfully.")
            self.view_node()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def delete_node(self):
        del_selected_row = self.NodeTable.currentRow() 
        if del_selected_row < 0:
            QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
            return
        conn = get_sql_connection()
        cursor = conn.cursor()
        try:
            current_NodeID = self.NodeTable.item(del_selected_row, 0).text()
            print(f"Deleting Node with ID: {current_NodeID}")
            cursor.execute("DELETE FROM [dbo].[Node] WHERE NodeID=?", (current_NodeID,))
            conn.commit()
            QMessageBox.information(self, "Success", "Node deleted successfully.")
            self.view_node()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            conn.close()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def update_node(self):
        del_selected_row = self.NodeTable.currentRow() 
        if del_selected_row < 0:
            QMessageBox.warning(self, "Update Item", "Please select an item to update.")
            return
        form = NodeForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = get_sql_connection()
            cursor = conn.cursor()
            print(f"Updating Data {data}")
            cursor.execute("UPDATE [dbo].[Node] SET NodeIP=?, NodeName=?, NodeOSVersion=?, NodeComments=?, WinClusterID=? WHERE NodeID=?", (data[1], data[2], data[3], data[4], data[5], data[0]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Node updated successfully.")
            self.view_node()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def view_node(self):
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [Inv].[dbo].[Node]")
        rows1 = cursor.fetchall()        
        self.NodeTable.setRowCount(len(rows1))
        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.NodeTable.setItem(i, j, QTableWidgetItem(str(row[j])))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def add_sql_cluster(self):
        form = SQLClusterForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = get_sql_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO [dbo].[SQLCluster] (SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data[:11])
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "SQL Cluster added successfully.")
            self.view_sql_cluster()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def delete_sql_cluster(self):
        del_selected_row = self.SQLCTable.currentRow()
        if del_selected_row < 0:
            QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
            return
        conn = get_sql_connection()
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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def update_sql_cluster(self):
        del_selected_row = self.SQLCTable.currentRow()
        if del_selected_row < 0:
            QMessageBox.warning(self, "Update Item", "Please select an item to update.")
            return
        form = SQLClusterForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = get_sql_connection()
            cursor = conn.cursor()
            print(f"Updating Data {data}")
            cursor.execute("UPDATE [dbo].[SQLCluster] SET SQLClusterIP=?, SQLClusterName=?, SQLType=?, SQLInstanceName=?, SQLPort=?, SQLServerVersion=?, NARsRaised=?, SQLComments=?, SQLServerEdition=?, MSDTCIP=? WHERE SQLClusterID=?", (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[0]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "SQL Cluster updated successfully.")
            self.view_sql_cluster()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def view_sql_cluster(self):
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [Inv].[dbo].[SQLCluster]")
        rows1 = cursor.fetchall()        
        self.SQLCTable.setRowCount(len(rows1))
        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.SQLCTable.setItem(i, j, QTableWidgetItem(str(row[j])))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def add_application(self):
        form = ApplicationForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = get_sql_connection()
            cursor = conn.cursor()
            print(f"Inserting Data: {data}")            
            cursor.execute("INSERT INTO [dbo].[Application] ([ApplicationID],[AppName],[AppOwner],[AppOwnerEmail],[AppVersion],[AppDepartment],[AppComments],[AppCriticality]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data[:8])
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Application added successfully.")
            self.view_application()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def delete_application(self):
        del_selected_row = self.AppTable.currentRow()
        if del_selected_row < 0:
            QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
            return
        conn = get_sql_connection()
        cursor = conn.cursor()
        try:
            current_AppID = self.AppTable.item(del_selected_row, 0).text() 
            print(f"Deleting Application with ID: {current_AppID}")
            cursor.execute("DELETE FROM [dbo].[Application] WHERE ApplicationID=?", (current_AppID,))
            conn.commit()
            QMessageBox.information(self, "Success", "Application deleted successfully.")
            self.view_application()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            conn.close()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def update_application(self):
        del_selected_row = self.AppTable.currentRow()
        if del_selected_row < 0:
            QMessageBox.warning(self, "Update Item", "Please select an item to update.")
            return
        form = ApplicationForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            conn = self.get_sql_connection()
            cursor = conn.cursor()
            print(f"Updating Data {data}")            
            cursor.execute("UPDATE [dbo].[Application] SET AppName=?, AppOwner=?, AppOwnerEmail=?, AppVersion=?, AppDepartment=?, AppComments=?, AppCriticality=? WHERE ApplicationID=?", (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[0]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Application updated successfully.")
            self.view_application()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def view_application(self):
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [Inv].[dbo].[Application]")
        rows1 = cursor.fetchall()        
        self.AppTable.setRowCount(len(rows1))
        for i, row in enumerate(rows1):
            for j in range(len(row)):
                self.AppTable.setItem(i, j, QTableWidgetItem(str(row[j])))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

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

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class WindowsClusterForm(StyleOfForm):
    def __init__(self, parent=None, 
                 WindowsClusterID=0, WindowsClusterIP='***.***.***.***', WindowsClusterName=''):
        super().__init__(parent)
        self.setWindowTitle('Windows Cluster Form')
        self.setGeometry(50, 50, 400, 200)

        layout = QFormLayout()

        # WindowsCluster inputs
        self.winId_input = QLineEdit(self)
        self.winId_input.setText(str(WindowsClusterID))
        self.WinClustIP_input = QLineEdit(self)
        self.WinClustIP_input.setText(str(WindowsClusterIP))
        self.WinClustName_input = QLineEdit(self)
        self.WinClustName_input.setText(str(WindowsClusterName))

        # Add rows for WindowsCluster
        layout.addRow('WindowsClusterID', self.winId_input)
        layout.addRow('WindowsClusterIP', self.WinClustIP_input)
        layout.addRow('WindowsClusterName', self.WinClustName_input)

        # Button Box for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def get_data(self):
        # Collect and return Windows Cluster data
        WindowsClusterID = self.winId_input.text()
        WindowsClusterIP = self.WinClustIP_input.text()
        WindowsClusterName = self.WinClustName_input.text()

        return (WindowsClusterID, WindowsClusterIP, WindowsClusterName)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class NodeForm(StyleOfForm):
    def __init__(self, parent=None, 
                 NodeID=000, NodeIP='***.***.***.***', NodeName='', NodeOSVersion='', NodeComments='Main Node', WinClusterID=0):
        super().__init__(parent)
        self.setWindowTitle('Node Form')
        self.setGeometry(50, 50, 400, 300)

        layout = QFormLayout()

        # Node inputs
        self.nodeId_input = QLineEdit(self)
        self.nodeId_input.setText(str(NodeID))
        self.nodeIP_input = QLineEdit(self)
        self.nodeIP_input.setText(str(NodeIP))
        self.nodeName_input = QLineEdit(self)
        self.nodeName_input.setText(str(NodeName))
        self.nodeOS_input = QComboBox(self)
        self.nodeOS_input.addItems(["Windows Server 2012", "Windows Server 2012 R2", "Windows Server 2016", "Windows Server 2019", "Windows Server 2022"])
        self.nodeOS_input.setCurrentText(NodeOSVersion)
        self.nodeComments_input = QLineEdit(self)
        self.nodeComments_input.setText(NodeComments)
        self.windowsclusterId_input = QLineEdit(self)
        self.windowsclusterId_input.setText(str(WinClusterID))

        # Add rows for Node inputs
        layout.addRow('NodeID', self.nodeId_input)
        layout.addRow('NodeIP', self.nodeIP_input)
        layout.addRow('NodeName', self.nodeName_input)
        layout.addRow('NodeOSVersion', self.nodeOS_input)
        layout.addRow('NodeComments', self.nodeComments_input)
        layout.addRow('WinClusterID', self.windowsclusterId_input)

        # Button Box for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def get_data(self):
        # Collect and return Node data
        NodeID = self.nodeId_input.text()
        NodeIP = self.nodeIP_input.text()
        NodeName = self.nodeName_input.text()
        NodeOSVersion = self.nodeOS_input.currentText()  # From dropdown
        NodeComments = self.nodeComments_input.text()
        WinClusterID = self.windowsclusterId_input.text()
        
        return (NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments, WinClusterID)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class SQLClusterForm(StyleOfForm):
    def __init__(self, parent=None, 
                 SQLClusterID=0000, SQLClusterIP='***.***.***.***', SQLClusterName='', SQLType='', SQLInstanceName='MSSQLSERVER', SQLPort='1433', SQLServerVersion='', NARsRaised='None', SQLComments='None', SQLServerEdition='', MSDTCIP=''):
        super().__init__(parent)
        self.setWindowTitle('SQL Cluster Form')
        self.setGeometry(50, 50, 400, 400)

        layout = QFormLayout()

        # SQL Cluster inputs
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
        self.sqlServerEdition_input.addItems(["Web", "Express Edition", "Developer Edition", "Standard Edition", "Enterprise Edition"])
        self.sqlServerEdition_input.setCurrentText(SQLServerEdition)
        self.msdtcIP_input = QLineEdit(self)
        self.msdtcIP_input.setText(MSDTCIP)

        # Add rows for SQL Cluster
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

        # Button Box for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def get_data(self):
        # Collect and return SQL Cluster data
        return (self.sqlClustId_input.text(), self.sqlClustIP_input.text(), self.sqlClustName_input.text(), self.sqlType_input.text(), self.sqlInstanceName_input.text(),
                self.sqlPort_input.text(), self.sqlserverversion_input.currentText(), self.narsRaised_input.text(), self.sqlComments_input.text(), self.sqlServerEdition_input.currentText(), self.msdtcIP_input.text())

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class ApplicationForm(StyleOfForm):
    def __init__(self, parent=None, 
                 ApplicationID=00000, AppName='', AppOwner='', AppOwnerEmail='@yahoo.com', AppVersion='', AppDepartment='', AppComments='None', AppCriticality=''):
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
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def get_data(self):
        # Collect and return Application data
        return (self.appId_input.text(), self.appName_input.text(), self.appOwner_input.text(), self.appOwnerEmail_input.text(),
                self.appVersion_input.text(), self.appDepartment_input.currentText(), self.appComments_input.text(), self.appCriticality_input.text())

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class Node_SQL_Map_Window(StyleOfForm):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Map Node to SQL Cluster")
        self.setGeometry(50, 50, 100, 100)

        form_layout = QFormLayout()
        button_layout = QHBoxLayout()

        # Node dropdown
        self.node_dropdown = QComboBox()
        nodes = get_nodes()
        for node in nodes:
            self.node_dropdown.addItem(f"{node[1]} (ID: {node[0]})", node[0])  # Display details of Nodes

        # SQL Cluster dropdown
        self.sql_cluster_dropdown = QComboBox()
        sql_clusters = get_sql_clusters()
        for cluster in sql_clusters:
            self.sql_cluster_dropdown.addItem(f"{cluster[1]} (ID: {cluster[0]})", cluster[0])

        form_layout.addRow(QLabel("Select Node:"), self.node_dropdown)
        form_layout.addRow(QLabel("Select SQL Cluster:"), self.sql_cluster_dropdown)

        # Submit button
        self.submit_button = QPushButton('Map')
        self.submit_button.clicked.connect(self.submit_form)
        button_layout.addWidget(self.submit_button)

        # Unmap button
        self.unmap_button = QPushButton('Unmap')
        self.unmap_button.clicked.connect(self.unmap_form)
        button_layout.addWidget(self.unmap_button)

        form_layout.addRow(button_layout)
        self.setLayout(form_layout)

    def submit_form(self):
        node_id = self.node_dropdown.currentData()
        sql_cluster_id = self.sql_cluster_dropdown.currentData()
        insert_node_sql_cluster(node_id, sql_cluster_id)

    def unmap_form(self):
        node_id = self.node_dropdown.currentData()
        sql_cluster_id = self.sql_cluster_dropdown.currentData()
        delete_node_sql_cluster(node_id, sql_cluster_id)        

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class SQL_App_Map_Window(StyleOfForm):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add SQL Cluster to Application")
        self.setGeometry(50, 50, 100, 100)

        form_layout = QFormLayout()
        button_layout = QHBoxLayout()

        # SQL Cluster dropdown
        self.sql_cluster_dropdown = QComboBox()
        sql_clusters = get_sql_clusters()
        for cluster in sql_clusters:
            self.sql_cluster_dropdown.addItem(f"{cluster[1]} (ID: {cluster[0]})", cluster[0])

        # Application dropdown
        self.application_dropdown = QComboBox()
        applications = get_applications()
        for app in applications:
            self.application_dropdown.addItem(f"{app[1]} (ID: {app[0]})", app[0])

        form_layout.addRow(QLabel("Select SQL Cluster:"), self.sql_cluster_dropdown)
        form_layout.addRow(QLabel("Select Application:"), self.application_dropdown)

        # Submit button
        self.submit_button = QPushButton('Map')
        self.submit_button.clicked.connect(self.submit_form)
        button_layout.addWidget(self.submit_button)

        # Unmap button
        self.unmap_button = QPushButton('Unmap')
        self.unmap_button.clicked.connect(self.unmap_form)
        button_layout.addWidget(self.unmap_button)

        form_layout.addRow(button_layout)
        self.setLayout(form_layout)

    def submit_form(self):
        sql_cluster_id = self.sql_cluster_dropdown.currentData()
        application_id = self.application_dropdown.currentData()
        insert_sql_cluster_application(sql_cluster_id, application_id)

    def unmap_form(self):
        sql_cluster_id = self.sql_cluster_dropdown.currentData()
        application_id = self.application_dropdown.currentData()
        delete_sql_cluster_application(sql_cluster_id, application_id)        

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
