import tkinter as tk
import os
import sqlite3
from tkinter import ttk, messagebox

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

# Definición de menú
def Con1():
    Vc = tk.Tk()
    Vc.title("Consulta")
    centrar_ventana(Vc, 800, 600)
    Vc.resizable(width=False, height=False)
    # Importar icono
    icdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    icodir = os.path.join(icdir, 'imag') 
    icopath = os.path.join(icodir, 'Log.ico') 
    Vc.iconbitmap(icopath)
    # Importar imagen fondo
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    idir = os.path.join(dir, 'imag')
    ipath = os.path.join(idir, 'f1.png')
    fv = tk.PhotoImage(file=ipath)
    tk.Label(Vc, image=fv).place(x=0, y=0, relheight=1, relwidth=1)

    def consultar_estudiantes():
        dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        dirbasededatos = os.path.join(dirantbase, 'DB')
        pathdb = os.path.join(dirbasededatos, 'db')

        # Limpiar el contenido anterior del Treeview
        for item in tree.get_children():
            tree.delete(item)
        
        # Conectar con la base de datos
        co = sqlite3.connect(pathdb)
        cur = co.cursor()
        
        try:
            # Consultar todos los datos de los estudiantes, contactos y académicos
            cur.execute('''SELECT est.id, est.nombres, est.apellidos, est.edad, est.sexo, est.nacionalidad, est.ci_estudiante, est.cedula_escolar,
                                  est.Pasaporte, est.estatura, est.peso, est.talla_zapato, est.talla_camisa, est.talla_pantalon, est.enfermedad_cronica, 
                                  est.observaciones, con.direccion, con.telefono_movil, con.email, ac.anio_a_cursar, ac.repite
                        FROM estudiantes est
                        LEFT JOIN estudiantes_contactos ec ON est.id = ec.estudiante_id
                        LEFT JOIN contactos con ON ec.contacto_id = con.id
                        LEFT JOIN academicos ac ON est.id = ac.estudiante_id''')
            estudiantes = cur.fetchall()
            
            for estudiante in estudiantes:
                tree.insert("", "end", values=estudiante)
        
        except sqlite3.Error as e:
            print("Hubo un problema con la operacion en la base de datos: ", e)
        
        finally:
            cur.close()
            co.close()

    nb = ttk.Notebook(Vc)
    pe1 = tk.Frame(nb)
    nb.add(pe1, text="Consulta de Estudiantes")
    nb.pack(); nb.config(height=300, width=600); nb.place(x=100, y=150)

    frame = ttk.Frame(pe1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Crear el Treeview con scrollbar
    columns = ("ID", "Nombres", "Apellidos", "Edad", "Sexo", "Nacionalidad", "CI Estudiante", "Cédula Escolar",
               "Pasaporte", "Estatura", "Peso", "Talla de Zapatos", "Talla Camisas", "Talla Pantalon",
               "Enfermedad Cronica", "Observaciones", "Direccion", "Telefono Movil", "Email", "Año a Cursar", "Repite")
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, stretch=tk.NO)

    # Scrollbar vertical
    scrollbar_vertical = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_vertical.set)
    scrollbar_vertical.pack(side="right", fill="y")

    # Scrollbar horizontal
    scrollbar_horizontal = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar_horizontal.set)
    scrollbar_horizontal.pack(side="bottom", fill="x")

    tree.pack(fill="both", expand=True)

    # Llamar a la función consultar_estudiantes al abrir la ventana
    consultar_estudiantes()

    Vc.mainloop()

Con1()
