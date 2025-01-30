import tkinter as tk
import os
import sqlite3
from tkinter import ttk, messagebox

ventana = False

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
            cur.execute('''SELECT est.nombres, est.apellidos, est.edad, est.sexo, est.nacionalidad, est.ci_estudiante, est.cedula_escolar,
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
    nb.pack(); nb.config(height=200, width=600); nb.place(x=100, y=150)

    frame = ttk.Frame(pe1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Crear el Treeview con scrollbar
    columns = ("Nombres", "Apellidos", "Edad", "Sexo", "Nacionalidad", "CI Estudiante", "Cédula Escolar",
               "Pasaporte", "Estatura", "Peso", "Talla de Zapatos", "Talla Camisas", "Talla Pantalon",
               "Enfermedad Cronica", "Observaciones", "Direccion", "Telefono Movil", "Email", "Año", "Repite")
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
            pop.title("Seleccionar Año")
            pop.geometry("400x500+500+300")
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
                query = '''SELECT est.nombres, est.apellidos, est.edad, est.sexo, est.nacionalidad, 
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

    if nivel == 1:
        bt2e = tk.Button(Vc, text="Opciones de Administrador", font=("Cascadia Mono",8),bg="light green"); bt2e.pack()
        bt2e.place(x=400,y=500)

    bt3 = tk.Button(Vc,text="Regresar",font=("Cascadia Mono",12), command=comeback); bt3.pack(); 
    bt3.place(x=150,y=500)

    

    Vc.mainloop()