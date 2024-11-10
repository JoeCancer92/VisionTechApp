import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            database='rec_db'  # Cambia por el nombre de tu base de datos
        )

        if conexion.is_connected():
            return conexion

    except Error as e:
        raise Exception(f"Error al conectar a la base de datos: {e}")