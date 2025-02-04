import tkinter as tk
import os
import sys
from Ventanas import Db

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

    ventana.wm_attributes("-topmost", 1)

#definicion de menu
def M1(master, nivel):
    Vm = tk.Toplevel(master)
    Vm.title("Menu")
    centrar_ventana(Vm, 800, 600)
    Vm.resizable(width=False,height=False)
    #importar icono
    def rutas1(ruta1):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta1)

    ruta1 = rutas1(r"Imag\Log.ico")
    ruta2 = rutas1(r"Imag\f1.png")
    
    Vm.iconbitmap(ruta1)
    #importar imagen fondo
     
    fv = tk.PhotoImage(file=ruta2); tk.Label(Vm,image=fv).place(x=0,y=0,relheight=1,relwidth=1)

    def boton():
        def btregistrar():
            def btregistarestu():
                Vm.destroy()
                from Ventanas.registro import Re1
                Re1(master, nivel)
            def btregistarmater():
                Vm.destroy()
                from Ventanas.registroM import Re2
                Re2(master, nivel)
            def btregistarnotas():
                Vm.destroy()
                from Ventanas.registroN import Rn1
                Rn1(master, nivel)
            def comeback():
                re_bt1.destroy()
                re_bt2.destroy()
                re_bt3.destroy()

                boton()
            
            re_bt1 = tk.Button(Vm,text="Registrar Estudiante",font=("Cascadia Mono",12),command=btregistarestu,width=20,height=1); re_bt1.pack()
            re_bt1.place(x=310,y=200)

            re_bt2 = tk.Button(Vm,text="Registrar Materias",font=("Cascadia Mono",12),command=btregistarmater,width=20,height=1); re_bt2.pack()
            re_bt2.place(x=310,y=300)

            re_bt3 = tk.Button(Vm,text="Registrar Notas",font=("Cascadia Mono",12),command=btregistarnotas,width=20,height=1); re_bt3.pack()
            re_bt3.place(x=310,y=400)

            re_bt3 = tk.Button(Vm,text="Atras",font=("Cascadia Mono",12),command=comeback,width=20,height=1); re_bt3.pack()
            re_bt3.place(x=310,y=500)

            rebt.destroy()
            logut.destroy()
            adbt.destroy()

        def loguto():
            Vm.destroy()
            master.deiconify()

        def administrar():
            rebt.destroy()
            logut.destroy()
            adbt.destroy()
            def btconsul():
                Vm.destroy()
                from Ventanas.consultaestu import Con1
                Con1(master, nivel)

            cbt = tk.Button(Vm,text="Consulta", font=("Cascadia Mono",12),command=btconsul,width=20,height=1); cbt.pack()
            cbt.place(x=310,y=200)


        rebt = tk.Button(Vm,text="Registro", font=("Cascadia Mono",12),command=btregistrar,width=20,height=1); rebt.pack()
        rebt.place(x=310,y=200)
        adbt = tk.Button(Vm,text="Administrar", font=("Cascadia Mono",12),width=20,height=1, command=administrar); adbt.pack()
        adbt.place(x=310,y=300)
        logut = tk.Button(Vm,text="Salir",font = ("Cascadia Mono",12),command=loguto,width=20,height=1); logut.pack()
        logut.place(x=310,y=400)

        Vm.protocol("WM_DELETE_WINDOW", loguto)
    boton()

    #ejecutar la base de datos
    Db.dbbin()
    Vm.mainloop()
def M2(master, nivel):
    Vm = tk.Toplevel(master)
    Vm.title("Menu")
    centrar_ventana(Vm, 800, 600)
    Vm.resizable(width=False,height=False)
    #importar icono
    def rutas1(ruta1):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta1)

    ruta1 = rutas1(r"Imag\Log.ico")
    ruta2 = rutas1(r"Imag\f1.png")
    
    Vm.iconbitmap(ruta1)
    #importar imagen fondo
     
    fv = tk.PhotoImage(file=ruta2); tk.Label(Vm,image=fv).place(x=0,y=0,relheight=1,relwidth=1)

    def boton():

        def loguto():
            Vm.destroy()
            master.deiconify()

        logut = tk.Button(Vm,text="Salir",font = ("Cascadia Mono",12),command=loguto,width=20,height=1); logut.pack()
        logut.place(x=310,y=400)

        Vm.protocol("WM_DELETE_WINDOW", loguto)
    boton()

    

    #ejecutar la base de datos
    Db.dbbin()

    Vm.mainloop()
def M3(master, nivel):
    Vm = tk.Toplevel(master)
    Vm.title("Menu")
    centrar_ventana(Vm, 800, 600)
    Vm.resizable(width=False,height=False)
    #importar icono
    def rutas1(ruta1):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta1)

    ruta1 = rutas1(r"Imag\Log.ico")
    ruta2 = rutas1(r"Imag\f1.png")
    
    Vm.iconbitmap(ruta1)
    #importar imagen fondo
     
    fv = tk.PhotoImage(file=ruta2); tk.Label(Vm,image=fv).place(x=0,y=0,relheight=1,relwidth=1)

    def boton():

        def loguto():
            Vm.destroy()
            master.deiconify()

        logut = tk.Button(Vm,text="Salir",font = ("Cascadia Mono",12),command=loguto,width=20,height=1); logut.pack()
        logut.place(x=310,y=400)

        Vm.protocol("WM_DELETE_WINDOW", loguto)
    boton()

    #ejecutar la base de datos
    Db.dbbin()

    Vm.mainloop()

