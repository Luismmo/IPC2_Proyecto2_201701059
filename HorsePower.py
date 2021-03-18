from tkinter import *
from tkinter import filedialog
import os

class HorsePower():
    def __init__(self):
        listaXML = []
    
    def abrirXML(self):
        archivo = filedialog.askopenfilename(initialdir = "/", title = "Seleccione el archivo XML: ", filetypes = (("archivos XML", "*.xml"),("all files","*.*")))
        print('archivo abierto.')
    
