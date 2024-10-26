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
        
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        
      
        # Creating Tabs for each Tables 
        self.windows_tab = self.create_windows_tab()

        # Add tabs to the main widget
        self.tab_widget.addTab(self.windows_tab, "Windows Cluster")

    def open_windows_cluster_form(self):
        form = WindowsClusterForm(self)
        form.exec_()
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Meathod To Export Data into Excel Files 
    def export_data(self):
        try:
            connection = get_sql_connection() # Connect To SQL Server Database Declared
            query = "SELECT * FROM [Inv].[dbo].[WindowsCluster]" #Will Fetch All The Data As Mentioned In SP 
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

        view_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        exportButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton)) 

        return button_layout,view_button,add_button,update_button,delete_button, exportButton
   
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def create_windows_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        Head_layout = QVBoxLayout()  # Heading Layout
        Heading = QLabel("Windows Clusters")
        self.Headings(Head_layout, Heading)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
    
        button_layout, view_button, add_button, update_button, delete_button, exportButton = self.Buttons()

        view_button.clicked.connect(self.view_windows_cluster)
        add_button.clicked.connect(self.add_windows_cluster)
        update_button.clicked.connect(self.update_windows_cluster)
        delete_button.clicked.connect(self.delete_windows_cluster)
        exportButton.clicked.connect(self.export_data)

        button_size = QSize(80, 30)  # Set custom button size
        for button in [add_button, delete_button, update_button, view_button, exportButton]:
            button.setFixedSize(button_size)  # Applying size to each button 

        # Create a smaller search input
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Search")
        self.searchInput.setFixedWidth(120)  # Set a fixed width for the search input
    
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_windows_cluster)

        button_layout.addStretch()

        # Create a layout for the search input and button
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.searchInput)  # Add the search input
        search_layout.addWidget(search_button)  # Add the search button
        #search_layout.addStretch()  # This will push the search layout to the right

        # Add buttons to the main button layout
        button_layout.addWidget(view_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(exportButton)
        button_layout.addLayout(search_layout)  # Add the search layout

        # Create table layout
        table_layout = QVBoxLayout()
        self.WinCTable = QTableWidget(self)  # Windows Cluster Table 
        self.WinCTable.setColumnCount(3)
        self.WinCTable.setHorizontalHeaderLabels(["WinClusterID", "WinClusterIP", "WinClusterName"])
        table_layout.addWidget(self.WinCTable)

        # Assemble the main layout
        main_layout.addLayout(Head_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(table_layout)

        tab.setLayout(main_layout)
        self.view_windows_cluster()  # Load data automatically when clicked on tab
        return tab
 

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def search_windows_cluster(self):
        search_term = self.searchInput.text()
        if not search_term: #if search is null or empty gives all Data
            self.view_windows_cluster()  # Display all data if search term is empty
            return
        try:
            conn = get_sql_connection()
            cursor = conn.cursor()
            query = "exec [dbo].[Search_WinClusters] ? "
            cursor.execute(query, (search_term,))
            rows = cursor.fetchall()
            conn.close()

            self.WinCTable.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    self.WinCTable.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.warning(self, "Search Error", f"Failed to execute search: {e}")


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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
