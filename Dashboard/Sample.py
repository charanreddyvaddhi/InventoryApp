import sys
import pyodbc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDialog, QTableWidget, QTableWidgetItem, QLabel

# Database connection function
def get_sql_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=Dashboard;'
        'UID=django;'
        'PWD=Charan@1999'
    )
    return conn

# Fetch data for nodes and SQL clusters
def fetch_data():
    conn = get_sql_connection()
    cursor = conn.cursor()
    
    # Query for node statuses
    cursor.execute("SELECT Node_Status, COUNT(*) FROM Nodes GROUP BY Node_Status")
    node_status_data = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Query for SQL cluster statuses
    cursor.execute("SELECT SQLCluster_Status, COUNT(*) FROM SQLCluster GROUP BY SQLCluster_Status")
    sqlcluster_status_data = {row[0]: row[1] for row in cursor.fetchall()}
    
    conn.close()
    return node_status_data, sqlcluster_status_data

# Fetch list of servers by status
def fetch_servers_by_status(table, status_column, status_value):
    conn = get_sql_connection()
    cursor = conn.cursor()
    
    # Query for servers by status
    cursor.execute(f"SELECT * FROM {table} WHERE {status_column} = ?", status_value)
    servers = cursor.fetchall()
    
    conn.close()
    return servers

# Dialog to show list of servers
class ServerListDialog(QDialog):
    def __init__(self, servers, title):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Display server information in a table
        self.table = QTableWidget(len(servers), len(servers[0]) if servers else 0)
        if servers:
            self.table.setHorizontalHeaderLabels([desc[0] for desc in servers[0].cursor_description])
            for i, row in enumerate(servers):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))
        
        layout.addWidget(QLabel(title))
        layout.addWidget(self.table)

# PyQt5 Application
class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server and SQL Cluster Dashboard")
        self.setGeometry(100, 100, 800, 600)
        
        # Main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        
        # Fetch data
        node_status_data, sqlcluster_status_data = fetch_data()
        
        # Create and add pie charts
        self.add_pie_chart("Node Status", node_status_data, "Nodes", "Node_Status")
        self.add_pie_chart("SQL Cluster Status", sqlcluster_status_data, "SQLCluster", "SQLCluster_Status")
    
    def add_pie_chart(self, title, data, table, status_column):
        labels = list(data.keys())
        sizes = list(data.values())
        colors = ['#66b3ff', '#ff6666']
        
        # Create a matplotlib figure
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors
        )
        ax.set_title(title)
        
        # Embed the matplotlib figure in PyQt5
        canvas = FigureCanvas(fig)
        canvas.mpl_connect("button_press_event", lambda event: self.on_pie_segment_click(event, wedges, labels, table, status_column))
        self.layout.addWidget(canvas)
    
    def on_pie_segment_click(self, event, wedges, labels, table, status_column):
        # Check which wedge (pie segment) was clicked
        for i, wedge in enumerate(wedges):
            if wedge.contains_point((event.x, event.y)):
                status_value = labels[i]
                
                # Fetch servers based on clicked segment's status
                servers = fetch_servers_by_status(table, status_column, status_value)
                
                # Show the server list in a new dialog
                dialog = ServerListDialog(servers, f"{status_value} Servers in {table}")
                dialog.exec_()
                break

# Run the application
app = QApplication(sys.argv)
window = DashboardApp()
window.show()
sys.exit(app.exec_())
