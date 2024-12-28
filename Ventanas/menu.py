import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Ventanas import Db

#definicion de menu
def M1():
    Vm = tk.Tk()
    Vm.title("Menu")
    Vm.config(bg="blue")
    Vm.geometry("640x480+500+50")
    Vm.resizable(width=False,height=False)
    Db.dbbin()

    Vm.mainloop()
def M2():
    Vm = tk.Tk()
    Vm.title("Menu")
    Vm.config(bg="green")
    Vm.geometry("640x480+500+50")
    Vm.resizable(width=False,height=False)
    Db.dbbin()

    Vm.mainloop()
def M3():
    Vm = tk.Tk()
    Vm.title("Menu")
    Vm.config(bg="yellow")
    Vm.geometry("640x480+500+50")
    Vm.resizable(width=False,height=False)
    Db.dbbin()

    Vm.mainloop()

