import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os, sys

ventana = False 
ventan2 = False
ventanamaterias = False

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    ventana.wm_attributes("-topmost", 1)

def rutas1(ruta1):
    try:
        rutabase = sys.__MEIPASS
    except Exception:
        rutabase = os.path.abspath(".")
    return os.path.join(rutabase, ruta1)

def Rn1(master, nivel):
    Vn = tk.Toplevel(master)
    Vn.title("Registro de Notas")
    centrar_ventana(Vn, 800, 600)
    Vn.resizable(width=False, height=False)
    
    # Importar icono y fondo
    ruta1 = rutas1(r"Imag\Log.ico")
    ruta2 = rutas1(r"Imag\f1.png")
    Vn.iconbitmap(ruta1)
    fv = tk.PhotoImage(file=ruta2)
    tk.Label(Vn, image=fv).place(x=0, y=0, relheight=1, relwidth=1)

    nb = ttk.Notebook(Vn)
    pe1 = tk.Frame(nb); pe2 = tk.Frame(nb)
    nb.add(pe1, text="Materias")
    nb.pack(); nb.config(height=200, width=600); nb.place(x=100, y=150)

    # Frame para la lista de materias
    frame_materias = ttk.Frame(pe1)
    frame_materias.pack(fill=tk.BOTH, expand=1)

    # Treeview para mostrar las materias
    columns_materias = ("ID", "Nombre", "Abreviatura", "Año", "CI Docente", "Nombre Docente")
    tree_materias = ttk.Treeview(frame_materias, columns=columns_materias, show="headings")
    
    for col in columns_materias:
        tree_materias.heading(col, text=col)
        tree_materias.column(col, width=120 if col == "ID" else 200, stretch=tk.NO)
    
    scrollbar_materias = ttk.Scrollbar(frame_materias, orient="vertical", command=tree_materias.yview)
    tree_materias.configure(yscrollcommand=scrollbar_materias.set)
    scrollbar_materias.pack(side="right", fill="y")

    scrollhmaterias = ttk.Scrollbar(frame_materias, orient="horizontal", command=tree_materias.xview)
    tree_materias.configure(xscrollcommand=scrollhmaterias.set)
    scrollhmaterias.pack(side="bottom", fill="x")
    tree_materias.pack(fill="both", expand=True)

    # Función para cargar las materias en el Treeview
    def cargar_materias():
        dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        dirbasededatos = os.path.join(dirantbase, 'DB')
        pathdb = os.path.join(dirbasededatos, 'db')

        for item in tree_materias.get_children():
            tree_materias.delete(item)
        
        co = sqlite3.connect(pathdb)
        cur = co.cursor()
        try:
            cur.execute('''SELECT id, nombre, abreviatura, anio, ci_docente, n_docente 
                        FROM materias''')
            for materia in cur.fetchall():
                tree_materias.insert("", "end", values=materia)
        finally:
            cur.close()
            co.close()

    # Cargar las materias al iniciar la ventana
    cargar_materias()

    # Función para mostrar estudiantes de una materia
    def mostrar_estudiantes_materia(materia_id, anio):
        global ventana

        if not ventana:
            ventana = True
            ventana_estudiantes = tk.Toplevel(Vn)
            ventana_estudiantes.title("Estudiantes de la Materia")
            centrar_ventana(ventana_estudiantes, 800, 300)
            ventana_estudiantes.resizable(width=False, height=False)

            # Frame para la lista de estudiantes
            frame_estudiantes = ttk.Frame(ventana_estudiantes)
            frame_estudiantes.pack(fill="both", expand=True, padx=10, pady=10)

            # Treeview para mostrar los estudiantes
            columns_estudiantes = ("ID", "Nombre", "Apellido", "Edad", "Año", "Nota 1er Lapso", "Nota 2do Lapso", "Nota 3er Lapso")
            tree_estudiantes = ttk.Treeview(frame_estudiantes, columns=columns_estudiantes, show="headings")
            
            for col in columns_estudiantes:
                tree_estudiantes.heading(col, text=col)
                tree_estudiantes.column(col, width=120 if col == "ID" else 150, stretch=tk.NO)
            
            scrollbar_estudiantes = ttk.Scrollbar(frame_estudiantes, orient="vertical", command=tree_estudiantes.yview)
            tree_estudiantes.configure(yscrollcommand=scrollbar_estudiantes.set)
            scrollbar_estudiantes.pack(side="right", fill="y")

            scrollh_estudiantes = ttk.Scrollbar(frame_estudiantes, orient="horizontal", command=tree_estudiantes.xview)
            tree_estudiantes.configure(xscrollcommand=scrollh_estudiantes.set)
            scrollh_estudiantes.pack(side="bottom", fill="x")
            tree_estudiantes.pack(fill="both", expand=True)

            # Función para cargar los estudiantes de la materia
            def cargar_estudiantes():
                dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                dirbasededatos = os.path.join(dirantbase, 'DB')
                pathdb = os.path.join(dirbasededatos, 'db')

                for item in tree_estudiantes.get_children():
                    tree_estudiantes.delete(item)
                
                co = sqlite3.connect(pathdb)
                cur = co.cursor()
                try:
                    cur.execute('''SELECT est.id, est.nombres, est.apellidos, est.edad, ac.anio_a_cursar,
                                    (SELECT nota FROM notas WHERE estudiante_id = est.id AND materia_id = ? AND lapso = 1),
                                    (SELECT nota FROM notas WHERE estudiante_id = est.id AND materia_id = ? AND lapso = 2),
                                    (SELECT nota FROM notas WHERE estudiante_id = est.id AND materia_id = ? AND lapso = 3)
                                FROM estudiantes est
                                JOIN academicos ac ON est.id = ac.estudiante_id
                                JOIN estudiante_materias em ON est.id = em.estudiante_id
                                WHERE em.materia_id = ? AND ac.anio_a_cursar = ?''', (materia_id, materia_id, materia_id, materia_id, anio))
                    for estudiante in cur.fetchall():
                        tree_estudiantes.insert("", "end", values=estudiante)
                finally:
                    cur.close()
                    co.close()

            # Cargar los estudiantes al iniciar la ventana
            cargar_estudiantes()

            def c1():
                global ventana
                ventana = False
                ventana_estudiantes.destroy()

            ventana_estudiantes.protocol("WM_DELETE_WINDOW",c1)

            # Función para ingresar notas
            def ingresar_notas(estudiante_id, materia_id):
                global ventan2 

                if not ventan2:
                    ventan2 = True
                    ventana_notas = tk.Toplevel(ventana_estudiantes)
                    ventana_notas.title("Ingresar Notas")
                    centrar_ventana(ventana_notas, 400, 300)
                    ventana_notas.resizable(width=False, height=False)

                    # Entradas para las notas
                    tk.Label(ventana_notas, text="Nota 1er Lapso:").grid(row=0, column=0, padx=10, pady=10)
                    entry_nota1 = tk.Entry(ventana_notas)
                    entry_nota1.grid(row=0, column=1, padx=10, pady=10)

                    tk.Label(ventana_notas, text="Nota 2do Lapso:").grid(row=1, column=0, padx=10, pady=10)
                    entry_nota2 = tk.Entry(ventana_notas)
                    entry_nota2.grid(row=1, column=1, padx=10, pady=10)

                    tk.Label(ventana_notas, text="Nota 3er Lapso:").grid(row=2, column=0, padx=10, pady=10)
                    entry_nota3 = tk.Entry(ventana_notas)
                    entry_nota3.grid(row=2, column=1, padx=10, pady=10)

                    # Función para guardar las notas
                    def guardar_notas():
                        global ventan2
                        nota1 = entry_nota1.get()
                        nota2 = entry_nota2.get()
                        nota3 = entry_nota3.get()

                        # Validar que las notas sean números
                        try:
                            nota1 = float(nota1) if nota1 else None
                            nota2 = float(nota2) if nota2 else None
                            nota3 = float(nota3) if nota3 else None

                            # Validar que las notas estén en el rango [0, 20]
                            if nota1 is not None and (nota1 <= 0 or nota1 > 20):
                                messagebox.showerror("Error", "La nota del primer lapso debe estar entre 0 y 20")
                                return
                            if nota2 is not None and (nota2 <= 0 or nota2 > 20):
                                messagebox.showerror("Error", "La nota del segundo lapso debe estar entre 0 y 20")
                                return
                            if nota3 is not None and (nota3 <= 0 or nota3 > 20):
                                messagebox.showerror("Error", "La nota del tercer lapso debe estar entre 0 y 20")
                                return
                            
                        except ValueError:
                            messagebox.showerror("Error", "Las notas deben ser números válidos")
                            return

                        # Validar que las notas de los lapsos anteriores estén registradas
                        if nota2 is not None and nota1 is None:
                            if not messagebox.askyesno("Advertencia", "Hay estudiantes sin nota del primer lapso. ¿Desea continuar?"):
                                return
                        if nota3 is not None and (nota1 is None or nota2 is None):
                            if not messagebox.askyesno("Advertencia", "Hay estudiantes sin nota del primer o segundo lapso. ¿Desea continuar?"):
                                return

                        # Guardar las notas en la base de datos
                        dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                        dirbasededatos = os.path.join(dirantbase, 'DB')
                        pathdb = os.path.join(dirbasededatos, 'db')

                        co = sqlite3.connect(pathdb)
                        cur = co.cursor()
                        try:
                            # Verificar si ya existe una nota para el primer lapso
                            if nota1 is not None:
                                cur.execute("SELECT id FROM notas WHERE estudiante_id = ? AND materia_id = ? AND lapso = 1", 
                                            (estudiante_id, materia_id))
                                if cur.fetchone():
                                    messagebox.showerror("Error", "Ya existe una nota para el primer lapso de este estudiante en esta materia")
                                    return

                            # Verificar si ya existe una nota para el segundo lapso
                            if nota2 is not None:
                                cur.execute("SELECT id FROM notas WHERE estudiante_id = ? AND materia_id = ? AND lapso = 2", 
                                            (estudiante_id, materia_id))
                                if cur.fetchone():
                                    messagebox.showerror("Error", "Ya existe una nota para el segundo lapso de este estudiante en esta materia")
                                    return

                            # Verificar si ya existe una nota para el tercer lapso
                            if nota3 is not None:
                                cur.execute("SELECT id FROM notas WHERE estudiante_id = ? AND materia_id = ? AND lapso = 3", 
                                            (estudiante_id, materia_id))
                                if cur.fetchone():
                                    messagebox.showerror("Error", "Ya existe una nota para el tercer lapso de este estudiante en esta materia")
                                    return

                            # Insertar las notas si no existen
                            if nota1 is not None:
                                cur.execute("INSERT INTO notas (estudiante_id, materia_id, lapso, nota) VALUES (?, ?, 1, ?)", 
                                            (estudiante_id, materia_id, nota1))
                            if nota2 is not None:
                                cur.execute("INSERT INTO notas (estudiante_id, materia_id, lapso, nota) VALUES (?, ?, 2, ?)", 
                                            (estudiante_id, materia_id, nota2))
                            if nota3 is not None:
                                cur.execute("INSERT INTO notas (estudiante_id, materia_id, lapso, nota) VALUES (?, ?, 3, ?)", 
                                            (estudiante_id, materia_id, nota3))

                            co.commit()
                            messagebox.showinfo("Éxito", "Notas guardadas correctamente")
                            ventan2 = False
                            ventana_notas.destroy()
                            cargar_estudiantes()  # Refrescar la lista de estudiantes
                        except sqlite3.Error as e:
                            messagebox.showerror("Error", f"Error al guardar las notas: {str(e)}")
                        finally:
                            cur.close()
                            co.close()

                    def c2():
                        global ventan2
                        ventan2 = False
                        ventana_notas.destroy()

                    ventana_notas.protocol("WM_DELETE_WINDOW",c2)
                    # Botón para guardar las notas
                    tk.Button(ventana_notas, text="Guardar Notas", command=guardar_notas).grid(row=3, column=0, columnspan=2, pady=10)
                else:
                    return

            # Evento de doble clic en un estudiante
            def dclick_estudiante(event):
                item = tree_estudiantes.selection()[0]
                valores = tree_estudiantes.item(item, 'values')
                estudiante_id = valores[0]
                ingresar_notas(estudiante_id, materia_id)
                
            tree_estudiantes.bind("<Double-1>", dclick_estudiante)
        else:
            return

    # Evento de doble clic en una materia
    def dclick_materia(event):
        item = tree_materias.selection()[0]
        valores = tree_materias.item(item, 'values')
        materia_id = valores[0]
        anio = valores[3]
        mostrar_estudiantes_materia(materia_id, anio)

    tree_materias.bind("<Double-1>", dclick_materia)

    def comeback():
            Vn.destroy()
            if nivel == 1:
                from Ventanas.menu import M1
                M1(master, 1)
            if nivel == 2:
                from Ventanas.menu import M2
                M2(master, 2)
            if nivel == 3:
                from Ventanas.menu import M3
                M3(master, 3)
    
    Vn.protocol("WM_DELETE_WINDOW", comeback)

    # Dentro de la función Rn1(master, nivel):

    def filtrar_materias():
        global ventanamaterias

        if not ventanamaterias:
            ventanamaterias = True
            pop = tk.Toplevel(Vn)  # Cambiar Vc por Vn
            pop.title("Filtrar Materias")
            centrar_ventana(pop, 400, 400)
            pop.resizable(width=False, height=False)
            pop.iconbitmap(ruta1)  # Asegúrate de que ruta1 esté definida
            pop.wm_attributes("-topmost", 1)

            nb = ttk.Notebook(pop)
            pf1 = tk.Frame(nb); pf2 = tk.Frame(nb)
            nb.add(pf1, text="Datos Básicos"); nb.add(pf2, text="Otros")
            nb.pack(fill=tk.BOTH, expand=1)
            
            # Pestaña 1 - Datos Básicos
            frame1 = tk.Frame(pf1)
            frame1.pack(pady=10)
            
            # Campo Nombre
            tk.Label(frame1, text="Nombre:", font=("Cascadia Mono", 8)).grid(row=0, column=0, sticky=tk.W)
            e_nombre = tk.Entry(frame1, width=25)
            e_nombre.grid(row=0, column=1, padx=5)
            
            # Campo Abreviatura
            tk.Label(frame1, text="Abreviatura:", font=("Cascadia Mono", 8)).grid(row=1, column=0, sticky=tk.W)
            e_abreviatura = tk.Entry(frame1, width=10)
            e_abreviatura.grid(row=1, column=1, padx=5)
            
            # Pestaña 2 - Otros
            frame2 = tk.Frame(pf2)
            frame2.pack(pady=10)
            
            # Año
            tk.Label(frame2, text="Año:", font=("Cascadia Mono", 8)).grid(row=0, column=0, sticky=tk.W)
            combo_anio = ttk.Combobox(frame2, values=["1er Año", "2do Año", "3er Año", "4to Año", "5to Año", "6to Año"], state="readonly")
            combo_anio.grid(row=0, column=1, padx=5)
            
            # CI Docente
            tk.Label(frame2, text="CI Docente:", font=("Cascadia Mono", 8)).grid(row=1, column=0, sticky=tk.W)
            e_ci_docente = tk.Entry(frame2, width=15)
            e_ci_docente.grid(row=1, column=1, padx=5)
            
            # Validación
            def validacion_materias():
                ci_docente = e_ci_docente.get()
                
                if ci_docente and not ci_docente.isdigit():
                    messagebox.showerror("Error", "El CI del docente debe ser numérico")
                    return False
                
                return True

            def filtrar():
                global ventanamaterias
                if not validacion_materias():
                    return
                
                # Recoger parámetros
                nombre = e_nombre.get().strip()
                abreviatura = e_abreviatura.get().strip()
                anio = combo_anio.get()
                ci_docente = e_ci_docente.get().strip()
                
                # Construir consulta
                query = "SELECT id, nombre, abreviatura, anio, ci_docente, n_docente FROM materias"
                conditions = []
                params = []
                
                if nombre:
                    conditions.append("nombre LIKE ?")
                    params.append(f"%{nombre}%")
                
                if abreviatura:
                    conditions.append("abreviatura LIKE ?")
                    params.append(f"%{abreviatura}%")
                
                if anio:
                    conditions.append("anio = ?")
                    params.append(anio)
                
                if ci_docente:
                    conditions.append("ci_docente = ?")
                    params.append(ci_docente)
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                # Ejecutar consulta
                dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                dirbasededatos = os.path.join(dirantbase, 'DB')
                pathdb = os.path.join(dirbasededatos, 'db')
                
                try:
                    co = sqlite3.connect(pathdb)
                    cur = co.cursor()
                    
                    # Limpiar Treeview
                    for item in tree_materias.get_children():
                        tree_materias.delete(item)
                    
                    cur.execute(query, params)
                    materias = cur.fetchall()
                    
                    if not materias:
                        messagebox.showinfo("Información", "No se encontraron resultados con los filtros aplicados")
                    else:
                        for materia in materias:
                            tree_materias.insert("", "end", values=materia)
                            
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error en la base de datos:\n{str(e)}")
                finally:
                    cur.close()
                    co.close()
                
                ventanamaterias = False
                pop.destroy()
            
            def cefiltrarmaterias(ventana):
                global ventanamaterias
                ventanamaterias = False
                ventana.destroy()

            pop.protocol("WM_DELETE_WINDOW", lambda: cefiltrarmaterias(pop))
            tk.Button(pop, text="Filtrar", font=("Cascadia Mono", 8), bg="light green", command=filtrar).pack(pady=10)
        else:
            return

    bt_filtrar_materias = tk.Button(Vn, text="Filtrar Materias", font=("Cascadia Mono",8), bg="light green", command=filtrar_materias)
    bt_filtrar_materias.place(x=250, y=500)

    bt3 = tk.Button(Vn,text="Regresar",font=("Cascadia Mono",12), command=comeback); bt3.pack(); 
    bt3.place(x=150,y=500)

    Vn.mainloop()