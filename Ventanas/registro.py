import tkinter as tk
import os
from tkinter import ttk
from tkinter import messagebox
from Db import execcons

def Re1():
    Vr = tk.Tk()
    Vr.title(string="Registro Estudiantes")
    Vr.geometry("800x600+350+50")
    Vr.resizable(width=False,height=False)
    #importar icono
    icdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    icodir = os.path.join(icdir,'imag') 
    icopath = os.path.join(icodir,'Log.ico') 
    Vr.iconbitmap(icopath)#colocar icono en la ventana
    #importar imagen fondo
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..')); idir = os.path.join(dir,'imag') ; ipath = os.path.join(idir,'f1.png') 
    fv = tk.PhotoImage(file=ipath); tk.Label(Vr,image=fv).place(x=0,y=0,relheight=1,relwidth=1)

    #creacion del notebook
    nb = ttk.Notebook(Vr); 
    pe1 = ttk.Frame(nb); pe2 = ttk.Frame(nb); pe3 = ttk.Frame(nb); pe4 = ttk.Frame(nb)#creacion de las pestañas
    nb.add(pe1,text="Datos del Estudiante"); nb.add(pe2,text="Datos del Padre"); nb.add(pe3,text="Datos de la Madre"); nb.add(pe4,text="Datos del Representante")#añadir a las pestañas en el notebook
    nb.pack(); nb.config(height=300,width=600); nb.place(x=100,y=150)

    #Creacion del Canvas
    cn = tk.Canvas(pe1); cn.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
    sc1 = tk.Scrollbar(pe1,orient=tk.VERTICAL,command=cn.yview); sc1.pack(side=tk.RIGHT,fill=tk.Y)#creacion del scrollbar
    cn.config(yscrollcommand=sc1.set)#configurar al canvas junto al scrollbar

    #creacion de los frames
    f1 = tk.Frame(cn); f2 = tk.Frame(cn)
    #asignacion de los frames al canvas
    cn.create_window((200,50),window=f1); cn.create_window((400,50),window=f2)

    #Validacion de Entradas y funciones especiales en los checkboxes
    def ecb_ob():
        if vcb1.get():
            fp.pack(pady=10)
        else:
            fp.pack_forget()
            e17.delete(0,tk.END)

    def validacion_est():
        nom = e1.get()
        edad = e2.get()
        cies = e3.get()
        fdi = e4_1.get()
        fme = e4_2.get()
        fan = e4_3.get()
        pes = e5.get()
        tcam = e6.get()
        tzap = e7.get()
        emil = e8.get()
        ape = e9.get()
        sex = cob1.get()
        ci = e10.get()
        lgna = e11.get()
        est = e12.get()
        tpan = e13.get()
        direc = e14.get()
        telfm = e15.get()

        if not nom and not edad and not cies and not fdi and not fme and not fan and not pes and not tcam and not tzap and not emil and not ape and sex == "[Seleccione una opcion]" and not ci and not lgna and not est and not tpan and not direc and not telfm:
            messagebox.showwarning("Advertencia","Campos vacios llenar los campos")
            return False
        elif not nom.strip():
            messagebox.showwarning("Nombre","El nombre no puede estar vacio")
            return False
        elif not nom.replace(" ","").isalpha():
            messagebox.showerror("Error","El nombre solo puede contener Letras")
            return False

        return True

    def btacc():
        if not validacion_est():
            print("False")
            return

    #frame 1 entradas y labels
    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f1,text="Nombre",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e1 = tk.Entry(f1,width=20); e1.pack(pady=5)
    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f1,text="Edad",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e2 = tk.Entry(f1,width=5); e2.pack(pady=5)
    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f1,text="Cedula Escolar",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e3 = tk.Entry(f1,width=20); e3.pack(pady=5)
    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f1,text="Fecha de Nacimiento",font=("Cascadia Mono",12)).pack(padx=4,pady=4)

    fd = ttk.Frame(f1); fd.pack(pady=5) 
    e4_1 = tk.Entry(fd, width=5); e4_1.pack(side=tk.LEFT, padx=2)
    e4_2 = tk.Entry(fd, width=5); e4_2.pack(side=tk.LEFT, padx=2)
    e4_3 = tk.Entry(fd, width=7); e4_3.pack(side=tk.LEFT, padx=2)

    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f1,text="Peso",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e5 = tk.Entry(f1,width=5); e5.pack(pady=5)
    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f1,text="Talla de Camisa",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e6 = tk.Entry(f1,width=5); e6.pack(pady=5)
    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f1,text="Talla de Zapatos",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e7 = tk.Entry(f1,width=5); e7.pack(pady=5)
    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f1,text="Email",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e8 = tk.Entry(f1,width=20); e8.pack(pady=5)
    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    vcb1 = tk.BooleanVar(); cb1 = tk.Checkbutton(f1,text="Observaciones",variable=vcb1,command=ecb_ob).pack(pady=8)
    fp = tk.Frame(f1); fp.pack(pady=10)
    e17 = tk.Entry(fp,width=20); e17.pack(pady=5)
    fp.pack_forget()

    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    #frame 2 entradas y labels
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f2,text="Apellidos",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e9 = tk.Entry(f2,width=20); e9.pack(pady=5)
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f2,text="Sexo",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    #combobox
    cob1 = ttk.Combobox(f2,values=("[Seleccione una opcion]","Masculino","Femenino")); cob1.set("[Seleccione una opcion]");cob1.pack(pady=5)
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f2,text="Cedula",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e10 = tk.Entry(f2,width=20);e10.pack(pady=5)
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f2,text="Lugar de Nacimiento",font=("Cascadia Mono",12)).pack(padx=4,pady=4) 
    e11 = tk.Entry(f2,width=20);e11.pack(pady=5)
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f2,text="Estatura",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e12 = tk.Entry(f2,width=20);e12.pack(pady=5)
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f2,text="Talla de Pantalon",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e13 = tk.Entry(f2,width=20);e13.pack(pady=5)
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f2,text="dirección",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e14 = tk.Entry(f2,width=20);e14.pack(pady=5)
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f2,text="Telefono Movil",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e15 = tk.Entry(f2,width=20);e15.pack(pady=5)
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5);vcb2 = tk.BooleanVar(); cb2 = tk.Checkbutton(f2,text="¿posee una enfermedad cronica?",variable=vcb2).pack(pady=8)
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)

    f1.bind("<Configure>", lambda e: cn.configure(scrollregion=cn.bbox("all")))
    f2.bind("<Configure>", lambda e: cn.configure(scrollregion=cn.bbox("all")))

    bt1 = tk.Button(Vr,text="Registrar",font=("Cascadia Mono",12),command=btacc); bt1.pack(); bt1.place(x=350,y=500)
    Vr.mainloop()

Re1()