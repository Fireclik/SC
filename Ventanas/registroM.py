import tkinter as tk
import os
from tkinter import messagebox
from tkinter import ttk



def Re2():
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
        anio = cob.get()
        nomd = e4.get()
        cid = e5.get()

        if not nomm and not abre and anio == "[Seleccione una opcion]" and not nomd and not cid:
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
        elif anio == "[Seleccione una opcion]":
            messagebox.showwarning("Año","Tiene que asignar un año al cual va dirigido la materia")
            return False
        
        return True
        

    def btacc():
        if not valdedatos():
            return
        
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
    cob = ttk.Combobox(f1,values=("[Seleccione una opcion]","1er Año","2do Año","3er Año","4to Año","5to Año","6to Año"),state="readonly"); cob.set("[Seleccione una opcion]"); cob.pack(pady=5)
    ttk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f2,text="Nombre del docente asignado").pack(padx=4,pady=5)
    e4 = tk.Entry(f2,width=20); e4.pack(pady=5)
    ttk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f1,text="Ci del docente asignado").pack(padx=4,pady=5)
    e5 = tk.Entry(f1,width=20); e5.pack(pady=5)
    
    f1.pack(side=tk.LEFT,fill=tk.BOTH,expand=1);f2.pack(side=tk.RIGHT,fill=tk.BOTH,expand=1)

    bt = tk.Button(Vrm,text="Registrar",font=("Cascadia Mono",12),command=btacc); bt.pack(); bt.place(x=350,y=500)

    Vrm.mainloop()
Re2()