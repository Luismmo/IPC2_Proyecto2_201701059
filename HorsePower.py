from tkinter import *
from tkinter import filedialog
import os
from xml.dom import minidom
from ListaEnlazada import ListaEnlazada
from MatrizOrtogonal import *

class HorsePower():
    def __init__(self):
        self.matrices = ListaEnlazada()        
    
    def abrirXML(self):
        archivo = filedialog.askopenfilename(initialdir = "/", title = "Seleccione el archivo XML: ", filetypes = (("archivos XML", "*.xml"),("all files","*.*")))        
        mixml = minidom.parse(archivo)        
        nombres = mixml.getElementsByTagName('matriz')
        for matriz in nombres:            
            nombre = matriz.getElementsByTagName('nombre')[0]
            nom = nombre.firstChild.data
            fila = matriz.getElementsByTagName('filas')[0]
            fil = fila.firstChild.data
            columna = matriz.getElementsByTagName('columnas')[0]
            col = columna.firstChild.data            
            #creando nueva matriz ortogonal
            nuevaMatriz = Matriz(nom,fil,col)
            #insertando nodos
            datos = matriz.getElementsByTagName('imagen')[0]
            nodos = datos.firstChild.data
            division = nodos.split('\n')
            try:
                del division[0]
                del division[len(division)-1]
            except:
                print('Excepción controlada')
            
            for a in range(len(division)):
                filaNodo = list(division[a])
                columnaNodo = 1
                for b in range(len(filaNodo)):                    
                    if filaNodo[b] == '-' or filaNodo[b]=='*':                        
                        if filaNodo[b] == '*':
                            nuevaMatriz.insertar('*',(a+1),columnaNodo)
                        columnaNodo+=1

            
            self.matrices.insertar(nuevaMatriz)
        self.matrices.mostrarNodos()
        self.matrices.retornarEn(1).recorrerFilas()
            
