import sys
import pyodbc  # SQL Server connection using pyodbc
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QVBoxLayout, QFormLayout, QLabel, QComboBox, QMessageBox

# Database connection using pyodbc for SQL Server
def get_sql_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=Inv;'
        'UID=django;'
        'PWD=Charan@1999'
    )
    return conn

# Function to fetch records from the Node table
def get_nodes():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Node")
    nodes = cursor.fetchall()
    conn.close()
    return nodes

# Function to fetch records from the SQLCluster table
def get_sql_clusters():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SQLClusterID, SQLClusterName FROM SQLCluster")
    sql_clusters = cursor.fetchall()
    conn.close()
    return sql_clusters

# Function to fetch records from the Application table
def get_applications():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ApplicationID, AppName FROM Application")
    applications = cursor.fetchall()
    conn.close()
    return applications

# Insert into NodeSQLCluster
def insert_node_sql_cluster(node_id, sql_cluster_id):
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO NodeSQLCluster (NodeID, SQLClusterID) VALUES (?, ?)", (node_id, sql_cluster_id))
        conn.commit()
        conn.close()
        QMessageBox.information(None, "Success", "Record inserted into NodeSQLCluster table!")
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))

# Insert into SQLClusterApplication
def insert_sql_cluster_application(sql_cluster_id, application_id):
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO SQLClusterApplication (SQLClusterID, ApplicationID) VALUES (?, ?)", (sql_cluster_id, application_id))
        conn.commit()
        conn.close()
        QMessageBox.information(None, "Success", "Record inserted into SQLClusterApplication table!")
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))

# Main window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mapping')
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
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Button 1: Node -> SQLCluster (Insert into NodeSQLCluster)
        self.button1 = QPushButton('Add Node to SQL Cluster')
        self.button1.clicked.connect(self.open_form_1)
        layout.addWidget(self.button1)

        # Button 2: SQLCluster -> Application (Insert into SQLClusterApplication)
        self.button2 = QPushButton('Add SQL Cluster to Application')
        self.button2.clicked.connect(self.open_form_2)
        layout.addWidget(self.button2)

        self.setLayout(layout)
        self.setWindowTitle("Main Window")
        self.show()

    # Open form for Button 1 (Node -> SQL Cluster)
    def open_form_1(self):
        self.form_window = FormWindow1()
        self.form_window.show()

    # Open form for Button 2 (SQL Cluster -> Application)
    def open_form_2(self):
        self.form_window = FormWindow2()
        self.form_window.show()

# Form window for Button 1: Add Node to SQL Cluster
class FormWindow1(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Node to SQL Cluster")

        form_layout = QFormLayout()

        # Node dropdown
        self.node_dropdown = QComboBox()
        nodes = get_nodes()
        for node in nodes:
            self.node_dropdown.addItem(f"{node[1]} (ID: {node[0]})", node[0])  # Display name with hidden NodeID

        # SQL Cluster dropdown
        self.sql_cluster_dropdown = QComboBox()
        sql_clusters = get_sql_clusters()
        for cluster in sql_clusters:
            self.sql_cluster_dropdown.addItem(f"{cluster[1]} (ID: {cluster[0]})", cluster[0])

        form_layout.addRow(QLabel("Select Node:"), self.node_dropdown)
        form_layout.addRow(QLabel("Select SQL Cluster:"), self.sql_cluster_dropdown)

        # Submit button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_form)
        form_layout.addWidget(self.submit_button)

        self.setLayout(form_layout)

    def submit_form(self):
        node_id = self.node_dropdown.currentData()
        sql_cluster_id = self.sql_cluster_dropdown.currentData()
        insert_node_sql_cluster(node_id, sql_cluster_id)

# Form window for Button 2: Add SQL Cluster to Application
class FormWindow2(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add SQL Cluster to Application")

        form_layout = QFormLayout()

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
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_form)
        form_layout.addWidget(self.submit_button)

        self.setLayout(form_layout)

    def submit_form(self):
        sql_cluster_id = self.sql_cluster_dropdown.currentData()
        application_id = self.application_dropdown.currentData()
        insert_sql_cluster_application(sql_cluster_id, application_id)

# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
