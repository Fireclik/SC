import os, sys
import shutil
import sqlite3
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

ventana = False


def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

    ventana.wm_attributes("-topmost", 1)

def main(master,nivel):

    def rutas1(ruta1):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta1)

    ruta1 = rutas1(r"Imag\Log.ico")

    root = tk.Toplevel(master)
    root.title("Finalizar Años")
    centrar_ventana(root,300,150)

    root.iconbitmap(ruta1)

    def cerrar_ano_escolar():
        respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de finalizar el año escolar?")
        if respuesta:
            try:
                # Ruta de la base de datos actual
                dir_actual = os.path.dirname(os.path.abspath(__file__))
                dir_db = os.path.join(os.path.abspath(os.path.join(dir_actual, '..')), 'DB')
                path_db = os.path.join(dir_db, 'db')

                if not os.path.exists(path_db):
                    messagebox.showerror("Error", "La base de datos actual no existe.")
                    return

                # Crear carpeta 'finalaños' si no existe
                dir_test1 = os.path.abspath(os.path.join(dir_actual, '..'))
                dir_finalanos = os.path.join(dir_test1, 'finalaños')
                if not os.path.exists(dir_finalanos):
                    os.makedirs(dir_finalanos)

                # Crear carpeta con fecha y hora
                ahora = datetime.now()
                fecha_hora_formateada = ahora.strftime('%d-%m-%Y-%H-%M')
                dir_fecha_hora = os.path.join(dir_finalanos, fecha_hora_formateada)
                os.makedirs(dir_fecha_hora)

                # Mover la base de datos
                shutil.move(path_db, dir_fecha_hora)

                messagebox.showinfo("Éxito", f"Año escolar finalizado. Base de datos movida a {dir_fecha_hora}")

            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def consultar_anos_anteriores():
        global ventana

        if not ventana:
            ventana = True
            # Ruta de la carpeta 'finalaños'
            dir_actual = os.path.dirname(os.path.abspath(__file__))
            dir_test1 = os.path.abspath(os.path.join(dir_actual, '..'))
            dir_finalanos = os.path.join(dir_test1, 'finalaños')

            if not os.path.exists(dir_finalanos):
                messagebox.showerror("Error", "No se encontraron años finalizados.")
                return

            # Obtener la lista de años finalizados
            anios_finalizados = [d for d in os.listdir(dir_finalanos) if os.path.isdir(os.path.join(dir_finalanos, d))]

            if not anios_finalizados:
                messagebox.showerror("Error", "No se encontraron años finalizados.")
                return

            # Crear una ventana para mostrar la lista
            ventana_lista = tk.Toplevel(root)
            ventana_lista.title("Años Finalizados")
            ventana_lista.geometry("400x300")

            lbl_instruccion = tk.Label(ventana_lista, text="Seleccione un año para generar el reporte:")
            lbl_instruccion.pack(pady=10)

            # Crear un Treeview para mostrar la lista
            tree = ttk.Treeview(ventana_lista)
            tree.pack(fill=tk.BOTH, expand=True)

            tree['columns'] = ('Año')
            tree.column('#0', width=0, stretch=tk.NO)
            tree.column('Año', anchor=tk.W, width=400)
            tree.heading('Año', text='Año', anchor=tk.CENTER)

            for anio in anios_finalizados:
                tree.insert('', tk.END, values=(anio,))

            def cefiltrarmaterias():
                global ventana
                ventana = False
                ventana_lista.destroy()
            
            ventana_lista.protocol("WM_DELETE_WINDOW",cefiltrarmaterias)

            # Función para manejar el doble clic
            def on_double_click(event):
                item = tree.selection()
                if item:
                    anio_seleccionado = tree.item(item, 'values')[0]
                    respuesta = messagebox.askyesno("Confirmación", f"¿Desea generar el reporte del año {anio_seleccionado}?")
                    if respuesta:
                        ventana_lista.destroy()
                        generar_reporte_anio(anio_seleccionado)

            tree.bind("<Double-1>", on_double_click)

    def generar_reporte_anio(anio_seleccionado):
        try:
            dir_actual = os.path.dirname(os.path.abspath(__file__))
            dir_test1 = os.path.abspath(os.path.join(dir_actual, '..'))
            dir_finalanos = os.path.join(dir_test1, 'finalaños')
            dir_anio = os.path.join(dir_finalanos, anio_seleccionado)

            # Ruta de la base de datos del año seleccionado
            path_db = os.path.join(dir_anio, 'db')

            if not os.path.exists(path_db):
                messagebox.showerror("Error", "No se encontró la base de datos en el año seleccionado.")
                return

            # Conectarse a la base de datos del año seleccionado
            co = sqlite3.connect(path_db)
            cur = co.cursor()

            # Obtener los datos de los estudiantes
            consulta_estudiantes = '''
            SELECT 
                e.id AS estudiante_id,
                e.nombres,
                e.apellidos,
                e.fecha_nacimiento,
                e.edad,
                e.sexo,
                e.lugar_nacimiento,
                e.nacionalidad,
                e.Pasaporte,
                e.ci_estudiante,
                e.cedula_escolar,
                e.estatura,
                e.peso,
                e.talla_zapato,
                e.talla_camisa,
                e.talla_pantalon,
                e.enfermedad_cronica,
                e.observaciones,
                a.anio_a_cursar,
                a.repite
            FROM estudiantes e
            LEFT JOIN academicos a ON e.id = a.estudiante_id
            ORDER BY a.anio_a_cursar, e.apellidos, e.nombres
            '''
            cur.execute(consulta_estudiantes)
            datos_estudiantes = cur.fetchall()

            # Obtener los datos de las materias
            consulta_materias = '''
            SELECT
                m.id,
                m.nombre,
                m.abreviatura,
                m.anio,
                m.ci_docente,
                m.n_docente
            FROM materias m
            ORDER BY m.anio, m.nombre
            '''
            cur.execute(consulta_materias)
            datos_materias = cur.fetchall()

            co.close()

            # Generar el reporte en Excel
            ruta_archivo = os.path.join(dir_anio, 'Reporte_Estudiantes_Materias.xlsx')
            
            with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
                # Datos de Estudiantes
                columnas_estudiantes = ['ID Estudiante', 'Nombres', 'Apellidos', 'Fecha de Nacimiento', 'Edad', 'Sexo',
                                        'Lugar de Nacimiento', 'Nacionalidad', 'Pasaporte', 'Cédula Estudiante',
                                        'Cédula Escolar', 'Estatura', 'Peso', 'Talla de Zapato', 'Talla de Camisa',
                                        'Talla de Pantalón', 'Enfermedad Crónica', 'Observaciones', 'Año a Cursar', 'Repite']

                df_estudiantes = pd.DataFrame(datos_estudiantes, columns=columnas_estudiantes)
                df_estudiantes.to_excel(writer, sheet_name='Estudiantes', index=False)

                # Datos de Materias
                columnas_materias = ['ID Materia', 'Nombre', 'Abreviatura', 'Año', 'CI Docente', 'Nombre Docente']
                df_materias = pd.DataFrame(datos_materias, columns=columnas_materias)
                df_materias.to_excel(writer, sheet_name='Materias', index=False)

            messagebox.showinfo("Éxito", f"Reporte generado exitosamente en: {ruta_archivo}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    btn_cerrar = tk.Button(root, text="Cerrar Año Escolar", command=cerrar_ano_escolar, width=25)
    btn_cerrar.pack(pady=10)

    btn_consultar = tk.Button(root, text="Consultar Años Anteriores", command=consultar_anos_anteriores, width=25)
    btn_consultar.pack(pady=10)

    def comeback():
        root.destroy()
        if nivel == 1:
            from Ventanas.menu import M1
            M1(master, 1)
        if nivel == 2:
            from Ventanas.menu import M2
            M2(master, 2)
        if nivel == 3:
            from Ventanas.menu import M3
            M3(master, 3)

    regresar = tk.Button(root, text="Regresar", command=comeback, width=25)
    regresar.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW",comeback)

    root.mainloop()

'''
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ººººººººººººººººººººººººººººººººººº Todas las marcas de Venta Reservados ººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ººººººººººººººººººººººººººººººººººSistema de gestion Academica Realizadoºººººººººººººººººººººººººººººººººººººººº
ººººººººººººººººººººººººººººººººººPor los estudiantes de 4to Semestre enºººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººº     Analisis y diseño de Sistemas    ºººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººº Alejandra Brito 30414509 04248613003 ºººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººº Edinson Lozano 31389068 04248487046  ºººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººº Victor Gonzalez 29985491 04161942133 ºººººººººººººººººººººººººººººººººººººººº
ººººººººººººººººººººººººººººººººº Leonardo Calojero 30729451 04121959745ºººººººººººººººººººººººººººººººººººººººº
ººººººººººººººººººººººººººººººººº Enmanuel Carreño 31177838 04128566093 ºººººººººººººººººººººººººººººººººººººººº
ººººººººººººººººººººººººººººººººº Kliver Rivas 30685024     04162917106 ºººººººººººººººººººººººººººººººººººººººº
ººººººººººººººººººººººººººººººººº Github: https://github.com/fireclik/sc ººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº
ºººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººººº

'''
    