import tkinter as tk
import os
import re
import sqlite3
from tkinter import ttk, messagebox

seleccion = " "; seestu = None
ventana = False; ventana2 = False; vm = False; 

seleccion_materia = " "
ventana_materia = False
ventanamaterias = False

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

    ventana.wm_attributes("-topmost", 1)

# Definición de menú
def Con1(master, nivel):
    Vc = tk.Toplevel(master)
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
    pe1 = tk.Frame(nb); pe2 = tk.Frame(nb)
    nb.add(pe1, text="Consulta de Estudiantes"); nb.add(pe2, text="Consulta de Materias")
    nb.pack(); nb.config(height=200, width=600); nb.place(x=100, y=150)

    global pestaña_activa
    pestaña_activa = "Estudiantes"
    
    def cambiar_pestaña(event):
        global pestaña_activa
        tab_id = nb.index(nb.select())
        pestaña_activa = "Estudiantes" if tab_id == 0 else "Materias"
        actualizar_botones()
        
    nb.bind("<<NotebookTabChanged>>", cambiar_pestaña)

    frame = ttk.Frame(pe1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    frame_materias = ttk.Frame(pe2)
    frame_materias.pack(fill="both", expand=True, padx=10, pady=10)

    def actualizar_botones():
        if pestaña_activa == "Estudiantes":
            bt1e.place(x=250,y=500)
            bt2e.place(x=400,y=500)
            bt1m.place_forget()
            bt2m.place_forget()
        else:
            bt1e.place_forget()
            bt2e.place_forget()
            bt1m.place(x=250,y=500)
            bt2m.place(x=400,y=500)

    # Crear el Treeview con scrollbar
    columns = ("ID","Nombres", "Apellidos", "Edad", "Sexo", "Nacionalidad", "CI Estudiante", "Cédula Escolar",
               "Pasaporte", "Estatura", "Peso", "Talla de Zapatos", "Talla Camisas", "Talla Pantalon",
               "Enfermedad Cronica", "Observaciones", "Direccion", "Telefono Movil", "Email", "Año", "Repite")
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120 if col == "ID" else 200, stretch=tk.NO)

    # Scrollbar vertical
    scrollbar_vertical = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_vertical.set)
    scrollbar_vertical.pack(side="right", fill="y")

    # Scrollbar horizontal
    scrollbar_horizontal = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar_horizontal.set)
    tree.bind("<Double-1>", lambda e: dclick())
    scrollbar_horizontal.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # Llamar a la función consultar_estudiantes al abrir la ventana
    consultar_estudiantes()

    def comeback():
            Vc.destroy()
            if nivel == 1:
                from Ventanas.menu import M1
                M1(master, 1)
            if nivel == 2:
                from Ventanas.menu import M2
                M2(master, 2)
            if nivel == 3:
                from Ventanas.menu import M3
                M3(master, 3)

    Vc.protocol("WM_DELETE_WINDOW", comeback)

    def closd_w(pop):
        global ventana
        ventana = False
        pop.destroy()

    def filtrar_estudiantes():
        global ventana

        if not ventana:
            ventana = True
            pop = tk.Toplevel(Vc)
            pop.title("Filtrar")
            centrar_ventana(pop,400,500)
            pop.resizable(width=False,height=False)
            pop.iconbitmap(icopath)
            pop.wm_attributes("-topmost", 1)
            print("Entro")

            nb = ttk.Notebook(pop)
            pe1 = tk.Frame(nb); pe2 = tk.Frame(nb); pe3 = tk.Frame(nb)
            nb.add(pe1,text="Datos pag 1"); nb.add(pe2,text="Datos pag 2"); nb.add(pe3,text="Datos pag 3")
            nb.pack(fill=tk.BOTH, expand=1)
            style = ttk.Style() 
            style.configure("TNotebook.Tab", padding=[10, 5]) 
            style.map("TNotebook.Tab", foreground=[("selected", "green"), ("!selected", "black")])

            def m():
                if v1.get():
                    f1.pack(pady=2)
                else:
                    e1.delete(0,tk.END)
                    f1.pack_forget()
            def m2():
                if v2.get():
                    f2.pack(pady=2)
                else:
                    e2.delete(0,tk.END)
                    e3.delete(0,tk.END)
                    f2.pack_forget()
            def m3():
                if v3.get():
                    f3.pack(pady=2)
                else:
                    e4.delete(0,tk.END)
                    e5.delete(0,tk.END)
                    f3.pack_forget()
            def m4():
                if v4.get():
                    f4.pack(pady=2)
                else:
                    e6.delete(0,tk.END)
                    e7.delete(0,tk.END)
                    f4.pack_forget()
            def m5():
                if v5.get():
                    f5.pack(pady=2)
                else:
                    e8.delete(0,tk.END)
                    e9.delete(0,tk.END)
                    f5.pack_forget()
                    
            frame1 = tk.Frame(pe1); frame1.pack()
            v1 = tk.BooleanVar(); cb1 = tk.Checkbutton(frame1,text="Nombre",variable=v1,command=m).pack(pady=5)
            f1 = tk.Frame(frame1); f1.pack(pady=2)
            e1 = tk.Entry(f1); e1.pack()
            f1.pack_forget()

            frame2 = tk.Frame(pe1); frame2.pack()
            v2 = tk.BooleanVar(); cb2 = tk.Checkbutton(frame2,text="Edad Rango",variable=v2,command=m2).pack(pady=5)
            f2 = tk.Frame(frame2); f2.pack(pady=2)
            tk.Label(f2,text="Min/Max",font=("Cascadia Mono",8)).pack(pady=2)
            e2 = tk.Entry(f2,width=5); e2.pack(side=tk.LEFT,padx=2)
            e3 = tk.Entry(f2,width=5); e3.pack(side=tk.LEFT, padx=2)
            f2.pack_forget()

            frame3 = tk.Frame(pe1); frame3.pack()
            v3 = tk.BooleanVar(); cb3 = tk.Checkbutton(frame3,text="Talla de Zapatos Rango",variable=v3,command=m3).pack(pady=5)
            f3 = tk.Frame(frame3); f3.pack(pady=2)
            tk.Label(f3,text="Min/Max",font=("Cascadia Mono",8)).pack(pady=2)
            e4 = tk.Entry(f3,width=5); e4.pack(side=tk.LEFT,padx=2)
            e5 = tk.Entry(f3,width=5); e5.pack(side=tk.LEFT, padx=2)
            f3.pack_forget()

            frame4 = tk.Frame(pe1); frame4.pack()
            v4 = tk.BooleanVar(); cb4 = tk.Checkbutton(frame4,text="Talla de Camisas Rango",variable=v4,command=m4).pack(pady=5)
            f4 = tk.Frame(frame4); f4.pack(pady=2)
            tk.Label(f4,text="Min/Max",font=("Cascadia Mono",8)).pack(pady=2)
            e6 = tk.Entry(f4,width=5); e6.pack(side=tk.LEFT,padx=2)
            e7 = tk.Entry(f4,width=5); e7.pack(side=tk.LEFT, padx=2)
            f4.pack_forget()

            frame5 = tk.Frame(pe1); frame5.pack()
            v5 = tk.BooleanVar(); cb5 = tk.Checkbutton(frame5,text="Talla de Pantalon Rango",variable=v5,command=m5).pack(pady=5)
            f5 = tk.Frame(frame5); f5.pack(pady=2)
            tk.Label(f5,text="Min/Max",font=("Cascadia Mono",8)).pack(pady=2)
            e8 = tk.Entry(f5,width=5); e8.pack(side=tk.LEFT,padx=2)
            e9 = tk.Entry(f5,width=5); e9.pack(side=tk.LEFT, padx=2)
            f5.pack_forget()

            #pestaña 2

            def m6():
                if v6.get():
                    f6.pack(pady=2)
                else:
                    a1.set(False)
                    a2.set(False)
                    a3.set(False)
                    a4.set(False)
                    a5.set(False)
                    a6.set(False)
                    f6.pack_forget()

            frame6 = tk.Frame(pe2); frame6.pack()
            v6 = tk.BooleanVar(); cb6 = tk.Checkbutton(frame6,text="Años",variable=v6,command=m6).pack(pady=5)
            f6 = tk.Frame(frame6); f6.pack(pady=2)
            a1 = tk.BooleanVar();an1 = tk.Checkbutton(f6,text="1er Año",variable=a1).pack(pady=2)
            a2 = tk.BooleanVar();an2 = tk.Checkbutton(f6,text="2do Año",variable=a2).pack(pady=2)
            a3 = tk.BooleanVar();an3 = tk.Checkbutton(f6,text="3er Año",variable=a3).pack(pady=2)
            a4 = tk.BooleanVar();an4 = tk.Checkbutton(f6,text="4to Año",variable=a4).pack(pady=2)
            a5 = tk.BooleanVar();an5 = tk.Checkbutton(f6,text="5to Año",variable=a5).pack(pady=2)
            a6 = tk.BooleanVar();an6 = tk.Checkbutton(f6,text="6to Año",variable=a6).pack(pady=2)
            f6.pack_forget()

            #pestaña 3
            tk.Label(pe3,text="").pack(pady=4); tk.Label(pe3,text="Sexo",font=("Cascadia Mono",8)).pack(pady=4)
            comb1 = ttk.Combobox(pe3,values=("Masculino","Femenino"),state="readonly");comb1.set("");comb1.pack(pady=5)
            tk.Label(pe3,text="").pack(pady=4); tk.Label(pe3,text="Nacionalidad",font=("Cascadia Mono",8)).pack(pady=4)
            comb2 = ttk.Combobox(pe3,values=("Venezolana","Extranjera"),state="readonly");comb2.set("");comb2.pack(pady=5)

            #validacion
            def validacione():
                nombre = e1.get()
                edadmin = e2.get(); edadmax = e3.get()
                tzapmin = e4.get(); tzapmax = e5.get()
                tcammin = e6.get(); tcammax = e7.get()
                tpanmin = e8.get(); tpanmax = e9.get()

                # Validación nombre
                if v1.get() and not nombre:
                    messagebox.showerror("Error","Debe llenar el nombre si está seleccionado")
                    return False
                elif nombre and not nombre.replace(" ","").isalpha():
                    messagebox.showerror("Error","El nombre solo puede contener letras")
                    return False
                
                # Validación edad
                if v2.get():
                    if not edadmin or not edadmax:
                        messagebox.showerror("Error","Complete ambos campos de edad")
                        return False
                    if not edadmin.isdigit() or not edadmax.isdigit():
                        messagebox.showerror("Error","Edades deben ser números")
                        return False
                    if int(edadmin) > int(edadmax):
                        messagebox.showerror("Error","Edad mínima no puede ser mayor a máxima")
                        return False
                
                # Validación talla zapatos (v3)
                if v3.get():
                    if not tzapmin or not tzapmax:
                        messagebox.showerror("Error","Complete ambos campos de zapatos")
                        return False
                    if not tzapmin.isdigit() or not tzapmax.isdigit():
                        messagebox.showerror("Error","Tallas deben ser números")
                        return False
                    if int(tzapmin) > int(tzapmax):
                        messagebox.showerror("Error","Talla mínima no puede ser mayor a máxima")
                        return False
                
                # Validación talla camisas (v4) - INDEPENDIENTE de v3
                if v4.get():
                    if not tcammin or not tcammax:
                        messagebox.showerror("Error","Complete ambos campos de camisas")
                        return False
                    if not tcammin.isdigit() or not tcammax.isdigit():
                        messagebox.showerror("Error","Tallas deben ser números")
                        return False
                    if int(tcammin) > int(tcammax):
                        messagebox.showerror("Error","Talla mínima no puede ser mayor a máxima")
                        return False
                
                # Validación talla pantalones (v5) - INDEPENDIENTE de v3
                if v5.get():
                    if not tpanmin or not tpanmax:
                        messagebox.showerror("Error","Complete ambos campos de pantalón")
                        return False
                    if not tpanmin.isdigit() or not tpanmax.isdigit():
                        messagebox.showerror("Error","Tallas deben ser números")
                        return False
                    if int(tpanmin) > int(tpanmax):
                        messagebox.showerror("Error","Talla mínima no puede ser mayor a máxima")
                        return False
                
                # Validación años (v6) - INDEPENDIENTE
                if v6.get():
                    if not a1.get() and not a2.get() and not a3.get() and not a4.get() and not a5.get() and not a6.get():
                        messagebox.showerror("Error","Seleccione al menos un año")
                        return False

                return True  # Si pasa todas las validaciones

            def filtrar():
                global ventana
                
                # Validar antes de filtrar
                if not validacione():
                    return
                
                # Recopilar datos de los filtros
                nombre = e1.get().strip() if v1.get() else None
                edad_min = e2.get() if v2.get() else None
                edad_max = e3.get() if v2.get() else None
                tzap_min = e4.get() if v3.get() else None
                tzap_max = e5.get() if v3.get() else None
                tcam_min = e6.get() if v4.get() else None
                tcam_max = e7.get() if v4.get() else None
                tpan_min = e8.get() if v5.get() else None
                tpan_max = e9.get() if v5.get() else None
                años_seleccionados = []
                if v6.get():
                    if a1.get(): años_seleccionados.append("1er Año")
                    if a2.get(): años_seleccionados.append("2do Año")
                    if a3.get(): años_seleccionados.append("3er Año")
                    if a4.get(): años_seleccionados.append("4to Año")
                    if a5.get(): años_seleccionados.append("5to Año")
                    if a6.get(): años_seleccionados.append("6to Año")
                sexo = comb1.get() if comb1.get() else None
                nacionalidad = comb2.get() if comb2.get() else None

                # Construir la consulta SQL dinámica
                query = '''SELECT est.id, est.nombres, est.apellidos, est.edad, est.sexo, est.nacionalidad, 
                                est.ci_estudiante, est.cedula_escolar, est.Pasaporte, est.estatura, 
                                est.peso, est.talla_zapato, est.talla_camisa, est.talla_pantalon, 
                                est.enfermedad_cronica, est.observaciones, con.direccion, 
                                con.telefono_movil, con.email, ac.anio_a_cursar, ac.repite 
                        FROM estudiantes est
                        LEFT JOIN estudiantes_contactos ec ON est.id = ec.estudiante_id
                        LEFT JOIN contactos con ON ec.contacto_id = con.id
                        LEFT JOIN academicos ac ON est.id = ac.estudiante_id'''
                
                conditions = []
                params = []
                
                # Añadir condiciones según los filtros
                if nombre:
                    conditions.append("est.nombres LIKE ?")
                    params.append(f"%{nombre}%")
                
                if edad_min and edad_max:
                    conditions.append("est.edad BETWEEN ? AND ?")
                    params.extend([edad_min, edad_max])
                
                if tzap_min and tzap_max:
                    conditions.append("est.talla_zapato BETWEEN ? AND ?")
                    params.extend([tzap_min, tzap_max])
                
                if tcam_min and tcam_max:
                    conditions.append("est.talla_camisa BETWEEN ? AND ?")
                    params.extend([tcam_min, tcam_max])
                
                if tpan_min and tpan_max:
                    conditions.append("est.talla_pantalon BETWEEN ? AND ?")
                    params.extend([tpan_min, tpan_max])
                
                if años_seleccionados:
                    placeholders = ",".join(["?"] * len(años_seleccionados))
                    conditions.append(f"ac.anio_a_cursar IN ({placeholders})")
                    params.extend(años_seleccionados)
                
                if sexo:
                    conditions.append("est.sexo = ?")
                    params.append(sexo)
                
                if nacionalidad:
                    conditions.append("est.nacionalidad = ?")
                    params.append(nacionalidad)
                
                # Combinar todas las condiciones
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
                    for item in tree.get_children():
                        tree.delete(item)
                    
                    cur.execute(query, params)
                    estudiantes = cur.fetchall()
                    
                    if not estudiantes:
                        messagebox.showinfo("Información", "No se encontraron resultados con los filtros aplicados")
                    else:
                        for estudiante in estudiantes:
                            tree.insert("", "end", values=estudiante)
                            
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error en la base de datos:\n{str(e)}")
                finally:
                    cur.close()
                    co.close()
                
                ventana = False
                pop.destroy()

            pop.protocol("WM_DELETE_WINDOW", lambda: closd_w(pop))
            bt = tk.Button(pop, text="Filtrar",font=("Cascadia Mono",8),bg="light green",command=filtrar).pack(pady=5)

    bt1e = tk.Button(Vc, text="Filtrar Estudiantes", font=("Cascadia Mono",8),bg="light green", command= filtrar_estudiantes); bt1e.pack()
    bt1e.place(x=250,y=500)
        

    def ventana_modificar(estudiante):
        global vm

        if not vm:
            vm = True
            vvm = tk.Toplevel(Vc)
            vvm.title("Modificar Estudiante")
            centrar_ventana(vvm, 400, 500)
            vvm.resizable(0, 0)

            estudiante_id = estudiante["id"]

            tk.Label(vvm, text="Seleccione un campo para modificar", font=("Cascadia Mono", 8)).pack()
            frame_selector = tk.Frame(vvm)
            frame_selector.pack(pady=10)
            
            campos = ["Nombres", "Apellidos", "Edad", "Sexo", "Nacionalidad", "CI Estudiante",
                    "Cedula Escolar", "Pasaporte", "Estatura", "Peso", "Talla de Zapatos",
                    "Talla Camisas", "Talla Pantalon", "Enfermedad Cronica", "Observaciones",
                    "Direccion", "Telefono Movil", "Email"]

            combo_campos = ttk.Combobox(frame_selector, values=campos, state="readonly")
            combo_campos.pack()

            frame_input = tk.Frame(vvm)
            frame_input.pack(pady=20)

            # Entry widgets
            entry_text = tk.Entry(frame_input)
            entry_text.pack_forget()

            combo_options = ttk.Combobox(frame_input, state="readonly")
            combo_options.pack_forget()

            check_button_var = tk.BooleanVar()
            check_button = tk.Checkbutton(frame_input, variable=check_button_var, onvalue=True, offvalue=False)
            check_button.pack_forget()

            def mostrar_input(event):
                entry_text.pack_forget()
                combo_options.pack_forget()
                check_button.pack_forget()
                
                campo_seleccionado = combo_campos.get()
                if campo_seleccionado in ["Nombres", "Apellidos", "CI Estudiante", "Cedula Escolar", "Pasaporte",
                                        "Enfermedad Cronica", "Observaciones", "Direccion", "Telefono Movil", "Email"]:
                    entry_text.pack()
                    entry_text.delete(0, tk.END)
                    valor_actual = estudiante["datos"][columns.index(campo_seleccionado)] 
                    entry_text.insert(0, valor_actual)

                elif campo_seleccionado in ["Edad", "Estatura", "Peso", "Talla de Zapatos", "Talla Pantalon"]:
                    entry_text.pack()
                    entry_text.delete(0, tk.END)
                elif campo_seleccionado == "Sexo":
                    combo_options.config(values=["Masculino", "Femenino"])
                    combo_options.pack()
                    combo_options.set("")
                elif campo_seleccionado == "Nacionalidad":
                    combo_options.config(values=["Venezolana", "Extranjera"])
                    combo_options.pack()
                    combo_options.set("")
                elif campo_seleccionado == "Talla Camisas":
                    combo_options.config(values=["14", "16", "S", "M", "L", "XL"])
                    combo_options.pack()
                    combo_options.set("")
                elif campo_seleccionado == "Repite":
                    check_button.pack()
                    valor_actual = estudiante["datos"][columns.index("Repite")]
                    check_button_var.set(True if valor_actual == "SI" else False)

            combo_campos.bind("<<ComboboxSelected>>", mostrar_input)

            def guardar_cambios():
                global vm
                campo = combo_campos.get()
                nuevo_valor = None
                
                # Validaciones
                if campo in ["Nombres", "Apellidos"]:
                    if not re.match(r'^[A-Za-zÁ-ú\s]+$', entry_text.get()):
                        messagebox.showerror("Error", "Solo se permiten letras y espacios")
                        return
                
                # Asignar nuevo valor según el campo
                if campo == "Repite":
                    nuevo_valor = check_button_var.get()
                elif campo in ["Edad", "Estatura", "Peso"]:
                    try:
                        nuevo_valor = float(entry_text.get().replace(',', '.'))  # Permitir comas
                    except ValueError:
                        messagebox.showerror("Error", "Debe ser un número válido (ej: 1.75)")
                        return
                else:
                    nuevo_valor = entry_text.get() if campo not in ["Sexo", "Nacionalidad", "Talla Camisas"] else combo_options.get()
                
                actualizar_estudiante(estudiante_id, campo, nuevo_valor)
                vm = False
                vvm.destroy()

            def cerrar_ventana(ventana):
                global vm
                vm = False
                ventana.destroy()
        
            vvm.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(vvm))
            tk.Button(vvm, text="Guardar Cambios", command=guardar_cambios).pack()
        else:
            return
        
    def actualizar_estudiante(estudiante_id, campo, valor):
        dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        dirbasededatos = os.path.join(dirantbase, 'DB')
        pathdb = os.path.join(dirbasededatos, 'db')
        co = sqlite3.connect(pathdb)
        cur = co.cursor()

        try:
            # Determinar la tabla a actualizar
            tabla = "estudiantes"
            mapeo_columnas = {
                'Nombres': 'nombres',
                'Apellidos': 'apellidos',
                'Edad': 'edad',
                'Sexo': 'sexo',
                'Nacionalidad': 'nacionalidad',
                'CI Estudiante': 'ci_estudiante',
                'Cédula Escolar': 'cedula_escolar',
                'Pasaporte': 'Pasaporte',
                'Estatura': 'estatura',
                'Peso': 'peso',
                'Observaciones':'observaciones',
                'Direccion': 'direccion',
                'Talla de Zapatos': 'talla_zapato',
                'Talla Camisas': 'talla_camisa',
                'Talla Pantalon': 'talla_pantalon',
                'Direccion': 'direccion',
                'Telefono Movil': 'telefono_movil',
                'Email': 'email',
                # Agregar todos los demás campos necesarios
            }

            columna = mapeo_columnas.get(campo, campo.lower().replace(' ', '_'))
                        
            if campo in ["Direccion", "Telefono Movil", "Email"]:
                # Obtener el contacto_id asociado al estudiante
                cur.execute("SELECT contacto_id FROM estudiantes_contactos WHERE estudiante_id = ?", (estudiante_id,))
                contacto_id = cur.fetchone()
                if contacto_id:
                    contacto_id = contacto_id[0]
                    # Actualizar la tabla contactos
                    cur.execute(f"UPDATE contactos SET {columna} = ? WHERE id = ?", (valor, contacto_id))
            else:
                # Construir consulta dinámica
                query = f"UPDATE {tabla} SET {columna} = ? WHERE id = ?"
                cur.execute(query, (valor, estudiante_id))
            
            co.commit()
            consultar_estudiantes()  # Refrescar datos
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
        finally:
            cur.close()
            co.close()
            messagebox.showinfo("Exito","Datos Modificados con exito")

    def eliminar_estudiante(estudiante_id):
        # Definir el directorio y la base de datos
        dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        dirbasededatos = os.path.join(dirantbase, 'DB')
        pathdb = os.path.join(dirbasededatos, 'db')
        co = sqlite3.connect(pathdb)
        cur = co.cursor()

        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este estudiante?"):
            return

        try:
            # Obtener los IDs de los adultos relacionados con el estudiante
            cur.execute("SELECT adulto_id FROM estudiante_adultos WHERE estudiante_id = ?", (estudiante_id,))
            adultos_relacionados = cur.fetchall()

            # Eliminar los adultos relacionados
            for adulto_id in adultos_relacionados:
                cur.execute("DELETE FROM adultos WHERE id = ?", (adulto_id[0],))

            # Eliminar todas las relaciones del estudiante en la tabla estudiante_adultos
            cur.execute("DELETE FROM estudiante_adultos WHERE estudiante_id = ?", (estudiante_id,))

            # Eliminar todas las relaciones del estudiante en las diferentes tablas
            tablas_relaciones = [
                'estudiantes_contactos', 'academicos', 'estudiante_materias', 'notas', 'ajustes'
            ]

            for tabla in tablas_relaciones:
                cur.execute(f"DELETE FROM {tabla} WHERE estudiante_id = ?", (estudiante_id,))

            # Finalmente eliminar el estudiante
            cur.execute("DELETE FROM estudiantes WHERE id = ?", (estudiante_id,))

            # Confirmar los cambios en la base de datos
            co.commit()
            consultar_estudiantes()  # Refrescar datos
            messagebox.showinfo("Éxito", "Estudiante y adultos relacionados eliminados con éxito")

        except sqlite3.Error as e:
            # Revertir los cambios si hubo un error
            co.rollback()
            messagebox.showerror("Error", f"Error al eliminar estudiante: {str(e)}")

        finally:
            cur.close()
            co.close()


    def dclick():
        item = tree.selection()[0]
        valores = tree.item(item, 'values')
        estudiante_id = valores[0]  # ID ahora está en la primera columna
        
        if seleccion == "Modificar":
            ventana_modificar({"id": estudiante_id, "datos": valores})
        elif seleccion == "Eliminar":
            if messagebox.askyesno("Confirmar", "¿Eliminar este estudiante permanentemente?"):
                eliminar_estudiante(estudiante_id)

    def administrar():
        global ventana2

        if not ventana2:
            ventana2 = True
            vmo = tk.Toplevel(Vc)
            vmo.title("Seleccionar un modo")
            centrar_ventana(vmo,400,500)
            vmo.resizable(0,0)

             # Variables de modo
            vcb1 = tk.BooleanVar()
            vcb2 = tk.BooleanVar()
            vcb3 = tk.BooleanVar()

            def comprobar():
                global seleccion
                if seleccion == "Nada":
                    vcb1.set(True)
                    vcb2.set(False)
                    vcb3.set(False)
                elif seleccion == "Modificar":
                    vcb1.set(False)
                    vcb2.set(True)
                    vcb3.set(False)
                elif seleccion == "Eliminar":
                    vcb1.set(False)
                    vcb2.set(False)
                    vcb3.set(True)
                else:
                    vcb1.set(True)
                    seleccion = "Nada"

            def cambiar1():
                global seleccion
                seleccion = "Nada" if vcb1.get() else ""
                comprobar()

            def cambiar2():
                global seleccion
                seleccion = "Modificar" if vcb2.get() else ""
                comprobar()

            def cambiar3():
                global seleccion
                seleccion = "Eliminar" if vcb3.get() else ""
                comprobar()

            tk.Label(vmo, text=" ", font=("Cascadia Mono", 8)).pack()
            tk.Label(vmo, text="Seleccione un modo:", font=("Cascadia Mono", 8)).pack()

            c1 = tk.Checkbutton(vmo, text="Nada", variable=vcb1, command=cambiar1)
            c1.pack()

            tk.Label(vmo, text=" ", font=("Cascadia Mono", 8)).pack()

            c2 = tk.Checkbutton(vmo, text="Modificar", variable=vcb2, command=cambiar2)
            c2.pack()

            tk.Label(vmo, text=" ", font=("Cascadia Mono", 8)).pack()

            c3 = tk.Checkbutton(vmo, text="Eliminar", variable=vcb3, command=cambiar3)
            c3.pack()

            comprobar()
            vmo.protocol("WM_DELETE_WINDOW", lambda: cmo(vmo))
        else:
            return
        
    def cmo(ventana):
        global ventana2 
        ventana2 = False
        ventana.destroy()
    

    if nivel == 1:
        bt2e = tk.Button(Vc, text="Opciones de Administrador", font=("Cascadia Mono",8),bg="light green",command=administrar); bt2e.pack()
        bt2e.place(x=400,y=500)

    bt3 = tk.Button(Vc,text="Regresar",font=("Cascadia Mono",12), command=comeback); bt3.pack(); 
    bt3.place(x=150,y=500)

    #2da Pagina Consulta de Materias

    columns_materias = ("ID", "Nombre", "Abreviatura", "Año", "CI Docente", "Nombre Docente")
    tree_materias = ttk.Treeview(frame_materias, columns=columns_materias, show="headings")
    
    for col in columns_materias:
        tree_materias.heading(col, text=col)
        tree_materias.column(col, width=120 if col == "ID" else 200, stretch=tk.NO)
    
    scrollbar_materias = ttk.Scrollbar(frame_materias, orient="vertical", command=tree_materias.yview)
    tree_materias.configure(yscrollcommand=scrollbar_materias.set)
    scrollbar_materias.pack(side="right", fill="y")

    # Scrollbar horizontal
    scrollhmaterias = ttk.Scrollbar(frame_materias, orient="horizontal", command=tree_materias.xview)
    tree_materias.configure(xscrollcommand=scrollhmaterias.set)
    scrollhmaterias.pack(side="bottom", fill="x")
    tree_materias.pack(fill="both", expand=True)

    tree_materias.bind("<Double-1>", lambda e: dclick_materia())

    def dclick_materia():
        item = tree_materias.selection()[0]
        valores = tree_materias.item(item, 'values')
        materia_id = valores[0]
        
        if seleccion_materia == "Modificar":
            ventana_modificar_materia({"id": materia_id, "datos": valores})
        elif seleccion_materia == "Eliminar":
            if messagebox.askyesno("Confirmar", "¿Eliminar esta materia permanentemente?"):
                eliminar_materia(materia_id)

    def ventana_modificar_materia(materia):
        global ventana_materia

        if not ventana_materia:
            ventana_materia = True
            vvm = tk.Toplevel(Vc)
            vvm.title("Modificar Materia")
            centrar_ventana(vvm, 400, 400)
            vvm.resizable(0, 0)

            materia_id = materia["id"]
            campos_materias = ["Nombre", "Abreviatura", "CI Docente", "Nombre Docente"]

            tk.Label(vvm, text="Seleccione un campo para modificar", font=("Cascadia Mono", 8)).pack()
            frame_selector = tk.Frame(vvm)
            frame_selector.pack(pady=10)
            
            combo_campos = ttk.Combobox(frame_selector, values=campos_materias, state="readonly")
            combo_campos.set("Nombre")
            combo_campos.pack()

            frame_input = tk.Frame(vvm)
            frame_input.pack(pady=20)

            entry_text = tk.Entry(frame_input)
            entry_text.pack_forget()

            combo_anio = ttk.Combobox(frame_input, 
                                    values=["1er Año", "2do Año", "3er Año", 
                                        "4to Año", "5to Año", "6to Año"],
                                    state="readonly")
            combo_anio.pack_forget()

            def mostrar_input(event):
                entry_text.pack_forget()
                combo_anio.pack_forget()
                
                campo_seleccionado = combo_campos.get()
                valor_actual = materia["datos"][columns_materias.index(campo_seleccionado)]
                
                if campo_seleccionado == "Año":
                    combo_anio.pack()
                    combo_anio.set(valor_actual)
                else:
                    entry_text.pack()
                    entry_text.delete(0, tk.END)
                    entry_text.insert(0, valor_actual)

            combo_campos.bind("<<ComboboxSelected>>", mostrar_input)

            def guardar_cambios():
                global ventana_materia
                campo = combo_campos.get()
                nuevo_valor = entry_text.get() if campo != "Año" else combo_anio.get()
                
                # Validaciones
                if campo == "CI Docente" and not nuevo_valor.isdigit():
                    messagebox.showerror("Error", "El CI debe ser numérico")
                    return
                    
                actualizar_materia(materia_id, campo, nuevo_valor)
                messagebox.showinfo("Exito","Modificacion Efectuada Con Exito")
                ventana_materia = False
                vvm.destroy()
                consultar_materias()

            def cventanamodificacionm(ventana):
                global ventana_materia
                ventana_materia = False
                ventana.destroy()

            vvm.protocol("WM_DELETE_WINDOW", lambda: cventanamodificacionm(vvm))
            tk.Button(vvm, text="Guardar Cambios", command=guardar_cambios).pack()

    def actualizar_materia(materia_id, campo, valor):
        dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        dirbasededatos = os.path.join(dirantbase, 'DB')
        pathdb = os.path.join(dirbasededatos, 'db')
        
        columna = campo.lower().replace(' ', '_')
        if campo == "CI Docente": columna = "ci_docente"
        if campo == "Nombre Docente": columna = "n_docente"
        
        try:
            co = sqlite3.connect(pathdb)
            cur = co.cursor()
            cur.execute(f"UPDATE materias SET {columna} = ? WHERE id = ?", (valor, materia_id))
            co.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
        finally:
            cur.close()
            co.close()

    def eliminar_materia(materia_id):
        dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        dirbasededatos = os.path.join(dirantbase, 'DB')
        pathdb = os.path.join(dirbasededatos, 'db')
        
        try:
            co = sqlite3.connect(pathdb)
            cur = co.cursor()
            
            # Eliminar relaciones en tablas dependientes
            cur.execute("DELETE FROM estudiante_materias WHERE materia_id = ?", (materia_id,))
            cur.execute("DELETE FROM notas WHERE materia_id = ?", (materia_id,))
            cur.execute("DELETE FROM ajustes WHERE materia_id = ?", (materia_id,))
            
            # Eliminar la materia
            cur.execute("DELETE FROM materias WHERE id = ?", (materia_id,))
            
            co.commit()
            consultar_materias()
            messagebox.showinfo("Éxito", "Materia eliminada con éxito")
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
            co.rollback()
        finally:
            cur.close()
            co.close()
    

    def consultar_materias():
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
    
    consultar_materias()

    def filtrar_materias():
        global ventanamaterias

        if not ventanamaterias:
            ventanamaterias = True
            pop = tk.Toplevel(Vc)
            pop.title("Filtrar Materias")
            centrar_ventana(pop, 400, 400)
            pop.resizable(width=False, height=False)
            pop.iconbitmap(icopath)
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
        
    def administrar_materias():
        global ventana2

        if not ventana2:
            ventana2 = True
            vmo = tk.Toplevel(Vc)
            vmo.title("Seleccionar un modo")
            centrar_ventana(vmo, 400, 500)
            vmo.resizable(0,0)

            vcb1 = tk.BooleanVar()
            vcb2 = tk.BooleanVar()
            vcb3 = tk.BooleanVar()

            def comprobar():
                global seleccion_materia
                if seleccion_materia == "Nada":
                    vcb1.set(True)
                    vcb2.set(False)
                    vcb3.set(False)
                elif seleccion_materia == "Modificar":
                    vcb1.set(False)
                    vcb2.set(True)
                    vcb3.set(False)
                elif seleccion_materia == "Eliminar":
                    vcb1.set(False)
                    vcb2.set(False)
                    vcb3.set(True)
                else:
                    vcb1.set(True)
                    seleccion_materia = "Nada"

            def cambiar1():
                global seleccion_materia
                seleccion_materia = "Nada" if vcb1.get() else ""
                comprobar()

            def cambiar2():
                global seleccion_materia
                seleccion_materia = "Modificar" if vcb2.get() else ""
                comprobar()

            def cambiar3():
                global seleccion_materia
                seleccion_materia = "Eliminar" if vcb3.get() else ""
                comprobar()

            tk.Label(vmo, text=" ", font=("Cascadia Mono", 8)).pack()
            tk.Label(vmo, text="Seleccione un modo:", font=("Cascadia Mono", 8)).pack()

            c1 = tk.Checkbutton(vmo, text="Nada", variable=vcb1, command=cambiar1)
            c1.pack()

            tk.Label(vmo, text=" ", font=("Cascadia Mono", 8)).pack()

            c2 = tk.Checkbutton(vmo, text="Modificar", variable=vcb2, command=cambiar2)
            c2.pack()

            tk.Label(vmo, text=" ", font=("Cascadia Mono", 8)).pack()

            c3 = tk.Checkbutton(vmo, text="Eliminar", variable=vcb3, command=cambiar3)
            c3.pack()

            comprobar()

            vmo.protocol("WM_DELETE_WINDOW", lambda: cmo(vmo))

    bt1m = tk.Button(Vc, text="Filtrar Materias", font=("Cascadia Mono",8), bg="light green", command=filtrar_materias)
    if nivel == 1:
        bt2m = tk.Button(Vc, text="Opciones Admin Materias", font=("Cascadia Mono",8), bg="light green", command= administrar_materias)
    
    # Configurar posición inicial
    actualizar_botones()
    

    Vc.mainloop()