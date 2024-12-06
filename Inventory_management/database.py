import pyodbc,os,configparser
from PyQt5.QtWidgets import QMessageBox

def get_sql_connection():
    # Determine the path to config.ini relative to this script
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, 'config.ini')

    # Read the configuration file
    config = configparser.ConfigParser()
    config.read(config_path)

    # Retrieve the database connection details
    driver = config['database']['driver']
    server = config['database']['server']
    database = config['database']['database']
    uid = config['database']['uid']
    pwd = config['database']['pwd']

    conn_str = (
        f'DRIVER={{{driver}}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={uid};'
        f'PWD={pwd}'
    )

    # Establish the connection
    conn = pyodbc.connect(conn_str)

#    conn = pyodbc.connect(
#        'DRIVER={ODBC Driver 13 for SQL Server};'
#        'SERVER=localhost;'
#        'DATABASE=Inv;'
#        'UID=django;'
#        'PWD=Charan@1999'
#    )
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

#Function To Fetch Records From to Show as Dropdowns - Department
def get_department():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DEPTNAME FROM [INV].[DBO].[DEPARTMENT]")
    departments  = [row[0] for row in cursor.fetchall()]
    conn.close()
    return departments


#Function To Fetch Records From to Show as Dropdowns - Editions
def get_edition():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SQLEDITION FROM [INV].[DBO].[EDITIONS]")
    editions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return editions


#Function To Fetch Records From to Show as Dropdowns - OS Versions
def get_osVersion():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT OSVERSION FROM [INV].[DBO].[OSVERSIONS]")
    osVersions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return osVersions


#Function To Fetch Records From to Show as Dropdowns - SQLType 
def get_sqltype():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SQLTYPE FROM [INV].[DBO].[SQLTYPE]")
    sqltypes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sqltypes


#Function To Fetch Records From to Show as Dropdowns - SQLVersions
def get_sqlversion():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SQLVERSIONS FROM [INV].[DBO].[SQLVERSIONS]")
    sqlversions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sqlversions

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

                   