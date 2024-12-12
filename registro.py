import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import execconsulta

def registro():
    def btvalidacion():
        nombre = e1.get()
        apellido = e2.get()
        edad = e3.get()
        ano = m4.get()
        if not nombre or not apellido or not edad or ano not in ["1er año","2do año","3er año"]:
            messagebox.showwarning("Warning","Necesita llenar los campos")
            return False
        
        if ' ' in nombre or ' ' in apellido:
            messagebox.showerror("Error","El nombre y apellido no pueden tener espacios")
            return False 
        
        if not edad.isdigit() or len(edad) != 2:
            messagebox.showerror("Error","La edad es incompresible")
            return False 
        
        if ano not in ["1er año","2do año","3er año"]:
            messagebox.showerror("Error","Necesita seleccionar una opcion")
            return False
        
        return True
    def btclick():
        if not btvalidacion():
            return
        nombre = e1.get()
        apellido = e2.get()
        edad = int(e3.get())
        ano = m4.get()
        consulta = 'INSERT INTO estudiantes (nombre,apellido,edad,ano) VALUES (?,?,?,?)'
        execconsulta(consulta,(nombre,apellido,edad,ano))

        e1.delete(0,tk.END)
        e2.delete(0,tk.END)
        e3.delete(0,tk.END)
        m4.set("[seleccione una opcion]")

    w2 = tk.Tk()
    w2.geometry("800x600+500+50")
    w2.resizable(width=False,height=False)

    lb1 = tk.Label(w2,text="Nombre",font=("Comic Sans MS",12))
    lb1.pack()
    lb1.place(x=200,y=20)
    e1 = tk.Entry(w2)
    e1.pack()
    e1.place(x=200,y=50)

    lb2 = tk.Label(w2,text="Apellido",font=("Comic Sans MS",12))
    lb2.pack()
    lb2.place(x=200,y=120)
    e2 = tk.Entry(w2)
    e2.pack()
    e2.place(x=200,y=150)
    
    lb3 = tk.Label(w2,text="Edad",font=("Comic Sans MS",12))
    lb3.pack()
    lb3.place(x=198,y=220)
    e3 = tk.Entry(w2,width=5)
    e3.pack()
    e3.place(x=200,y=250)
    
    lb4 = tk.Label(w2,text="Año Cursante",font=("Comic Sans MS",12))
    lb4.pack()
    lb4.place(x=200,y=320)
    m4 = ttk.Combobox(w2,values=("[seleccione una opcion]","1er año","2do año","3er año"),width=24)
    m4.pack()
    m4.place(x=200,y=350)
    m4.set("[seleccione una opcion]")
    
    bt1 = tk.Button(w2,text="Registrar",bg="lightgray",font=("Comic Sans MS",12),command=btclick)
    bt1.pack()
    bt1.place(x=200,y=450)

    w2.mainloop()