import pyodbc
from PyQt5.QtWidgets import QMessageBox

def get_sql_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=Inv;'
        'UID=django;'
        'PWD=Charan@1999'
    )
    return conn

def get_nodes():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT NODEID, NODENAME FROM [INV].[DBO].[NODE]")
    nodes = cursor.fetchall()
    conn.close()
    return nodes

def get_sql_clusters():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SQLCLUSTERID, SQLCLUSTERNAME FROM [INV].[DBO].[SQLCLUSTER]")
    sql_clusters = cursor.fetchall()
    conn.close()
    return sql_clusters

def get_applications():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT APPLICATIONID, APPNAME FROM [INV].[DBO].[APPLICATION]")
    applications = cursor.fetchall()
    conn.close()
    return applications

def insert_node_sql_cluster(node_id, sql_cluster_id):
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO NodeSQLCluster (NodeID, SQLClusterID) VALUES (?, ?)", (node_id, sql_cluster_id))
        conn.commit()
        conn.close()
        QMessageBox.information(None, "Success", "Mapping Between Node And SQLCluster Is Successful!")
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))

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

def insert_sql_cluster_application(sql_cluster_id, application_id):
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO SQLClusterApplication (SQLClusterID, ApplicationID) VALUES (?, ?)", (sql_cluster_id, application_id))
        conn.commit()
        conn.close()
        QMessageBox.information(None, "Success", "Mapping Between SQLCluster And Application Is Successful!")
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))

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
