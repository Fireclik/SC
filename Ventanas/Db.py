import sqlite3
import os

#Asignar directorio de la base de datos
dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
dirbasededatos = os.path.join(dirantbase,'DB')
os.makedirs(dirbasededatos, exist_ok=True)
pathdb = os.path.join(dirbasededatos,'db')

#Creacion de la base de datos
def dbbin():
    co = sqlite3.connect(pathdb)
    cur = co.cursor()

    #crear tabla de datos del estudiante
    cur.execute('''CREATE TABLE IF NOT EXISTS estudiantes (
                    id INTEGER PRIMARY KEY,
                    nombres TEXT,
                    apellidos TEXT,
                    fecha_nacimiento TEXT,
                    edad INTEGER,
                    sexo TEXT,
                    lugar_nacimiento TEXT,
                    nacionalidad TEXT,
                    ci_estudiante TEXT,
                    cedula_escolar TEXT,
                    estatura REAL,
                    peso REAL,
                    talla_zapato INTEGER,
                    talla_camisa TEXT,
                    talla_pantalon TEXT,
                    enfermedad_cronica TEXT,
                    observaciones TEXT
                )''')

    # Crear tabla de datos de contactos 
    cur.execute('''CREATE TABLE IF NOT EXISTS contactos (
                    id INTEGER PRIMARY KEY,
                    direccion TEXT,
                    telefono_movil TEXT,
                    email TEXT
                )''')

    # Crear tabla de relacion entre contactos y estudiantes
    cur.execute('''CREATE TABLE IF NOT EXISTS estudiantes_contactos (
                    estudiante_id INTEGER,
                    contacto_id INTEGER,
                    FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
                    FOREIGN KEY (contacto_id) REFERENCES contactos (id)
                )''')

    # Crear tabla de datos académicos 
    cur.execute('''CREATE TABLE IF NOT EXISTS academicos (
                    id INTEGER PRIMARY KEY,
                    anio_a_cursar TEXT,
                    repite TEXT,
                    estudiante_id INTEGER,
                    FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id)
                )''')

    # Crear tabla de materias
    cur.execute('''CREATE TABLE IF NOT EXISTS materias (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    codigo TEXT,
                    abreviatura TEXT,
                    anio TEXT,
                    ci_docente TEXT,
                    n_docente TEXT
                )''')

    # Crear tabla de relación estudiante-materias
    cur.execute('''CREATE TABLE IF NOT EXISTS estudiante_materias (
                    estudiante_id INTEGER,
                    materia_id INTEGER,
                    es_pendiente BOOLEAN,
                    FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
                    FOREIGN KEY (materia_id) REFERENCES materias (id)
                )''')

    # Crear tabla de notas
    cur.execute('''CREATE TABLE IF NOT EXISTS notas (
                    id INTEGER PRIMARY KEY,
                    estudiante_id INTEGER,
                    materia_id INTEGER,
                    lapso INTEGER,
                    nota REAL,
                    FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
                    FOREIGN KEY (materia_id) REFERENCES materias (id)
                )''')

    # Crear tabla de ajustes
    cur.execute('''CREATE TABLE IF NOT EXISTS ajustes (
                    id INTEGER PRIMARY KEY,
                    estudiante_id INTEGER,
                    materia_id INTEGER,
                    puntos_ajustados INTEGER,
                    FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
                    FOREIGN KEY (materia_id) REFERENCES materias (id)
                )''')

    # Crear tabla de datos sobre padres/madres/representantes 
    cur.execute('''CREATE TABLE IF NOT EXISTS adultos (
                    id INTEGER PRIMARY KEY,
                    nombre_apellido TEXT,
                    ci TEXT,
                    direccion TEXT,
                    vive_con_estudiante TEXT,
                    telefono_movil TEXT,
                    telefono_habitacion TEXT,
                    trabaja TEXT,
                    telefono_trabajo TEXT,
                    email TEXT
                )''')

    # Crear tabla de relación estudiante-adulto con que tipo de relacion tiene con el estudiante
    cur.execute('''CREATE TABLE IF NOT EXISTS estudiante_adultos (
                    estudiante_id INTEGER,
                    adulto_id INTEGER,
                    tipo_relacion TEXT, -- Puede ser 'padre', 'madre' o 'representante'
                    FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
                    FOREIGN KEY (adulto_id) REFERENCES adultos (id)
                )''')

    co.commit()
    co.close()

def execcons(cons, param=()):
    co = sqlite3.connect(pathdb)
    cur = co.cursor()
    cur.execute(cons, param)
    co.commit()
    co.close()

def exselccons(cons, param=()):
    co = sqlite3.connect(pathdb)
    cur = co.cursor()
    cur.execute(cons,param)
    rr = cur.fetchall()
    co.commit()
    co.close()