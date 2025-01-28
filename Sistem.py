import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def Log1():
    Vl = tk.Tk()
    Vl.title(string="Login")
    centrar_ventana(Vl, 800, 600)
    Vl.resizable(width=False,height=False)

    #importar icono
    icdir = os.path.dirname(__file__)
    icodir = os.path.join(icdir,'imag')
    icopath = os.path.join(icodir,'Log.ico')

    Vl.iconbitmap(icopath)

    #importar imagen de fondo
    cdir = os.path.dirname(__file__) #obtener la direccion actual de sistem.py
    imgdir = os.path.join(cdir,'imag') #obtener la direccion de la carpeta o ruta completa
    imgpath = os.path.join(imgdir,'Lg1.png') #especificacion del archivo

    Fv = tk.PhotoImage(file=imgpath)#guardar la imagen en una variable funcional en modo tkinter
    lb1 = tk.Label(Vl,image=Fv).place(x=0,y=0,relheight=1,relwidth=1)#colocar la imagen en la ventana

    #variables de la entrada
    usuario = tk.StringVar()
    contrasena = tk.StringVar()

    #Entrada de datos
    e1 = tk.Entry(Vl,width=15,font=("Cascadia Mono",20),textvariable=usuario)
    e1.pack()
    e1.place(x=275,y=350)
    e2 = tk.Entry(Vl,width=15,font=("Cascadia Mono",20),show="*",textvariable=contrasena)
    e2.pack()
    e2.place(x=275,y=440)

    #boton funcion
    def log():
        us = usuario.get()
        con = contrasena.get()
        if us == "admins321" and con == "123sni":
            messagebox.showinfo("Correcto","Datos ingresados correctamente")
            e1.delete(0,tk.END)
            e2.delete(0,tk.END)
            Vl.withdraw()
            from Ventanas.menu import M1
            M1(Vl, 1)
        elif us == "subad22" and con == "22mm":
            messagebox.showinfo("Correcto","Datos ingresados correctamente")
            e1.delete(0,tk.END)
            e2.delete(0,tk.END)
            from Ventanas.menu import M2
            Vl.withdraw()
            M2(Vl, 2)
        elif us == "70eta" and con == "eta":
            messagebox.showinfo("Correcto","Datos ingresados correctamente")
            e1.delete(0,tk.END)
            e2.delete(0,tk.END)
            Vl.withdraw()
            from Ventanas.menu import M3
            M3(Vl, 3)
        else:
            messagebox.showerror("Error","Usuario o Contraseña incorrectos")

    #definicion de botones
    btl = tk.Button(Vl,text="Ingresar",font=("Cascadia Mono",12),height=1,width=15,bg="powder blue",command=log)
    btl.pack()
    btl.place(x=320,y=520)

    Vl.mainloop()
Log1()
    