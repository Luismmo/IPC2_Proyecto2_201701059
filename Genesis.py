from tkinter import *
from tkinter import filedialog, ttk, font
from HorsePower import HorsePower
class Interfaz():
    def __init__(self):
        
        corcel = HorsePower()
        # Configuración de la raíz
        root = Tk()
        root.title("Proyecto 2 - IPC2")
        menubar = Menu(root)
        root.config(menu=menubar)

        cargarmenu = Menu(menubar, tearoff=0)
        cargarmenu.add_command(label="Seleccionar XML", command = lambda: corcel.abrirXML())
        #filemenu.add_command(label="Salir", command=root.quit)

        operacionesmenu = Menu(menubar, tearoff=0)
        operacionesmenu.add_command(label="Giro horizontal")
        operacionesmenu.add_command(label="Giro vertical")
        operacionesmenu.add_command(label="Transpuesta")

        reportemenu = Menu(menubar, tearoff = 0)
        reportemenu.add_command(label = "Desplegar HTML")

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Información del desarrollador")
        #helpmenu.add_separator()
        helpmenu.add_command(label="Documentación del programa")

        #lo que se muestra en el menú desplegable
        menubar.add_cascade(label="Cargar archivo", menu=cargarmenu)
        menubar.add_cascade(label="Operaciones", menu=operacionesmenu)
        menubar.add_cascade(label = "Reporte", menu = reportemenu)
        menubar.add_cascade(label="Ayuda", menu=helpmenu)

        # Finalmente bucle de la aplicación
        root.geometry('1000x590')
        root.resizable(False,False)
        root.mainloop()

ventana = Interfaz()