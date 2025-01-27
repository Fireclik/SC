import tkinter as tk
import os
from tkinter import messagebox
from tkinter import ttk
import sqlite3

an1 = 0; an2 = 0; an3 = 0; an4 = 0; an5 = 0; an6 = 0;ventana = False

    

def Re2():
    global an1,an2,an3,an4,an5,an6
    Vrm = tk.Tk()
    Vrm.title("Registro de Materias")
    Vrm.geometry("800x600+400+50")
    Vrm.resizable(width=False,height=False)
    #importar icono
    icdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    icodir = os.path.join(icdir,'imag') 
    icopath = os.path.join(icodir,'Log.ico') 
    Vrm.iconbitmap(icopath)
    
    #importar imagen fondo
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..')); idir = os.path.join(dir,'imag') ; ipath = os.path.join(idir,'f1.png') 
    fv = tk.PhotoImage(file=ipath); tk.Label(Vrm,image=fv).place(x=0,y=0,relheight=1,relwidth=1)

    def valdedatos():
        nomm = e1.get()
        abre = e3.get()
        global an1,an2,an3,an4,an5,an6, sec
        nomd = e4.get()
        cid = e5.get()

        if not nomm and not abre and not nomd and not cid:
            messagebox.showwarning("Vacios","Los datos de la materia estan vacios necesita llenarlos")
            return False
        elif not nomm.strip():
            messagebox.showwarning("Nombre de la Materia","El nombre de la materia no puede estar vacio")
            return False
        elif not abre.strip():
            messagebox.showwarning("Abreviatura","La abreviatura no puede estar vacia")
            return False
        elif " " in abre:
            messagebox.showerror("Error","La abreviatura no puede tener espacios")
            return False
        elif not nomd.strip():
            messagebox.showwarning("Nombre","El nombre del docente no puede estar vacio")
            return False
        elif not nomd.replace(" ","").isalpha():
            messagebox.showerror("Error","El nombre del docente solo puede contener Letras")
            return False
        elif not cid:
            messagebox.showwarning("Cedula Docente","La cedula del docente es necesaria")
            return False
        elif not cid.isdigit():
            messagebox.showerror("Error","La cedula del docente tiene que tener solo digitos")
            return False
        elif an1==0 and an2==0 and an3==0 and an4==0 and an5==0 and an6 == 0:
            messagebox.showwarning("Año","Tiene que asignar un año al cual va dirigido la materia")
            return False
        
        return True
    
    def registrar_materia():
        #Datos de la materia
        nombre_materia = e1.get()
        abreviatura = e3.get()
        nombre_docente = e4.get()
        ci_docente = e5.get()
        global an1, an2, an3, an4, an5, an6
        dirantbase = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
        dirbasededatos = os.path.join(dirantbase,'DB')
        pathdb = os.path.join(dirbasededatos,'db')

        #conexion con la base de datos
        co = sqlite3.connect(pathdb)
        cur = co.cursor()
        try:
            años = ["1er Año", "2do Año", "3er Año", "4to Año", "5to Año", "6to Año"]
            anios_check = [an1, an2, an3, an4, an5, an6]

            for i, check in enumerate(anios_check):
                if check == 1:
                    anio = años[i]
                    cur.execute('''INSERT INTO materias (nombre, abreviatura, n_docente, ci_docente, anio) 
                                VALUES (?, ?, ?, ?, ?)''', (nombre_materia, abreviatura, nombre_docente, ci_docente, anio))
                    
                    materia_id = cur.lastrowid

                    # obtener estudiantes del año correspondiente
                    estudiantes = cur.execute('''SELECT id FROM estudiantes WHERE id IN 
                                                (SELECT estudiante_id FROM academicos WHERE anio_a_cursar = ?)''', (anio,)).fetchall()

                    for estudiante in estudiantes:
                        cur.execute('''INSERT INTO estudiante_materias (estudiante_id, materia_id, es_pendiente) 
                                    VALUES (?, ?, ?)''', (estudiante[0], materia_id, False))
                    
            co.commit()
            print("Materia registrada exitosamente.")
        except sqlite3.Error as e:
            print("Hubo un problema con la operacion en la base de datos: ",e)
            co.rollback()
        finally:
            cur.close()
            co.rollback()


    
    def popup():
        global an1, an2, an3, an4, an5, an6, ventana

        if not ventana:
            ventana = True
            pop = tk.Toplevel(Vrm)
            pop.title("Seleccionar Año")
            pop.geometry("200x300+500+300")
            pop.resizable(width=False,height=False)
            pop.iconbitmap(icopath)
            print("Entro")

            v1 = tk.BooleanVar(); cb1 = tk.Checkbutton(pop,text="1er Año",variable=v1).pack(pady=5)
            if an1 == 1:
                v1.set(True)
            v2 = tk.BooleanVar(); cb2 = tk.Checkbutton(pop,text="2do Año",variable=v2).pack(pady=5)
            if an2 == 1:
                v2.set(True)
            v3 = tk.BooleanVar(); cb3 = tk.Checkbutton(pop,text="3er Año",variable=v3).pack(pady=5)
            if an3 == 1:
                v3.set(True)
            v4 = tk.BooleanVar(); cb4 = tk.Checkbutton(pop,text="4to Año",variable=v4).pack(pady=5)
            if an4 == 1:
                v4.set(True)
            v5 = tk.BooleanVar(); cb5 = tk.Checkbutton(pop,text="5to Año",variable=v5).pack(pady=5)
            if an5 == 1:
                v5.set(True)
            v6 = tk.BooleanVar(); cb6 = tk.Checkbutton(pop,text="6to Año",variable=v6).pack(pady=5)
            if an6 == 1:
                v6.set(True)
            
            def selecpop():
                global an1,an2,an3,an4,an5,an6,sec,ventana

                if v1.get():
                    an1 = 1
                else:
                    an1 = 0

                if v2.get():
                    an2 = 1
                else:
                    an2 = 0

                if v3.get():
                    an3 = 1
                else:
                    an3 = 0

                if v4.get():
                    an4 = 1
                else:
                    an4 = 0

                if v5.get():
                    an5 = 1
                else:
                    an5 = 0

                if v6.get():
                    an6 = 1
                else:
                    an6 = 0
                
                ventana = False
                pop.destroy()
            
            pop.protocol("WM_DELETE_WINDOW", lambda: cerrar_popup(pop))
            bt = tk.Button(pop, text="Seleccionar",font=("Cascadia Mono",8),bg="light green",command=selecpop).pack(pady=5)
        else:
            print("NO")
            print(ventana)
            return
    def cerrar_popup(pop):
        global ventana
        ventana = False
        pop.destroy()
    
    def limpieza():
        global an1,an2,an3,an4,an5,an6
        e1.delete(0,tk.END);e3.delete(0,tk.END);e4.delete(0,tk.END);e5.delete(0,tk.END)
        an1 = 0; an2 = 0; an3 = 0; an4 = 0; an5 = 0; an6 = 0

    def btacc():
        if not valdedatos():
            return
        
        registrar_materia()
        limpieza()
        messagebox.showinfo("Exito","Datos ingresados Correctamente")

    #Creacion del notebook
    nb = ttk.Notebook(Vrm)
    pe1 = tk.Frame(nb)
    nb.add(pe1,text="Registro de Materias")
    nb.pack(); nb.config(height=300,width=600); nb.place(x=100,y=150)

    

    #creacion del canvas
    can = tk.Canvas(pe1); can.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

    f1 = tk.Frame(can); f2 = tk.Frame(can)

    #colocacion de los labels
    ttk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f1,text="Nombre de la Materia").pack(padx=4,pady=5)
    e1 = tk.Entry(f1,width=20); e1.pack(pady=5)
    ttk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f2,text="Abreviatura",).pack(padx=4,pady=5)
    e3 = tk.Entry(f2,width=7); e3.pack(pady=5)
    ttk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f1,text="Asignacion de la materia al año").pack(padx=4,pady=4)

    bt2 = tk.Button(f1,text="Asignar Año",font=("Cascadia Mono",8),bg="light blue",command=popup).pack(pady=5)

    ttk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f2,text="Nombre del docente asignado").pack(padx=4,pady=5)
    e4 = tk.Entry(f2,width=20); e4.pack(pady=5)
    ttk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f1,text="Ci del docente asignado").pack(padx=4,pady=5)
    e5 = tk.Entry(f1,width=20); e5.pack(pady=5)
    
    f1.pack(side=tk.LEFT,fill=tk.BOTH,expand=1);f2.pack(side=tk.RIGHT,fill=tk.BOTH,expand=1)

    bt = tk.Button(Vrm,text="Registrar",font=("Cascadia Mono",12),command=btacc); bt.pack(); bt.place(x=350,y=500)

    Vrm.mainloop()
Re2()