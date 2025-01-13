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
    pe1 = ttk.Frame(nb); pe2 = ttk.Frame(nb); pe3 = ttk.Frame(nb); pe4 = ttk.Frame(nb); pe5 = ttk.Frame(nb)#creacion de las pestañas
    nb.add(pe1,text="Datos del Estudiante"); nb.add(pe2,text="Datos Academicos"); nb.add(pe3,text="Datos de la Madre"); nb.add(pe4,text="Datos del Padre"); nb.add(pe5,text="Datos del Representante")#añadir a las pestañas en el notebook
    nb.pack(); nb.config(height=300,width=600); nb.place(x=100,y=150)

    #Pesataña 1
    #Creacion del Canvas
    cn = tk.Canvas(pe1); cn.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
    sc1 = tk.Scrollbar(pe1,orient=tk.VERTICAL,command=cn.yview); sc1.pack(side=tk.RIGHT,fill=tk.Y)#creacion del scrollbar
    cn.config(yscrollcommand=sc1.set)#configurar al canvas junto al scrollbar

    #creacion de los frames
    f1 = tk.Frame(cn); f2 = tk.Frame(cn)
    #asignacion de los frames al canvas
    cn.create_window((200,50),window=f1); cn.create_window((400,50),window=f2)

    def on_mousewheel3(event): 
        cn3.yview_scroll(int(-1*(event.delta/120)), "units")
    def on_mousewheel(event): 
        cn.yview_scroll(int(-1*(event.delta/120)), "units")
    def on_mousewheel4(event): 
        cn4.yview_scroll(int(-1*(event.delta/120)), "units")
    def on_mousewheel5(event): 
        cn5.yview_scroll(int(-1*(event.delta/120)), "units")

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
            if pes < 5:
                raise ValueError
            return True
        except ValueError:
            return False
    def validar_tallazapatos(tzap):
        try:
            tzap = int(tzap)
            if tzap < 10:
                raise ValueError
            return True
        except ValueError:
            return False
    def validar_tallaPantalon(tpan):
        try:
            tpan = int(tpan)
            if tpan < 5:
                raise ValueError
            return True
        except ValueError:
            return False
        
    def validar_estatura(est):
        try:
            est = float(est)
            if est < 0.30:
                raise ValueError
            return True
        except ValueError:
            return False

    def validar_telef(telfm):
        patron = r'^04(2|4|6|8|12|24|26|16)\d{7}$'
        if re.match(patron,telfm):
            return True
        else:
            return False

    def ecb_ob():
        if vcb1.get():
            fp.pack(pady=5)
        else:
            fp.pack_forget()
            e17.delete(0,tk.END)

    def ecb_ob2():
        if vcb2.get():
            fp2.pack(pady=10)
        else:
            fp2.pack_forget()
            e18.delete(0,tk.END)
            
    def ecb_ob3():
        if vcb6.get():
            fp3.pack(pady=10)
        else:
            fp3.pack_forget()
            e25.delete(0,tk.END)

    def ecb_ob4():
        if vcb11.get():
            fp4.pack(pady=10)
        else:
            fp4.pack_forget()
            e32.delete(0,tk.END)
    
    def combobox_nacionalidad(event):
        if e17_2.get() == "Venezolana":
            fp_2.pack_forget()
            e17_3.delete(0,tk.END)
        elif e17_2.get() == "Extranjera":
            fp_2.pack(pady=5)
            cb1.pack_forget()
            if vcb1.get():
                fp.pack_forget()
            cb1.pack(pady=4)
            ecb_ob()

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
        cursar = cob2.get()
        ci = e10.get()
        lgna = e11.get()
        est = e12.get()
        est = est.replace(",",".")
        tpan = e13.get()
        direc = e14.get()
        telfm = e15.get()
        enferm = e18.get()
        pasap = e17_3.get()

        if not nom and not edad and not cies and not fdi and not fme and not fan and not pes and tcam == "[Seleccione]" and not tzap and not emil and not ape and sex == "[Seleccione una opcion]" and not ci and not lgna and not est and not tpan and not direc and not telfm and cursar == "[Seleccione una opcion]":
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
        elif emil and ' ' in emil:
            messagebox.showerror("Error","Email No puede Tener Espacios")
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
        elif e17_2.get() == "Venezolana" and not cies and not ci:
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
        elif not enferm and vcb2.get():
            messagebox.showwarning("Enfermedad","El campo de enfermedad cronica marcado porfavor describirla")
            return False
        elif not e17.get() and vcb1.get():
            messagebox.showwarning("Observaciones","El Campo de Observaciones Seleccionado porfavor llenarlo")
            return False
        elif cursar == "[Seleccione una opcion]":
            messagebox.showwarning("Año a Cursar","Seleccione el año a cursar del estudiante")
            return False
        elif e17_2.get() == "Extranjera" and not pasap:
            messagebox.showwarning("Pasaporte","El Estudiante extranjero tiene que colocar su pasaporte")
            return False
        elif pasap and ci and cies or pasap and ci or pasap and cies or e17_2.get() == "Extranjera" and ci or e17_2.get() == "Extranjera" and cies or e17_2.get() == "Extranjera" and ci and cies:
            messagebox.showerror("Error","El estudiante extranjero tiene que tener unicamente su pasaporte la cedula o cedula escolar no se ingresan")
            return False

        pes = float(pes)
        tzap = int(tzap)

        return True
    
    def validacion_telefhabitacion(telfh):
        try:
            telfh = int(telfh)
            if telfh <= 0:
                raise ValueError
            return True
        except ValueError:
            return False
    
    def notienemadre():
        if vcb4.get():
            frame.pack_forget()
            e19.delete(0,tk.END)
            e20.delete(0,tk.END)
            e21.delete(0,tk.END)
            e22.delete(0,tk.END)
            e23.delete(0,tk.END)
            e24.delete(0,tk.END)
            e25.delete(0,tk.END)
            vcb5.set(False)
            vcb6.set(False)
            vcb7.set(False)
            ecb_ob3
        else:
            frame.pack(fill=tk.BOTH,expand=1)

    def tienemadre(madre):
        if vcb4.get():
            return madre
        else:
            madre = 1
            return madre
        
    def validacion_madre():
        nombreap = e19.get()
        ci = e20.get()
        dir = e21.get()
        telfm = e22.get()
        telfh = e23.get()
        emil = e24.get()
        telft = e25.get()

        if not nombreap and not ci and not dir:
            messagebox.showwarning("Madre","Campos de datos de la madre Vacios")
            return False
        elif not nombreap.strip():
            messagebox.showwarning("Nombre Madre","El nombre de la madre no puede estar vacio")
            return False
        elif not nombreap.replace(" ","").isalpha():
            messagebox.showerror("Error","El nombre de la madre solo puede contener Letras")
            return False
        elif not ci:
            messagebox.showwarning("Cedula Madre","La Cedula de la Madre es necesaria")
            return False
        elif not ci.isdigit():
            messagebox.showerror("Error","La Cedula tiene que tener solo digitos")
            return False
        elif not dir:
            messagebox.showwarning("Direccion","La direccion no puede estar vacia")
            return False
        elif telfm and not validar_telef(telfm):
            messagebox.showerror("Error","Telefono Movil Invalido")
            return False
        elif telfh and not validacion_telefhabitacion(telfh):
            messagebox.showerror("Error","Telefono de Habitacion Invalido")
            return False
        elif telft and not validacion_telefhabitacion(telft):
            messagebox.showerror("Error","Telefono de Trabajo Invalido")
            return False
        elif emil and ' ' in emil:
            messagebox.showerror("Error","Email No puede Tener espacios")
            return False
        elif not vcb7.get() and not vcb10.get() and not vcb12.get():
            messagebox.showwarning("Representante","Indique que familiar es el representante")
            return False

        return True

    def notienepadre():
        if vcb8.get():
            frame2.pack_forget()
            e26.delete(0,tk.END)
            e27.delete(0,tk.END)
            e28.delete(0,tk.END)
            e29.delete(0,tk.END)
            e30.delete(0,tk.END)
            e31.delete(0,tk.END)
            e32.delete(0,tk.END)
            vcb9.set(False)
            vcb10.set(False)
            vcb11.set(False)
            ecb_ob4()
        else:
            frame2.pack(fill=tk.BOTH,expand=1)
       
    def tienepadre(padre):
        if vcb8.get():
            return padre
        else:
            padre = 1
            return padre
        
    def validacion_padre():
        nombreap = e26.get()
        ci = e27.get()
        dir = e28.get()
        telfm = e29.get()
        telfh = e30.get()
        emil = e31.get()
        telft = e32.get()

        if not nombreap and not ci and not dir:
            messagebox.showwarning("Padre","Campos de datos del Padre Vacios")
            return False
        elif not nombreap.strip():
            messagebox.showwarning("Nombre Madre","El nombre del Padre no puede estar vacio")
            return False
        elif not nombreap.replace(" ","").isalpha():
            messagebox.showerror("Error","El nombre del Padre solo puede contener Letras")
            return False
        elif not ci:
            messagebox.showwarning("Cedula Padre","La Cedula del Padre es necesaria")
            return False
        elif not ci.isdigit():
            messagebox.showerror("Error","La Cedula tiene que tener solo digitos")
            return False
        elif not dir:
            messagebox.showwarning("Direccion","La direccion no puede estar vacia")
            return False
        elif telfm and not validar_telef(telfm):
            messagebox.showerror("Error","Telefono Movil Invalido")
            return False
        elif telfh and not validacion_telefhabitacion(telfh):
            messagebox.showerror("Error","Telefono de Habitacion Invalido")
            return False
        elif telft and not validacion_telefhabitacion(telft):
            messagebox.showerror("Error","Telefono de Trabajo Invalido")
            return False
        elif emil and ' ' in emil:
            messagebox.showerror("Error","Email No puede Tener Espacios")
            return False
        elif not vcb7.get() and not vcb10.get() and not vcb12.get():
            messagebox.showwarning("Representante","Indique que familiar es el representante")
            return False

        return True
    
    def representantetrabaja():
        if vcb14.get():
            fp5.pack(pady=10)
        else:
            fp5.pack_forget()
            e39.delete(0,tk.END)

    def esrepresentante1():
        if vcb7.get():
            vcb12.set(False)
            vcb10.set(False)
            esrepresentante3() 

    def esrepresentante2():
        if vcb10.get():
            vcb12.set(False)
            vcb7.set(False)
            esrepresentante3()         

    def esrepresentante3():
        if not vcb12.get():
            frame3.pack_forget()
            e33.delete(0,tk.END)
            e34.delete(0,tk.END)
            e35.delete(0,tk.END)
            e36.delete(0,tk.END)
            e37.delete(0,tk.END)
            e38.delete(0,tk.END)
            e39.delete(0,tk.END)
            e40.delete(0,tk.END)
            vcb13.set(False)
            vcb14.set(False)
        else:
            frame3.pack(fill=tk.BOTH,expand=1)
            vcb7.set(False)
            vcb10.set(False)

       
    def tienerepresentante(representante):
        if not vcb12.get():
            return representante
        else:
            representante = 1
            return representante
        
    def validacion_Representante():
        nombreap = e33.get()
        ci = e34.get()
        dir = e35.get()
        telfm = e36.get()
        telfh = e37.get()
        emil = e38.get()
        telft = e39.get()
        tiprepresent = e40.get()

        if not nombreap and not ci and not dir:
            messagebox.showwarning("Representante","Campos de datos del Representante Vacios")
            return False
        elif not nombreap.strip():
            messagebox.showwarning("Nombre Representante","El nombre del Representante no puede estar vacio")
            return False
        elif not nombreap.replace(" ","").isalpha():
            messagebox.showerror("Error","El nombre del Representante solo puede contener Letras")
            return False
        elif not ci:
            messagebox.showwarning("Cedula Padre","La Cedula del Representante es necesaria")
            return False
        elif not ci.isdigit():
            messagebox.showerror("Error","La Cedula tiene que tener solo digitos")
            return False
        elif not dir:
            messagebox.showwarning("Direccion","La direccion no puede estar vacia")
            return False
        elif telfm and not validar_telef(telfm):
            messagebox.showerror("Error","Telefono Movil Invalido")
            return False
        elif telfh and not validacion_telefhabitacion(telfh):
            messagebox.showerror("Error","Telefono de Habitacion Invalido")
            return False
        elif telft and not validacion_telefhabitacion(telft):
            messagebox.showerror("Error","Telefono de Trabajo Invalido")
            return False
        elif emil and ' ' in emil:
            messagebox.showerror("Error","Email No puede tener espacios")
            return False
        elif not tiprepresent.strip():
            messagebox.showwarning("Tipo de representante","El tipo de representante tiene que ser especificado,(Tio,Tia,Abuela,Abuelo,etc.)")
            return False
        elif not tiprepresent.replace(" ","").isalpha():
            messagebox.showerror("Error","El tipo de representante solo puede contener Letras")
            return False

        return True
        
    def btacc():
        madre = 0
        padre = 0
        representante = 0
        if not validacion_est():
            print("False Estudiante")
            return
        else:
            print("True Estudiante")

        if tienemadre(madre) == 1:
            if not validacion_madre():
                print("False Madre")
                return
            else:
                madre = 2

        if tienepadre(padre) == 1:
            if not validacion_padre():
                print("False padre")
                return
            else:
                padre = 2

        if tienerepresentante(representante) == 1:
            if not validacion_Representante():
                print ("False Representante")
                return
            else:
                representante = 2

        if padre == 0 and madre == 0 and representante == 0:
            messagebox.showerror("Error","El estudiante tiene que ser representado por alguien")
            return 
                
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
    
    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(f1,text="Nacionalidad",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e17_2 = ttk.Combobox(f1,values=("Venezolana","Extranjera"),state="readonly"); e17_2.set("Venezolana"); e17_2.bind("<<ComboboxSelected>>",combobox_nacionalidad);e17_2.pack(pady=4)
    fp_2 = tk.Frame(f1); fp_2.pack(pady=5)
    tk.Label(fp_2,text="Pasaporte",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    e17_3 = tk.Entry(fp_2,width=20); e17_3.pack(pady=5)
    tk.Label(fp_2,text=" ",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    fp_2.pack_forget()

    tk.Label(f1,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    vcb1 = tk.BooleanVar(); cb1 = tk.Checkbutton(f1,text="Observaciones",variable=vcb1,command=ecb_ob); cb1.pack(pady=4)
    fp = tk.Frame(f1); fp.pack(pady=5)
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
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    vcb2 = tk.BooleanVar(); cb2 = tk.Checkbutton(f2,text="¿posee una enfermedad cronica?",variable=vcb2,command=ecb_ob2).pack(pady=8)
    tk.Label(f2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    fp2 = tk.Frame(f2); fp2.pack(pady=5)
    e18 = tk.Entry(fp2,width=20); e18.pack(pady=5)
    fp2.pack_forget()

    f1.bind("<Configure>", lambda e: cn.configure(scrollregion=cn.bbox("all")))
    f2.bind("<Configure>", lambda e: cn.configure(scrollregion=cn.bbox("all")))

    cn.bind_all("<MouseWheel>", on_mousewheel)

    #Pestaña 2
    ttk.Label(pe2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); tk.Label(pe2,text="Año a cursar",font=("Cascadia Mono",12)).pack(padx=4,pady=4)
    cob2 = ttk.Combobox(pe2,values=("[Seleccione una opcion]","1er Año","2do Año","3er Año","4to Año","5to Año","6to Año"),state="readonly"); cob2.set("[Seleccione una opcion]");cob2.pack(pady=5)
    ttk.Label(pe2,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    vcb3 = tk.BooleanVar(); cb3 = tk.Checkbutton(pe2,text="¿Repite?",variable=vcb3).pack(pady=8)

    #pestaña 3

    ttk.Label(pe3,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    vcb4 = tk.BooleanVar(); cb4 = tk.Checkbutton(pe3,text="No tiene",variable=vcb4,command=notienemadre).pack(pady=8)

    #Creacion del Canvas
    frame = tk.Frame(pe3); frame.pack(fill=tk.BOTH,expand=1)

    cn3 = tk.Canvas(frame); cn3.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
    sc3 = tk.Scrollbar(frame,orient=tk.VERTICAL,command=cn3.yview); sc3.pack(side=tk.RIGHT,fill=tk.Y)#creacion del scrollbar
    cn3.config(yscrollcommand=sc3.set)#configurar al canvas junto al scrollbar

    #creacion de los frames
    f5 = tk.Frame(cn3); f6 = tk.Frame(cn3)
    #asignacion de los frames al canvas
    cn3.create_window((200,50),window=f5); cn3.create_window((400,50),window=f6)
    
    

    ttk.Label(f5,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f5,text="Nombre y Apellido de la Madre").pack(padx=4,pady=5)
    e19 = tk.Entry(f5,width=20); e19.pack(pady=5)
    ttk.Label(f6,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f6,text="Cedula de la Madre").pack(padx=4,pady=5)
    e20 = tk.Entry(f6,width= 20); e20.pack(pady=5)
    ttk.Label(f5,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f5,text="Direccion").pack(padx=4,pady=5)
    e21 = tk.Entry(f5, width=20); e21.pack(pady=5)
    ttk.Label(f6,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f6,text="Telefono Movil").pack(padx=4,pady=5)
    e22 = tk.Entry(f6,width=20); e22.pack(pady=5)
    ttk.Label(f5,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f5,text="Telefono de Habitacion").pack(padx=4,pady=5)
    e23 = tk.Entry(f5,width=20); e23.pack(pady=5)
    ttk.Label(f6,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f6,text="Email").pack(padx=4,pady=5)
    e24 = tk.Entry(f6,width=20); e24.pack(pady=5)
    ttk.Label(f5,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    vcb5 = tk.BooleanVar(); cb5 = tk.Checkbutton(f5,text="¿Vive con el Estudiante?",variable=vcb5).pack(padx=4,pady=5)
    vcb7 = tk.BooleanVar(); cb7 = tk.Checkbutton(f5,text="Es Representate",variable=vcb7,command=esrepresentante1).pack(padx=4,pady=5)
    vcb6 = tk.BooleanVar(); cb6 = tk.Checkbutton(f6,text="¿Trabaja?",variable=vcb6,command=ecb_ob3).pack(padx=4,pady=5)

    fp3 = tk.Frame(f6); fp3.pack(pady=5)
    ttk.Label(fp3,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(fp3,text="Telefono de Trabajo").pack(padx=4,pady=5)
    e25 = tk.Entry(fp3,width=20); e25.pack(pady=5)
    fp3.pack_forget()

    
    f5.bind("<Configure>", lambda e: cn3.configure(scrollregion=cn3.bbox("all")))
    f6.bind("<Configure>", lambda e: cn3.configure(scrollregion=cn3.bbox("all")))

    #Capacidad de utilizar la rueda del raton en el scrollbar
    cn3.bind_all("<MouseWheel>", on_mousewheel3)

    #pestaña 4

    ttk.Label(pe4,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    vcb8 = tk.BooleanVar(); cb8 = tk.Checkbutton(pe4,text="No tiene",variable=vcb8,command=notienepadre).pack(pady=8)

    #Creacion del Canvas
    frame2 = tk.Frame(pe4); frame2.pack(fill=tk.BOTH,expand=1)

    cn4 = tk.Canvas(frame2); cn4.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
    sc4 = tk.Scrollbar(frame2,orient=tk.VERTICAL,command=cn4.yview); sc4.pack(side=tk.RIGHT,fill=tk.Y)#creacion del scrollbar
    cn4.config(yscrollcommand=sc4.set)#configurar al canvas junto al scrollbar

    #creacion de los frames
    f7 = tk.Frame(cn4); f8 = tk.Frame(cn4)
    #asignacion de los frames al canvas
    cn4.create_window((200,50),window=f7); cn4.create_window((400,50),window=f8)
    
    

    ttk.Label(f7,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f7,text="Nombre y Apellido del Padre").pack(padx=4,pady=5)
    e26 = tk.Entry(f7,width=20); e26.pack(pady=5)
    ttk.Label(f8,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f8,text="Cedula del Padre").pack(padx=4,pady=5)
    e27 = tk.Entry(f8,width= 20); e27.pack(pady=5)
    ttk.Label(f7,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f7,text="Direccion").pack(padx=4,pady=5)
    e28 = tk.Entry(f7, width=20); e28.pack(pady=5)
    ttk.Label(f8,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f8,text="Telefono Movil").pack(padx=4,pady=5)
    e29 = tk.Entry(f8,width=20); e29.pack(pady=5)
    ttk.Label(f7,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f7,text="Telefono de Habitacion").pack(padx=4,pady=5)
    e30 = tk.Entry(f7,width=20); e30.pack(pady=5)
    ttk.Label(f8,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f8,text="Email").pack(padx=4,pady=5)
    e31 = tk.Entry(f8,width=20); e31.pack(pady=5)
    ttk.Label(f7,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    vcb9 = tk.BooleanVar(); cb9 = tk.Checkbutton(f7,text="¿Vive con el Estudiante?",variable=vcb9).pack(padx=4,pady=5)
    vcb10 = tk.BooleanVar(); cb10 = tk.Checkbutton(f7,text="Es Representate",variable=vcb10,command=esrepresentante2).pack(padx=4,pady=5)
    vcb11 = tk.BooleanVar(); cb11 = tk.Checkbutton(f8,text="¿Trabaja?",variable=vcb11,command=ecb_ob4).pack(padx=4,pady=5)

    fp4 = tk.Frame(f8); fp4.pack(pady=5)
    ttk.Label(fp4,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(fp4,text="Telefono de Trabajo").pack(padx=4,pady=5)
    e32 = tk.Entry(fp4,width=20); e32.pack(pady=5)
    fp4.pack_forget()

    
    f7.bind("<Configure>", lambda e: cn4.configure(scrollregion=cn4.bbox("all")))
    f8.bind("<Configure>", lambda e: cn4.configure(scrollregion=cn4.bbox("all")))

    cn4.bind_all("<MouseWheel>", on_mousewheel4)

    #pestaña 5

    ttk.Label(pe5,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    vcb12 = tk.BooleanVar(); cb12 = tk.Checkbutton(pe5,text="Otro Representante",variable=vcb12,command=esrepresentante3).pack(pady=8)

    #Creacion del Canvas
    frame3 = tk.Frame(pe5); frame3.pack(fill=tk.BOTH,expand=1)

    cn5 = tk.Canvas(frame3); cn5.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
    sc5 = tk.Scrollbar(frame3,orient=tk.VERTICAL,command=cn5.yview); sc5.pack(side=tk.RIGHT,fill=tk.Y)#creacion del scrollbar
    cn5.config(yscrollcommand=sc5.set)#configurar al canvas junto al scrollbar

    #creacion de los frames
    f9 = tk.Frame(cn5); f10 = tk.Frame(cn5)
    #asignacion de los frames al canvas
    cn5.create_window((200,50),window=f9); cn5.create_window((400,50),window=f10)
    
    

    ttk.Label(f9,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f9,text="Nombre y Apellido").pack(padx=4,pady=5)
    e33 = tk.Entry(f9,width=20); e33.pack(pady=5)
    ttk.Label(f10,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f10,text="Cedula").pack(padx=4,pady=5)
    e34 = tk.Entry(f10,width= 20); e34.pack(pady=5)
    ttk.Label(f9,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f9,text="Direccion").pack(padx=4,pady=5)
    e35 = tk.Entry(f9, width=20); e35.pack(pady=5)
    ttk.Label(f10,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f10,text="Telefono Movil").pack(padx=4,pady=5)
    e36 = tk.Entry(f10,width=20); e36.pack(pady=5)
    ttk.Label(f9,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f9,text="Telefono de Habitacion").pack(padx=4,pady=5)
    e37 = tk.Entry(f9,width=20); e37.pack(pady=5)
    ttk.Label(f10,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f10,text="Email").pack(padx=4,pady=5)
    e38 = tk.Entry(f10,width=20); e38.pack(pady=5)
    ttk.Label(f9,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)

    ttk.Label(f10,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(f10,text="Tipo de Representante").pack(padx=4,pady=5)
    e40 = tk.Entry(f10,width=20); e40.pack(pady=5)
    ttk.Label(f10,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5)
    vcb13 = tk.BooleanVar(); cb13 = tk.Checkbutton(f9,text="¿Vive con el Estudiante?",variable=vcb13).pack(padx=4,pady=5)
    vcb14 = tk.BooleanVar(); cb14 = tk.Checkbutton(f10,text="¿Trabaja?",variable=vcb14,command=representantetrabaja).pack(padx=4,pady=5)

    fp5 = tk.Frame(f10); fp5.pack(pady=5)
    ttk.Label(fp5,text=" ",font=("Cascadia Mono",8)).pack(padx=4,pady=5); ttk.Label(fp5,text="Telefono de Trabajo").pack(padx=4,pady=5)
    e39 = tk.Entry(fp5,width=20); e39.pack(pady=5)
    fp5.pack_forget()

    frame3.pack_forget()


    f9.bind("<Configure>", lambda e: cn5.configure(scrollregion=cn5.bbox("all")))
    f10.bind("<Configure>", lambda e: cn5.configure(scrollregion=cn5.bbox("all")))

    cn5.bind_all("<MouseWheel>", on_mousewheel5)
    
    bt1 = tk.Button(Vr,text="Registrar",font=("Cascadia Mono",12),command=btacc); bt1.pack(); bt1.place(x=350,y=500)
    Vr.mainloop()
    
Re1()