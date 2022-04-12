# Proyecto ConA
# Control de accesos mediante tarjerta 125 Khz basado en bbdd Mysql
# Programado en Python para una unidad autonoma basada en Raspberry pi 3B+
# v 1.0 enero 2022
# (c) José Antonio Caravaca Valdés

import pandas
import pymysql
from sshtunnel import SSHTunnelForwarder

ssh_host = 'www.ceeldense.es'
ssh_username = 'ftp_josean'
ssh_password = 'Josean#15.21'
dbr_usuario = 'jacaravaca'
dbr_pass = 'Josean#15.21'
database_name = 'bdd_cont'
localhost = '127.0.0.1'


def open_ssh_tunnel():
    #Abre un  SSH tunnel y conecta usando user y pass.
    #return tunnel: Global SSH tunnel connection

    global tunnel
    tunnel = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        remote_bind_address=('127.0.0.1', 3306)
    )

    tunnel.start()
#-------------------------------------------------------------------------------------
def mysql_connect():
    #Conecta con Mysql Server
    #return connection: Global MySQL database connection

    global connection

    connection = pymysql.connect(
        host='127.0.0.1',
        user=dbr_usuario,
        passwd=dbr_pass,
        db=database_name,
        port=tunnel.local_bind_port
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
def close_ssh_tunnel():
    #Closes the SSH tunnel connection.
    tunnel.close
#-----------------------------------------------------------------------------------
def socio (chip,puerta):
    open_ssh_tunnel()
    mysql_connect()
    df = run_query("SELECT torn_nomb,torn_apel,torn_foto, torn_pu" + puerta + " FROM g_torn01 where torn_chip=" + chip + ";")
    mysql_disconnect()
    close_ssh_tunnel()
    return df.head(1)
    
