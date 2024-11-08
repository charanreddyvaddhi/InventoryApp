from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QDialog
from database import get_sql_connection
from forms.inventory_form import InventoryForm
from forms.windows_cluster_form import WindowsClusterForm
from forms.node_form import NodeForm
from forms.sql_cluster_form import SQLClusterForm
from forms.application_form import ApplicationForm

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Inventory Operations

def add_inventory(self):
    form = InventoryForm()
    if form.exec_() == QDialog.Accepted:
        data = form.get_data()
        conn = get_sql_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                EXEC InsertOrMapData @WinClusterID = ?, @WinClusterIP = ?, @WinClusterName = ?, 
                @NodeID = ?, @NodeIP = ?, @NodeName = ?, @NodeOSVersion = ?, @NodeComments = ?, 
                @SQLClusterID = ?, @SQLClusterIP = ?, @SQLClusterName = ?, @SQLType = ?, @SQLInstanceName = ?, @SQLPort = ?, @SQLServerVersion = ?, 
                @NARsRaised = ?, @SQLComments = ?, @SQLServerEdition = ?, @MSDTCIP = ?, 
                @ApplicationID = ?, @AppName = ?, @AppOwner = ?, @AppOwnerEmail = ?, @AppVersion = ?, @AppDepartment = ?, @AppComments = ?, @AppCriticality = ?
                """, data)
            conn.commit()
            QMessageBox.information(self, "Success", "Inventory Details added successfully.")
            self.view_inventory()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        finally:
            conn.close()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def view_inventory(self):
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("EXECUTE [dbo].[Select_All_Data]")
    rows = cursor.fetchall()
    self.Inv_tab.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j in range(len(row)):
            self.Inv_tab.setItem(i, j, QTableWidgetItem(str(row[j])))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Windows Cluster Operations

def add_windows_cluster(self):
    form = WindowsClusterForm()
    if form.exec_() == QDialog.Accepted:
        data = form.get_data()
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO [dbo].[WindowsCluster] (WinClusterID, WinClusterIP, WinClusterName) VALUES (?, ?, ?)", data[:3])
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Windows Cluster added successfully.")
        self.view_windows_cluster()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def view_windows_cluster(self):
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [Inv].[dbo].[WindowsCluster]")
    rows = cursor.fetchall()
    self.WinCTable.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j in range(len(row)):
            self.WinCTable.setItem(i, j, QTableWidgetItem(str(row[j])))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def update_windows_cluster(self):
    selected_row = self.WinCTable.currentRow()
    if selected_row < 0:
        QMessageBox.warning(self, "Update Item", "Please select an item to update.")
        return
    win_cluster_id = self.WinCTable.item(selected_row, 0).text()
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT WinClusterID, WinClusterIP, WinClusterName FROM [dbo].[WindowsCluster] WHERE WinClusterID = ?", (win_cluster_id,))
    record = cursor.fetchone()
    conn.close()
    if not record:
        QMessageBox.warning(self, "Error", "Could not retrieve details for the selected Windows Cluster.")
        return
    form = WindowsClusterForm(WindowsClusterID=record[0], WindowsClusterIP=record[1], WindowsClusterName=record[2])
    if form.exec_() == QDialog.Accepted:
        data = form.get_data()
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE [dbo].[WindowsCluster] SET WinClusterIP=?, WinClusterName=? WHERE WinClusterID=?", (data[1], data[2], data[0]))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Windows Cluster updated successfully.")
        self.view_windows_cluster()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def delete_windows_cluster(self):
    selected_row = self.WinCTable.currentRow()
    if selected_row < 0:
        QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
        return
    conn = get_sql_connection()
    cursor = conn.cursor()
    try:
        current_win_cluster_id = self.WinCTable.item(selected_row, 0).text()
        cursor.execute("DELETE FROM [dbo].[WindowsCluster] WHERE WinClusterID=?", (current_win_cluster_id,))
        conn.commit()
        QMessageBox.information(self, "Success", "Windows Cluster deleted successfully.")
        self.view_windows_cluster()
    except Exception as e:
        QMessageBox.critical(self, "Database Error", str(e))
    finally:
        conn.close()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Node Operations

def add_node(self):
    form = NodeForm()
    if form.exec_() == QDialog.Accepted:
        data = form.get_data()
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO [dbo].[Node] (NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments, WinClusterID) VALUES (?, ?, ?, ?, ?, ?)", data[:6])
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Node added successfully.")
        self.view_node()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def view_node(self):
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [Inv].[dbo].[Node]")
    rows = cursor.fetchall()
    self.NodeTable.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j in range(len(row)):
            self.NodeTable.setItem(i, j, QTableWidgetItem(str(row[j])))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def update_node(self):
    selected_row = self.NodeTable.currentRow()
    if selected_row < 0:
        QMessageBox.warning(self, "Update Item", "Please select an item to update.")
        return
    node_id = self.NodeTable.item(selected_row, 0).text()
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments, WinClusterID FROM [dbo].[Node] WHERE NodeID = ?", (node_id,))
    record = cursor.fetchone()
    conn.close()
    if not record:
        QMessageBox.warning(self, "Error", "Could not retrieve details for the selected Node.")
        return
    form = NodeForm(NodeID=record[0], NodeIP=record[1], NodeName=record[2], NodeOSVersion=record[3], NodeComments=record[4], WinClusterID=record[5])
    if form.exec_() == QDialog.Accepted:
        data = form.get_data()
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE [dbo].[Node] SET NodeIP=?, NodeName=?, NodeOSVersion=?, NodeComments=?, WinClusterID=? WHERE NodeID=?", (data[1], data[2], data[3], data[4], data[5], data[0]))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Node updated successfully.")
        self.view_node()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def delete_node(self):
    selected_row = self.NodeTable.currentRow()
    if selected_row < 0:
        QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
        return
    conn = get_sql_connection()
    cursor = conn.cursor()
    try:
        current_node_id = self.NodeTable.item(selected_row, 0).text()
        cursor.execute("DELETE FROM [dbo].[Node] WHERE NodeID=?", (current_node_id,))
        conn.commit()
        QMessageBox.information(self, "Success", "Node deleted successfully.")
        self.view_node()
    except Exception as e:
        QMessageBox.critical(self, "Database Error", str(e))
    finally:
        conn.close()    

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%       
#SQL Cluster Operation 

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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def view_sql_cluster(self):
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [Inv].[dbo].[SQLCluster]")
    rows1 = cursor.fetchall()        
    self.SQLCTable.setRowCount(len(rows1))
    for i, row in enumerate(rows1):
        for j in range(len(row)):
            self.SQLCTable.setItem(i, j, QTableWidgetItem(str(row[j])))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def update_sql_cluster(self):
    selected_row_SQLC = self.SQLCTable.currentRow()
    if selected_row_SQLC < 0:
        QMessageBox.warning(self, "Update Item", "Please select an item to update.")
        return
    sql_cluster_id = self.SQLCTable.item(selected_row_SQLC, 0).text()

    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute(
    """
    SELECT SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, 
           SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP 
    FROM [dbo].[SQLCluster] 
    WHERE SQLClusterID = ?
    """, 
    (sql_cluster_id,)
        )
    record = cursor.fetchone()
    conn.close()
    if not record:
        QMessageBox.warning(self, "Error", "Could not retrieve details for the selected SQL Cluster.")
        return
    form = SQLClusterForm(SQLClusterID=record[0], SQLClusterIP=record[1], SQLClusterName=record[2],SQLType=record[3], SQLInstanceName=record[4], SQLPort=record[5], SQLServerVersion=record[6], NARsRaised=record[7], SQLComments=record[8], SQLServerEdition=record[9], MSDTCIP=record[10])
    #form = SQLClusterForm()
    if form.exec_() == QDialog.Accepted:
        data = form.get_data()
        conn = get_sql_connection()
        cursor = conn.cursor()
        print(f"Updating Data as {data}")
        cursor.execute("UPDATE [dbo].[SQLCluster] SET SQLClusterIP=?, SQLClusterName=?, SQLType=?, SQLInstanceName=?, SQLPort=?, SQLServerVersion=?, NARsRaised=?, SQLComments=?, SQLServerEdition=?, MSDTCIP=? WHERE SQLClusterID=?", (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[0]))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "SQL Cluster updated successfully.")
        self.view_sql_cluster()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def delete_sql_cluster(self):
    del_selected_row = self.SQLCTable.currentRow()
    if del_selected_row < 0:
        QMessageBox.warning(self, "Delete Item", "Please select an item to delete.")
        return
    conn = get_sql_connection()
    cursor = conn.cursor()
    try:
        current_SQLClusterID = self.SQLCTable.item(del_selected_row, 0).text()
        print(f"Deleting SQLCluster with ID: {current_SQLClusterID}")
        cursor.execute("DELETE FROM [dbo].[SQLCluster] WHERE SQLClusterID=?", (current_SQLClusterID,))
        conn.commit()
        QMessageBox.information(self, "Success", "SQL Cluster deleted successfully.")
        self.view_sql_cluster()
    except Exception as e:
        QMessageBox.critical(self, "Database Error", str(e))
    finally:
        conn.close()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Application Operation 

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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def view_application(self):
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [Inv].[dbo].[Application]")
    rows1 = cursor.fetchall()        
    self.AppTable.setRowCount(len(rows1))
    for i, row in enumerate(rows1):
        for j in range(len(row)):
            self.AppTable.setItem(i, j, QTableWidgetItem(str(row[j])))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def update_application(self):
    selected_row_App = self.AppTable.currentRow()
    if selected_row_App < 0:
        QMessageBox.warning(self, "Update Item", "Please select an item to update.")
        return
    application_id = self.AppTable.item(selected_row_App, 0).text()
    
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute(
    """
    SELECT ApplicationID, AppName, AppOwner, AppOwnerEmail, AppVersion, 
           AppDepartment, AppComments, AppCriticality 
    FROM [dbo].[Application] 
    WHERE ApplicationID = ?
    """, 
    (application_id,)
            )
    record = cursor.fetchone()
    conn.close()
    if not record:
        QMessageBox.warning(self, "Error", "Could not retrieve details for the selected application.")
        return
    form = ApplicationForm(ApplicationID=record[0],AppName=record[1],AppOwner=record[2],
    AppOwnerEmail=record[3],AppVersion=record[4],AppDepartment=record[5],AppComments=record[6],
    AppCriticality=record[7]
    )
    #form = ApplicationForm()
    if form.exec_() == QDialog.Accepted:
        data = form.get_data()
        conn = get_sql_connection()
        cursor = conn.cursor()
        print(f"Updating Data as {data}")            
        cursor.execute("UPDATE [dbo].[Application] SET AppName=?, AppOwner=?, AppOwnerEmail=?, AppVersion=?, AppDepartment=?, AppComments=?, AppCriticality=? WHERE ApplicationID=?", (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[0]))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Application updated successfully.")
        self.view_application()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%