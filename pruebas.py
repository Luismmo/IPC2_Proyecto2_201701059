""" from tkinter import Tk, Label, Button
#from HorsePower import saludar
class VentanaEjemplo:
    def __init__(self, master):
        
        self.master = master
        master.title("Una simple interfaz gráfica")
        self.etiqueta = Label(master, text="Esta es la primera ventana!")
        self.etiqueta.pack()
        self.botonSaludo = Button(master, text="Saludar", command=self.saludar)
        self.botonSaludo.pack()
        self.botonCerrar = Button(master, text="Cerrar", command=master.quit)
        self.botonCerrar.pack()

    #def saludar(self):
     #   print('Hola')
    
root = Tk()
miVentana = VentanaEjemplo(root)
root.geometry('900x400')
root.resizable(width=False, height=False)
root.mainloop() """
from MatrizOrtogonal import *
from xml.dom import minidom
matriz = Matriz('prueba',4,7)
matriz.insertar('Luis',4,1)
matriz.insertar('Gio',3,2)
matriz.insertar('Armando',2,3)
matriz.insertar('Cesar',1,4)
matriz.insertar('Marvin',2,5)
matriz.insertar('Evelin',3,6)
matriz.insertar('Edwin',4,7)
matriz.recorrerFilas()
#matriz.recorrerColumnas()
#mixml = minidom.parse('entrada.xml')
#nombres = mixml.getElementsByTagName('matriz')
