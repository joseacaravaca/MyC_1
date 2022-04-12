import pandas
import pymysql

dbr_usuario = 'jacv'
dbr_pass = 'karabaka66974'
database_name = 'controlaccesos'
mhost = '127.0.0.1'
mport=3306


#-------------------------------------------------------------------------------------
def mysql_connect():
    #Conecta con Mysql Server
    #return connection: Global MySQL database connection

    global connection

    connection = pymysql.connect(
        host=mhost,
        user=dbr_usuario,
        passwd=dbr_pass,
        db=database_name,
        port=mport
    )
#-----------------------------------------------------------------------------------
def run_query(sql):
    #Ejecuta una consulta SQL.
    #param sql: MySQL query
    #return: Pandas dataframe containing results

    return pandas.read_sql_query(sql, connection)
#-----------------------------------------------------------------------------------
def run_query(sql):
    """Runs a given SQL query via the global database connection.

    :param sql: MySQL query
    :return: Pandas dataframe containing results
    """

    return pandas.read_sql_query(sql, connection)
#-----------------------------------------------------------------------------------
def mysql_disconnect():
    #Closes the MySQL database connection.
    connection.close()
#-----------------------------------------------------------------------------------
def empleado (chip,puerta):
    mysql_connect()
    df = run_query( 
    "SELECT emp_nombre,emp_apellidos,emp_pue" + puerta + 
    " FROM empleados where " + 
    " (emp_chip=" + chip + ") OR" +
    " (emp_chip1=" + chip + ") OR" +
    " (emp_chip2=" + chip + ");")
    mysql_disconnect()
    return df.head(1)
    