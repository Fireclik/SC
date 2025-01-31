import tkinter as tk
import os
import sqlite3
from tkinter import ttk, messagebox

global modo_administracion, selected_student
modo_administracion = "nada"
selected_student = None

ventana = False; ventana2 = False

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
    pe1 = tk.Frame(nb); pe2 = tk.Frame(nb)
    nb.add(pe1, text="Consulta de Estudiantes"); nb.add(pe2, text="Consulta de Materias")
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
    tree.bind("<Double-1>", lambda e: manejar_doble_click())
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

    def validar_modificacion(campo, valor):
        # Validaciones comunes
        if campo in ["Nombres", "Apellidos"]:
            if not valor.strip():
                messagebox.showerror("Error", "El campo no puede estar vacío")
                return False
            if not valor.replace(" ", "").isalpha():
                messagebox.showerror("Error", "Solo se permiten letras")
                return False
        
        if campo == "Edad":
            if not valor.isdigit() or len(valor) != 2:
                messagebox.showerror("Error", "Edad inválida")
                return False
        
        if campo in ["Cédula Escolar", "CI Estudiante"]:
            if not valor.isdigit():
                messagebox.showerror("Error", "Solo se permiten dígitos")
                return False
        
        if campo == "Peso":
            try:
                float(valor.replace(",", "."))
            except:
                messagebox.showerror("Error", "Peso inválido")
                return False
        
        if campo == "Estatura":
            try:
                float(valor.replace(",", "."))
            except:
                messagebox.showerror("Error", "Estatura inválida")
                return False
        
        if campo == "Talla de Zapatos":
            if not valor.isdigit() or not (20 <= int(valor) <= 45):
                messagebox.showerror("Error", "Talla de zapatos inválida")
                return False
        
        # Validaciones específicas de documentos
        if campo in ["CI Estudiante", "Cédula Escolar", "Pasaporte"]:
            nacionalidad = selected_student[4]
            
            if campo == "Pasaporte" and nacionalidad == "Venezolana":
                messagebox.showerror("Error", "Venezolanos no pueden tener pasaporte")
                return False
            
            if campo in ["CI Estudiante", "Cédula Escolar"] and nacionalidad == "Extranjera":
                messagebox.showerror("Error", "Extranjeros deben usar pasaporte")
                return False
            
            # Verificar duplicados en la base de datos
            dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            dirbasededatos = os.path.join(dirantbase, 'DB')
            pathdb = os.path.join(dirbasededatos, 'db')
            
            try:
                co = sqlite3.connect(pathdb)
                cur = co.cursor()
                cur.execute(f"SELECT COUNT(*) FROM estudiantes WHERE {campo} = ?", (valor,))
                if cur.fetchone()[0] > 0:
                    messagebox.showerror("Error", "¡Este documento ya existe!")
                    return False
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
                return False
            finally:
                cur.close()
                co.close()
        return True

    def manejar_doble_click():
        global selected_student
        selected_student = None 
        
        # Verificar si hay algo seleccionado
        if not tree.selection():
            messagebox.showwarning("Advertencia", "Seleccione un estudiante primero")
            return
        
        try:
            item = tree.selection()[0]
            selected_student = tree.item(item)['values']
            
            if not selected_student:
                messagebox.showwarning("Advertencia", "No se pudo obtener los datos del estudiante")
                return
                
            if modo_administracion == "modificar":
                ventana_modificacion()
            elif modo_administracion == "eliminar":
                confirmar_eliminacion()
                
        except IndexError:
            messagebox.showerror("Error", "No se pudo obtener el registro seleccionado")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def ventana_modificacion():
        pop = tk.Toplevel(Vc)
        pop.title("Modificar Estudiante")
        centrar_ventana(pop, 400, 300)
        
        campos = ["Nombres", "Apellidos", "Edad", "Sexo", "Nacionalidad", 
                "CI Estudiante", "Cédula Escolar", "Pasaporte", "Estatura", 
                "Peso", "Talla de Zapatos", "Talla Camisas", "Talla Pantalon",
                "Enfermedad Cronica", "Observaciones", "Direccion", 
                "Telefono Movil", "Email", "Año", "Repite"]
        
        ttk.Label(pop, text="Seleccione el campo a modificar:", font=("Cascadia Mono", 9)).pack(pady=10)
        
        combo_campo = ttk.Combobox(pop, values=campos, state="readonly")
        combo_campo.pack(pady=5)
        
        frame_controles = tk.Frame(pop)
        frame_controles.pack(pady=10)
        
        entrada_valor = None
        combo_especial = None
        
        def actualizar_controles(event):
            nonlocal entrada_valor, combo_especial
            campo = combo_campo.get()
            valor_actual = selected_student[campos.index(campo)]
            
            # Limpiar frame
            for widget in frame_controles.winfo_children():
                widget.destroy()
            
            # Crear controles según el tipo de campo
            if campo in ["Sexo"]:
                combo_especial = ttk.Combobox(frame_controles, values=["Masculino", "Femenino"], state="readonly")
                combo_especial.set(valor_actual)
                combo_especial.pack()
            elif campo in ["Nacionalidad"]:
                combo_especial = ttk.Combobox(frame_controles, values=["Venezolana", "Extranjera"], state="readonly")
                combo_especial.set(valor_actual)
                combo_especial.pack()
            else:
                entrada_valor = tk.Entry(frame_controles, width=25)
                entrada_valor.insert(0, str(valor_actual))
                entrada_valor.pack()

        combo_campo.bind("<<ComboboxSelected>>", actualizar_controles)
    
        def guardar_cambios():
            # Verificar si la ventana todavía existe
            if not pop.winfo_exists():
                return
            
            try:
                # Obtener el campo seleccionado
                campo = combo_campo.get()
                if not campo:
                    messagebox.showerror("Error", "Seleccione un campo a modificar")
                    return
                
                # Obtener el valor nuevo
                nuevo_valor = ""
                if entrada_valor and entrada_valor.winfo_exists():
                    nuevo_valor = entrada_valor.get()
                elif combo_especial and combo_especial.winfo_exists():
                    nuevo_valor = combo_especial.get()
                else:
                    messagebox.showerror("Error", "No se pudo obtener el valor")
                    return
                
                # Validar y actualizar
                if not validar_modificacion(campo, nuevo_valor):
                    return
                    
                if actualizar_en_bd(campo, nuevo_valor):
                    consultar_estudiantes()
                    pop.destroy()
                    
            except Exception as e:
                messagebox.showerror("Error crítico", f"Error inesperado:\n{str(e)}")
        
        tk.Button(pop, text="Guardar Cambios", command=guardar_cambios, 
                font=("Cascadia Mono", 9), bg="lightgreen").pack(pady=10)

    def actualizar_en_bd(campo, valor):
        mapa_campos = {
            "Nombres": "nombres",
            "Apellidos": "apellidos",
            "Edad": "edad",
            "Sexo": "sexo",
            "Nacionalidad": "nacionalidad",
            "CI Estudiante": "ci_estudiante",
            "Cédula Escolar": "cedula_escolar",
            "Pasaporte": "Pasaporte",
            "Estatura": "estatura",
            "Peso": "peso",
            "Talla de Zapatos": "talla_zapato",
            "Talla Camisas": "talla_camisa",
            "Talla Pantalon": "talla_pantalon",
            "Enfermedad Cronica": "enfermedad_cronica",
            "Observaciones": "observaciones"
        }
        
        dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        dirbasededatos = os.path.join(dirantbase, 'DB')
        pathdb = os.path.join(dirbasededatos, 'db')
        
        try:
            co = sqlite3.connect(pathdb)
            cur = co.cursor()
            
            # Obtener el ID del estudiante CON VALIDACIÓN
            cur.execute("SELECT id FROM estudiantes WHERE ci_estudiante = ? OR cedula_escolar = ? OR Pasaporte = ?",
                    (selected_student[5], selected_student[6], selected_student[7]))  # Índices corregidos
            resultado = cur.fetchone()
            
            if not resultado:
                messagebox.showerror("Error", "No se encontró el estudiante en la base de datos")
                return False
                
            estudiante_id = resultado[0]
            # Actualizar el campo correspondiente
            if campo in mapa_campos:
                query = f"UPDATE estudiantes SET {mapa_campos[campo]} = ? WHERE id = ?"
                cur.execute(query, (valor, estudiante_id))
                
                # Si es un campo de contacto
                if campo in ["Direccion", "Telefono Movil", "Email"]:
                    query_contacto = f'''
                        UPDATE contactos SET {mapa_campos[campo]} = ? 
                        WHERE id = (
                            SELECT contacto_id FROM estudiantes_contactos 
                            WHERE estudiante_id = ?
                        )
                    '''
                    cur.execute(query_contacto, (valor, estudiante_id))
                
                # Si es un campo académico
                if campo in ["Año", "Repite"]:
                    query_academico = f'''
                        UPDATE academicos SET {mapa_campos[campo]} = ? 
                        WHERE estudiante_id = ?
                    '''
                    cur.execute(query_academico, (valor, estudiante_id))
                
                co.commit()
                messagebox.showinfo("Éxito", "Registro actualizado correctamente")
                return True
                
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en base de datos: {str(e)}")
            return False
        finally:
            cur.close()
            co.close()

    def eliminar_estudiante():
        dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        dirbasededatos = os.path.join(dirantbase, 'DB')
        pathdb = os.path.join(dirbasededatos, 'db')
        
        try:
            co = sqlite3.connect(pathdb)
            cur = co.cursor()
            
            # Obtener el ID con validación
            cur.execute("SELECT id FROM estudiantes WHERE ci_estudiante = ? OR cedula_escolar = ? OR Pasaporte = ?",
                    (selected_student[5], selected_student[6], selected_student[7]))  # Índices corregidos
            resultado = cur.fetchone()
            
            if not resultado:
                messagebox.showerror("Error", "Estudiante no encontrado en la base de datos")
                return
                
            estudiante_id = resultado[0]
            
            # Eliminar en cascada todas las relaciones
            tablas_relacionadas = [
                "estudiante_materias",
                "estudiante_adultos",
                "notas",
                "ajustes",
                "estudiantes_contactos",
                "academicos"
            ]
            
            for tabla in tablas_relacionadas:
                cur.execute(f"DELETE FROM {tabla} WHERE estudiante_id = ?", (estudiante_id,))
            
            # Finalmente eliminar al estudiante
            cur.execute("DELETE FROM estudiantes WHERE id = ?", (estudiante_id,))
            
            co.commit()
            messagebox.showinfo("Éxito", "Estudiante y todas sus relaciones eliminadas correctamente")
            consultar_estudiantes()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
        finally:
            cur.close()
            co.close()

    def confirmar_eliminacion():
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este estudiante?")
        if respuesta:
            eliminar_estudiante()

    #Definicion de opciones de administrador
    def administrar():
        global ventana2, modo_administracion
        
        def actualizar_modo():
            global modo_administracion
            modo_administracion = modo.get()
            messagebox.showinfo("Modo actual", f"Modo seleccionado: {modo_administracion.capitalize()}")
        
        if not ventana2:
            ventana2 = True
            pop = tk.Toplevel(Vc)
            pop.title("Opciones de Administrador")
            centrar_ventana(pop, 300, 200)
            pop.resizable(False, False)
            pop.iconbitmap(icopath)
            pop.wm_attributes("-topmost", 1)
            
            frame = tk.Frame(pop, padx=20, pady=20)
            frame.pack(expand=True, fill='both')
            
            tk.Label(frame, text="Seleccione el modo:", font=("Cascadia Mono", 10)).pack(pady=5)
            
            modo = tk.StringVar(value="nada")
            
            opciones = [
                ("Ninguna acción", "nada"),
                ("Modificar datos", "modificar"),
                ("Eliminar estudiantes", "eliminar")
            ]
            
            for texto, valor in opciones:
                tk.Radiobutton(frame, text=texto, variable=modo, value=valor, 
                            command=actualizar_modo, font=("Cascadia Mono", 9)).pack(anchor='w')
            
            def cerrar():
                global ventana2
                ventana2 = False
                pop.destroy()
            
            pop.protocol("WM_DELETE_WINDOW", cerrar)

    if nivel == 1:
        bt2e = tk.Button(Vc, text="Opciones de Administrador", font=("Cascadia Mono",8),bg="light green",command=administrar); bt2e.pack()
        bt2e.place(x=400,y=500)

    bt3 = tk.Button(Vc,text="Regresar",font=("Cascadia Mono",12), command=comeback); bt3.pack(); 
    bt3.place(x=150,y=500)

    

    Vc.mainloop()