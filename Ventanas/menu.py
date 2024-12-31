import tkinter as tk
import os
from tkinter import ttk
from tkinter import messagebox
from Ventanas import Db

#definicion de menu
def M1():
    Vm = tk.Tk()
    Vm.title("Menu")
    Vm.geometry("800x600+400+50")
    Vm.resizable(width=False,height=False)
    #importar icono
    icdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    icodir = os.path.join(icdir,'imag') 
    icopath = os.path.join(icodir,'Log.ico') 
    Vm.iconbitmap(icopath)
    #importar imagen fondo
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..')); idir = os.path.join(dir,'imag') ; ipath = os.path.join(idir,'f1.png') 
    fv = tk.PhotoImage(file=ipath); tk.Label(Vm,image=fv).place(x=0,y=0,relheight=1,relwidth=1)

    #ejecutar la base de datos
    Db.dbbin()

    Vm.mainloop()
def M2():
    Vm = tk.Tk()
    Vm.title("Menu")
    Vm.geometry("800x600+400+50")
    Vm.resizable(width=False,height=False)
    #importar icono
    icdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    icodir = os.path.join(icdir,'imag') 
    icopath = os.path.join(icodir,'Log.ico') 
    Vm.iconbitmap(icopath)
    #importar imagen fondo
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..')); idir = os.path.join(dir,'imag') ; ipath = os.path.join(idir,'f1.png') 
    fv = tk.PhotoImage(file=ipath); tk.Label(Vm,image=fv).place(x=0,y=0,relheight=1,relwidth=1)

    #ejecutar la base de datos
    Db.dbbin()

    Vm.mainloop()
def M3():
    Vm = tk.Tk()
    Vm.title("Menu")
    Vm.geometry("800x600+400+50")
    Vm.resizable(width=False,height=False)
    #importar icono
    icdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    icodir = os.path.join(icdir,'imag') 
    icopath = os.path.join(icodir,'Log.ico') 
    Vm.iconbitmap(icopath)
    #importar imagen fondo
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..')); idir = os.path.join(dir,'imag') ; ipath = os.path.join(idir,'f1.png') 
    fv = tk.PhotoImage(file=ipath); tk.Label(Vm,image=fv).place(x=0,y=0,relheight=1,relwidth=1)

    #ejecutar la base de datos
    Db.dbbin()

    Vm.mainloop()

