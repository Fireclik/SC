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





    Vrm.mainloop()
Re2()