from PyQt5.QtCore import (Qt,QSize)
from PyQt5.QtWidgets import (QWidget,QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTableWidget, QHeaderView,QPushButton, QStyle ) 
from search_methods import (search_inventory, search_windows_cluster, search_node, search_sql_cluster, search_application)
from data_operations import (view_inventory, add_inventory, view_windows_cluster, add_windows_cluster, update_windows_cluster, delete_windows_cluster, view_node, add_node, update_node, delete_node, view_sql_cluster, add_sql_cluster, update_sql_cluster, delete_sql_cluster, view_application, add_application, update_application, delete_application)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def Headings(self, Head_layout, Heading):
    Heading.setAlignment(Qt.AlignCenter)
    Heading.setStyleSheet("font-size:30px; font-weight:bold; text-decoration:underline; font-family:Century Gothic")
    Head_layout.addWidget(Heading)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
def Buttons(self):
    button_layout = QHBoxLayout()#Button Layout
    view_button = QPushButton()
    add_button = QPushButton('Add')
    update_button = QPushButton("Update")
    delete_button = QPushButton()
    exportButton = QPushButton()
    search_button = QPushButton("Search")  
     
    view_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
    delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
    exportButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton)) 

    return button_layout,view_button,add_button,update_button,delete_button, exportButton, search_button

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def create_inventory_tab(self):
    tab = QWidget()
    main_layout = QVBoxLayout()

    Head_layout = QVBoxLayout()
    Heading = QLabel("MS-SQL Inventory")
    Headings(self, Head_layout, Heading)

    self.searchInput_INV = QLineEdit()
    self.searchInput_INV.setPlaceholderText("Enter To search")

    button_layout, view_button, add_button, update_button, delete_button, exportButton, search_button = Buttons(self)
    
    view_button.clicked.connect(self.view_inventory)
    add_button.clicked.connect(self.add_inventory)
    exportButton.clicked.connect(self.export_data)
    search_button.clicked.connect(lambda: search_inventory(self, self.searchInput_INV.text()))

    button_layout.addWidget(view_button)
    button_layout.addWidget(add_button)
    button_layout.addWidget(exportButton)
    button_layout.addStretch(3)
    button_layout.addWidget(self.searchInput_INV)
    button_layout.addWidget(search_button)

    button_size = QSize(80, 30)  # Set custom button size
    for button in [add_button, view_button, exportButton, search_button]:
        button.setFixedSize(button_size)  # Applying size to each button
    button_layout.addStretch()

    table_layout = QVBoxLayout()
    self.Inv_tab = QTableWidget(self)
    self.Inv_tab.setColumnCount(28)
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
    self.view_inventory()  # Automatically load data when clicked on tab
    return tab

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def create_windows_tab(self):
    tab = QWidget()
    main_layout = QVBoxLayout()

    Head_layout = QVBoxLayout()
    Heading = QLabel("Windows Clusters")
    Headings(self, Head_layout, Heading)

    self.searchInput_Winc = QLineEdit()
    self.searchInput_Winc.setPlaceholderText("Enter To search")

    button_layout, view_button, add_button, update_button, delete_button, exportButton, search_button = Buttons(self)
    view_button.clicked.connect(self.view_windows_cluster)
    add_button.clicked.connect(self.add_windows_cluster)
    update_button.clicked.connect(self.update_windows_cluster)
    delete_button.clicked.connect(self.delete_windows_cluster)
    search_button.clicked.connect(lambda: search_windows_cluster(self, self.searchInput_Winc.text()))

    button_layout.addWidget(view_button)
    button_layout.addWidget(add_button)
    button_layout.addWidget(update_button)
    button_layout.addWidget(delete_button)
    button_layout.addStretch(3)
    button_layout.addWidget(self.searchInput_Winc)
    button_layout.addWidget(search_button)

    button_size = QSize(80, 30)  # Set custom button size
    for button in [add_button, delete_button, update_button, view_button , search_button]:
        button.setFixedSize(button_size)  # Applying size to each button 

    table_layout = QVBoxLayout()
    self.WinCTable = QTableWidget(self)  # Windows Cluster Table 
    self.WinCTable.setColumnCount(3)
    self.WinCTable.setHorizontalHeaderLabels(["WinClusterID","WinClusterIP","WinClusterName"])
    table_layout.addWidget(self.WinCTable)

    main_layout.addLayout(Head_layout)
    main_layout.addLayout(button_layout)
    main_layout.addLayout(table_layout)

    tab.setLayout(main_layout)
    self.view_windows_cluster()  # Automatically load data when clicked on tab
    return tab

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def create_node_tab(self):
    tab = QWidget()
    main_layout = QVBoxLayout()

    Head_layout = QVBoxLayout()
    Heading = QLabel("VM/Nodes")
    Headings(self, Head_layout, Heading)

    self.searchInput_Node = QLineEdit()
    self.searchInput_Node.setPlaceholderText("Enter To search")

    button_layout, view_button, add_button, update_button, delete_button, exportButton, search_button = Buttons(self)
    add_button.clicked.connect(self.add_node)
    delete_button.clicked.connect(self.delete_node)
    update_button.clicked.connect(self.update_node)
    view_button.clicked.connect(self.view_node)
    search_button.clicked.connect(lambda: search_node(self, self.searchInput_Node.text()))

    button_layout.addWidget(view_button)
    button_layout.addWidget(add_button)
    button_layout.addWidget(update_button)
    button_layout.addWidget(delete_button)
    button_layout.addStretch(3)
    button_layout.addWidget(self.searchInput_Node)
    button_layout.addWidget(search_button)

    button_size =QSize(80, 30)  # Set custom button size
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
    Headings(self,Head_layout, Heading)

    self.searchInput_SQLC = QLineEdit()
    self.searchInput_SQLC.setPlaceholderText("Enter To search")

    button_layout, view_button, add_button, update_button, delete_button, exportButton, search_button = Buttons(self)

    add_button.clicked.connect(self.add_sql_cluster)   
    delete_button.clicked.connect(self.delete_sql_cluster)
    update_button.clicked.connect(self.update_sql_cluster)
    view_button.clicked.connect(self.view_sql_cluster)
    #search_button.clicked.connect(self.search_sql_cluster)
    search_button.clicked.connect(lambda: search_sql_cluster(self, self.searchInput_SQLC.text()))

    button_layout.addWidget(view_button)
    button_layout.addWidget(add_button)
    button_layout.addWidget(update_button)
    button_layout.addWidget(delete_button)
    button_layout.addStretch(3)
    button_layout.addWidget(self.searchInput_SQLC)
    button_layout.addWidget(search_button)

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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def create_application_tab(self):
    tab = QWidget()
    main_layout = QVBoxLayout()

    Head_layout = QVBoxLayout()#Heading Layout
    Heading = QLabel("Applications")
    Headings(self,Head_layout, Heading)

    self.searchInput_App = QLineEdit()
    self.searchInput_App.setPlaceholderText("Enter To search")

    button_layout, view_button, add_button, update_button, delete_button, exportButton, search_button = Buttons(self)

    add_button.clicked.connect(self.add_application)   
    delete_button.clicked.connect(self.delete_application)
    update_button.clicked.connect(self.update_application)
    view_button.clicked.connect(self.view_application)
    #search_button.clicked.connect(self.search_application)
    search_button.clicked.connect(lambda: search_application(self, self.searchInput_App.text()))

    button_layout.addWidget(view_button)
    button_layout.addWidget(add_button)
    button_layout.addWidget(update_button)
    button_layout.addWidget(delete_button)
    button_layout.addStretch(3)
    button_layout.addWidget(self.searchInput_App)
    button_layout.addWidget(search_button)

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
