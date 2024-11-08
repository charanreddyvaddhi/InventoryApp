from PyQt5.QtWidgets import QMainWindow, QAction, QTabWidget, QTableWidget, QFileDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHeaderView, QMessageBox, QStyle
from PyQt5.QtCore import QSize
import pandas as pd
from database import get_sql_connection
from forms.windows_cluster_form import WindowsClusterForm
from forms.node_form import NodeForm
from forms.sql_cluster_form import SQLClusterForm
from forms.application_form import ApplicationForm
from forms.node_sql_map_form import Node_SQL_Map_Window
from forms.sql_app_map_form import SQL_App_Map_Window
from styles import STYLESHEET
from data_operations import (add_inventory, view_inventory, add_windows_cluster, delete_windows_cluster, update_windows_cluster, view_windows_cluster,
                             add_node, delete_node, update_node, view_node, add_sql_cluster, delete_sql_cluster, update_sql_cluster, view_sql_cluster,
                             add_application, delete_application, update_application, view_application)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inventory Management')
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet(STYLESHEET)

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

        map_winc_node_action = QAction('Map WinC-Node', self)
        map_winc_node_action.triggered.connect(self.open_wind_node_map_form)
        file_menu.addAction(map_winc_node_action)

        map_node_sqlc_action = QAction('Map Node-SQLC', self)
        map_node_sqlc_action.triggered.connect(self.open_node_sql_map_form)
        file_menu.addAction(map_node_sqlc_action)

        map_sqlc_app_action = QAction('Map SQLC-App', self)
        map_sqlc_app_action.triggered.connect(self.open_sql_app_map_form)
        file_menu.addAction(map_sqlc_app_action)
        
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
                
        # Creating Tabs for each Table
        self.inventory_tab = self.create_inventory_tab()
        self.windows_tab = self.create_windows_tab()
        self.node_tab = self.create_node_tab()
        self.sql_tab = self.create_sql_tab()
        self.application_tab = self.create_application_tab()

        # Add tabs to the main widget
        self.tab_widget.addTab(self.inventory_tab, "All")
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

    def open_wind_node_map_form(self):
        form = Node_SQL_Map_Window()
        form.show()

    def open_node_sql_map_form(self):
        form = Node_SQL_Map_Window()
        form.show()

    def open_sql_app_map_form(self):
        form = SQL_App_Map_Window()
        form.show()

    def export_data(self):
        try:
            connection = get_sql_connection()
            query = "EXECUTE [dbo].[Select_All_Data]"
            df = pd.read_sql_query(query, connection)
            connection.close()

            options = QFileDialog.Options()
            filePath, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx)", options=options)

            if filePath:
                df.to_excel(filePath, index=False)
                QMessageBox.information(self, "Success", "Data exported successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to export data: {e}")

    # Add methods for create_inventory_tab, create_windows_tab, etc.
    # These methods should be defined similarly to the ones shown in tab_creation.py
