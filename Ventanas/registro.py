import tkinter as tk
import os
import re
from tkinter import ttk
from datetime import datetime
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
    def validar_fecha(fecha):
        try:
            datetime.strptime(fecha,"%d/%m/%Y")
            return True
        except ValueError:
            return False
    def validar_peso(pes):
        try:
            pes = float(pes)
            if pes < 5 or pes > 78:
                raise ValueError
            return True
        except ValueError:
            return False
    def validar_tallazapatos(tzap):
        try:
            tzap = int(tzap)
            if tzap < 35 or tzap > 45:
                raise ValueError
            return True
        except ValueError:
            return False
    def validar_tallaPantalon(tpan):
        try:
            tpan = int(tpan)
            if tpan < 24 or tpan > 38:
                raise ValueError
            return True
        except ValueError:
            return False
        
    def validar_estatura(est):
        try:
            est = float(est)
            if est < 0.60 or est > 1.99:
                raise ValueError
            return True
        except ValueError:
            return False

    def validar_telef(telfm):
        patron = r'^04(2|4|6|8|12)\d{7}$'
        if re.match(patron,telfm):
            return True
        else:
            return False

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
        fecha = f"{fdi}/{fme}/{fan}"
        pes = e5.get()
        pes = pes.replace(",",".")
        tcam = e6.get()
        tzap = e7.get()
        emil = e8.get()
        ape = e9.get()
        sex = cob1.get()
        ci = e10.get()
        lgna = e11.get()
        est = e12.get()
        est = est.replace(",",".")
        tpan = e13.get()
        direc = e14.get()
        telfm = e15.get()

        if not nom and not edad and not cies and not fdi and not fme and not fan and not pes and tcam == "[Seleccione]" and not tzap and not emil and not ape and sex == "[Seleccione una opcion]" and not ci and not lgna and not est and not tpan and not direc and not telfm:
            messagebox.showwarning("Advertencia","Campos vacios llenar los campos")
            return False
        elif not nom.strip():
            messagebox.showwarning("Nombre","El nombre no puede estar vacio")
            return False
        elif not nom.replace(" ","").isalpha():
            messagebox.showerror("Error","El nombre solo puede contener Letras")
            return False
        elif not edad:
            messagebox.showwarning("Edad","La edad del estudiante no puede estar vacia")
            return False
        elif not edad.isdigit() or len(edad) !=2:
            messagebox.showerror("Error","La edad es incomprensible")
            return False
        elif cies and not cies.isdigit():
            messagebox.showerror("Error","La Cedula escolar tiene que tener solo digitos")
            return False
        elif not validar_fecha(fecha):
            messagebox.showerror("Error","La Fecha de nacimiento es Invalida")
            return False
        elif not pes:
            messagebox.showwarning("Peso","El peso del Estudiante Es necesario")
            return False
        elif not validar_peso(pes):
            messagebox.showerror("Error","El peso es invalido")
            return False
        elif tcam == "[Seleccione]":
            messagebox.showwarning("Talla de Camisas","Tiene que seleccionar una Talla de Camisas")
            return False
        elif not tzap:
            messagebox.showwarning("Talla de Zapatos","La talla de zapatos es necesario")
            return False
        elif not tzap.isdigit():
            messagebox.showerror("Error","La Talla de zapatos tiene que ser solo digitos")
            return False
        elif not validar_tallazapatos(tzap):
            messagebox.showerror("Error","La Talla de zapatos esta fuera de rango")
            return False 
        elif emil and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',emil):
            messagebox.showerror("Error","Email Invalido")
            return False
        elif not ape.strip():
            messagebox.showwarning("Apellido","El Apellido no puede estar vacio")
            return False
        elif not ape.replace(" ","").isalpha():
            messagebox.showerror("Error","El Apellido solo puede contener Letras")
            return False
        elif sex == "[Seleccione una opcion]":
            messagebox.showwarning("Sexo","Tiene que definir el sexo del estudiante")
            return False
        elif not cies and not ci:
            messagebox.showwarning("Ci y ci Escolar","Tiene que colocar la cedula escolar o la cedula")
            return False
        elif ci and not ci.isdigit():
            messagebox.showerror("Error","La cedula Solo puede tener digitos")
            return False
        elif ci and cies:
            messagebox.showwarning("Ci y Ci Escolar","Solo puede colocar la cedula o la cedula escolar")
            return False
        elif not lgna:
            messagebox.showwarning("Lugar de Nacimiento","El Lugar de Nacimiento es Necesario")
            return False
        elif not est:
            messagebox.showwarning("Estatura","La estatura del estudiante es necesaria")
            return False
        elif not validar_estatura(est):
            messagebox.showerror("Estatura","La Estatura del estudiante es Invalida")
            return False
        elif not tpan:
            messagebox.showwarning("Talla de Pantalon","La talla de pantalon del estudiante es necesario")
            return False
        elif not validar_tallaPantalon(tpan):
            messagebox.showerror("Error","La talla de Pantalon ingresada es Invalida")
            return False
        elif not direc:
            messagebox.showwarning("Direccion","La direccion es un campo obligatorio")
            return False    
        elif telfm and not validar_telef(telfm):
            messagebox.showerror("Error","Numero de telefono Invalido")
            return False
        
        pes = float(pes)
        tzap = int(tzap)

        if ci and not cies:
            ci = int(ci)
            print(ci)
        else:
            cies = int(cies)
            print(cies)

        print(tzap)
        print(emil)
        print(telfm)
        return True

    def btacc():
        if not validacion_est():
            print("False")
            return
        else:
            messagebox.showinfo("Datos ingresados","Datos ingresados Correctamente")

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
    e6 = ttk.Combobox(f1,values=("[Seleccione]","14","16","S","M","L"),state="readonly"); e6.set("[Seleccione]") ;e6.pack(pady=4)
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
    cob1 = ttk.Combobox(f2,values=("[Seleccione una opcion]","Masculino","Femenino"),state="readonly"); cob1.set("[Seleccione una opcion]");cob1.pack(pady=5)
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