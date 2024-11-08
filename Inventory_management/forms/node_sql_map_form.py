import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QDialog
from database import get_nodes, get_sql_clusters, insert_node_sql_cluster, delete_node_sql_cluster
from forms.style_of_form import StyleOfForm

class Node_SQL_Map_Window(StyleOfForm):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Map Node to SQL Cluster")
        self.setGeometry(50, 50, 400, 200)

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
