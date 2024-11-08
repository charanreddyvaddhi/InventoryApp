from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from database import get_sql_connection

def search_inventory(self, search_term):
    if not search_term:
        self.view_inventory()
        return
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        query = "EXEC [dbo].[Search_All_Clusters] ? "
        cursor.execute(query, (search_term,))
        rows = cursor.fetchall()
        conn.close()
        self.Inv_tab.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j in range(len(row)):
                self.Inv_tab.setItem(i, j, QTableWidgetItem(str(row[j])))
    except Exception as e:
        QMessageBox.warning(self, "Search Error", f"Failed to execute search: {e}")

def search_windows_cluster(self, search_term):
    if not search_term:
        self.view_windows_cluster()
        return
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        query = "EXEC [dbo].[Search_WinClusters] ? "
        cursor.execute(query, (search_term,))
        rows = cursor.fetchall()
        conn.close()
        self.WinCTable.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j in range(len(row)):
                self.WinCTable.setItem(i, j, QTableWidgetItem(str(row[j])))
    except Exception as e:
        QMessageBox.warning(self, "Search Error", f"Failed to execute search: {e}")

def search_node(self, search_term):
    if not search_term:
        self.view_node()
        return
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        query = "EXEC [dbo].[Search_Nodes] ? "
        cursor.execute(query, (search_term,))
        rows = cursor.fetchall()
        conn.close()
        self.NodeTable.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j in range(len(row)):
                self.NodeTable.setItem(i, j, QTableWidgetItem(str(row[j])))
    except Exception as e:
        QMessageBox.warning(self, "Search Error", f"Failed to execute search: {e}")

def search_sql_cluster(self, search_term):
    if not search_term:
        self.view_sql_cluster()
        return
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        query = "EXEC [dbo].[Search_SQLC] ? "
        cursor.execute(query, (search_term,))
        rows = cursor.fetchall()
        conn.close()
        self.SQLCTable.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j in range(len(row)):
                self.SQLCTable.setItem(i, j, QTableWidgetItem(str(row[j])))
    except Exception as e:
        QMessageBox.warning(self, "Search Error", f"Failed to execute search: {e}")

def search_application(self, search_term):
    if not search_term:
        self.view_application()
        return
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        query = "EXEC [dbo].[Search_App] ? "
        cursor.execute(query, (search_term,))
        rows = cursor.fetchall()
        conn.close()
        self.AppTable.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j in range(len(row)):
                self.AppTable.setItem(i, j, QTableWidgetItem(str(row[j])))
    except Exception as e:
        QMessageBox.warning(self, "Search Error", f"Failed to execute search: {e}")
