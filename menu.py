import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database
import registro

def menu():
    w1 = tk.Tk()
    w1.geometry("640x480+500+50")
    w1.resizable(width=False,height=False)

    database.dbin()
    def btclick():
        w1.destroy()
        registro.registro()
    bt1 = tk.Button(w1,text="Registro",command=btclick)
    bt1.pack()
    #hola
    w1.mainloop()