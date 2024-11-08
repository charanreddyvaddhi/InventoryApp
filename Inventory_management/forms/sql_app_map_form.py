import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QDialog
from database import get_sql_clusters, get_applications, insert_sql_cluster_application, delete_sql_cluster_application
from forms.style_of_form import StyleOfForm

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
