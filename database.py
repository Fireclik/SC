import sqlite3
import os

# Obtener la ruta del archivo de la base de datos en la carpeta "base_de_datos" 
database_dir = os.path.join(os.path.dirname(__file__), 'base_de_datos') 
os.makedirs(database_dir, exist_ok=True) # Crear la carpeta si no existe 
database_path = os.path.join(database_dir, 'estu.db')

def dbin():
    co = sqlite3.connect(database_path)
    cur = co.cursor()
    cur.execute(''' CREATE TABLE IF NOT EXISTS estudiantes (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                edad INTEGER NOT NULL,
                ano TEXT NOT NULL
                ) ''')
    co.commit()
    co.close()
def execconsulta(consulta, params=()):
    co = sqlite3.connect(database_path)
    cur = co.cursor()
    cur.execute(consulta, params)
    co.commit()
    co.close()
    
def fetchconsulta(consulta, params=()):
    co = sqlite3.connect(database_path)
    cur = co.cursor()
    cur.execute(consulta, params)
    resultados = cur.fetchall()
    co.commit()
    co.close()