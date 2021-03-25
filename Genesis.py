import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk, font
import os
from xml.dom import minidom
from ListaEnlazada import ListaEnlazada
from MatrizOrtogonal import *

class Interfaz():
    def __init__(self):
        self.operacionSeleccionada = ''
        self.matrices = ListaEnlazada()            
        # Configuración de la raíz
        self.root = Tk()
        self.root.title("Proyecto 2 - IPC2")
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        self.cargarmenu = Menu(self.menubar, tearoff=0)
        self.cargarmenu.add_command(label="Seleccionar XML", command = lambda: self.abrirXML())        

        self.operacionesMatriz = Menu(self.menubar, tearoff=0)
        self.operacionesMatriz.add_command(label="Giro horizontal", command = lambda: self.botonApachado(1))
        self.operacionesMatriz.add_command(label="Giro vertical", command = lambda: self.botonApachado(2))
        self.operacionesMatriz.add_command(label="Transpuesta", command = lambda: self.botonApachado(3))
        self.operacionesMatriz.add_command(label="Limpiar zona", command = lambda: self.botonApachado(4))
        self.operacionesMatriz.add_command(label="Agregar linea horizontal", command = lambda: self.botonApachado(5))
        self.operacionesMatriz.add_command(label="Agregar linea vertical", command = lambda: self.botonApachado(6))
        self.operacionesMatriz.add_command(label="Agregar rectangulo", command = lambda: self.botonApachado(7))
        self.operacionesMatriz.add_command(label="Agregar triangulo rectangulo", command = lambda: self.botonApachado(8))
        self.operacionesMatriz.add_separator()        
        self.operacionesMatriz.add_command(label="Unión A, B")
        self.operacionesMatriz.add_command(label="Inersección A, B")
        self.operacionesMatriz.add_command(label="Diferencia A, B")
        self.operacionesMatriz.add_command(label="Diferencia simétrica A, B")

        self.reportemenu = Menu(self.menubar, tearoff = 0)
        self.reportemenu.add_command(label = "Desplegar HTML")

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Información del desarrollador")
        self.helpmenu.add_command(label="Documentación del programa")

        #lo que se muestra en el menú desplegable
        self.menubar.add_cascade(label="Cargar archivo", menu=self.cargarmenu)
        self.menubar.add_cascade(label="Operaciones", menu=self.operacionesMatriz)
        self.menubar.add_cascade(label ="Reporte", menu=self.reportemenu)
        self.menubar.add_cascade(label="Ayuda", menu=self.helpmenu)

        self.titulo = Label(self.root, text = 'Bienvenido, para empezar cargue un archivo XML')        
        self.titulo.grid(row =0, sticky = (N, S, E, W), columnspan = 3)
        self.titulo.config(font = ('Verdana', 18))
        #FRAME BOTONES
        self.panelBotones = Frame(self.root, borderwidth = 2, relief = 'raised')        

        #FRAME MATRIZ ORIGINAL NUMERO UNO
        self.panelOriginal = Frame(self.root, borderwidth = 2, relief = 'raised', bg="lightblue")             

        #FRAME MATRIZ ORIGINAL NUMERO DOS
        self.panelOriginal2 = Frame(self.root, borderwidth = 2, relief = 'raised', bg="lightblue")             

        #FRAME MATRIZ RESULTADO
        self.panelResultado = Frame(self.root, borderwidth = 2, relief = 'raised', bg="gold")        

        # Finalmente bucle de la aplicación
        #self.root.geometry('1100x590')
        #self.root.resizable(False,False)
        self.root.mainloop()
    
    def inicializarWidgets(self):
        self.limpiarBotones()
        #AGREGO LOS FRAMES        
        self.panelBotones.grid(columnspan = 2, row = 1, padx = 5,pady = 5, sticky = (N, S, E, W))        
        self.panelOriginal.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = (N, S, E, W))
        self.panelResultado.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = (N, S, E, W))
        #AGREGO LOS COMOPONENTES NECESARIOS
        self.indicador = Label(self.panelBotones, text = 'Seleccione una matriz')
        self.indicador.grid(padx = 5,row = 0, column = 0)
        listaMatrices = []
        for a in range(self.matrices.tamanio):
            listaMatrices.append(str(self.matrices.retornarEn(a+1).nombre))
        self.comboMatrices = ttk.Combobox(self.panelBotones, values = listaMatrices)
        self.comboMatrices.set(listaMatrices[0])
        self.comboMatrices.grid(padx = 5, row = 0, column = 1)
        self.imprimir = Button(self.panelBotones, text = 'Imprimir', command = lambda: self.Imprimir(), bg = 'salmon')
        self.imprimir.grid(padx=5, row = 0, column = 2)

    def widgetsLineas(self):
        self.labelFila = Label(self.panelBotones, text = 'En fila:')
        self.labelFila.grid(padx= 5, row = 0, column = 2)
        self.filaEntry = Entry(self.panelBotones, width = 2)
        self.filaEntry.grid(padx = 3, row =0, column =3 )
        self.labelColumna = Label(self.panelBotones, text = 'En columna:')
        self.labelColumna.grid(padx= 5, row = 0, column = 4)
        self.columnaEntry = Entry(self.panelBotones, width = 2)
        self.columnaEntry.grid(padx = 3, row =0, column =5 )
        self.labelCa = Label(self.panelBotones, text = 'Cantidad:')
        self.labelCa.grid(padx= 5, row = 0, column = 6)
        self.cantidadEntry = Entry(self.panelBotones, width = 2)
        self.cantidadEntry.grid(padx = 3, row =0, column =7 )
        self.imprimir = Button(self.panelBotones, text = 'Imprimir', command = lambda: self.Imprimir(), bg = 'salmon')
        self.imprimir.grid(padx=5, row = 0, column = 8)

    def inicializarWidgets2(self):
        self.limpiarBotones()
        #AGREGO LOS FRAMES        
        self.panelBotones.grid(columnspan = 3, row = 1, padx = 5,pady = 5, sticky = (N, S, E, W))        
        self.panelOriginal.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = (N, S, E, W))
        self.panelResultado.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = (N, S, E, W))
        #AGREGO LOS COMOPONENTES NECESARIOS        
        self.indicador = Label(self.panelBotones, text = 'Seleccione una matriz')
        self.indicador.grid(padx = 5,row = 0, column = 0)
        listaMatrices = []
        for a in range(self.matrices.tamanio):
            listaMatrices.append(str(self.matrices.retornarEn(a+1).nombre))
        self.comboMatrices = ttk.Combobox(self.panelBotones, values = listaMatrices)
        self.comboMatrices.set(listaMatrices[0])
        self.comboMatrices.grid(padx = 5, row = 0, column = 1)
        #WIDGETS VARIADOS
        if self.operacionSeleccionada == 'area':            
            self.coordenanda1 = Label(self.panelBotones, text = 'Coordenada inicial:')
            self.coordenanda1.grid(padx= 5, row = 0, column = 2)
            self.x1 = Entry(self.panelBotones, width = 2)
            self.x1.grid(padx = 3, row =0, column =3 )
            self.y1 = Entry(self.panelBotones, width = 2)
            self.y1.grid(padx = 5, row =0, column =4 )

            self.coordenanda2 = Label(self.panelBotones, text = 'Coordenada final:')
            self.coordenanda2.grid(padx= 5, row = 0, column = 5)
            self.x2 = Entry(self.panelBotones, width = 2)
            self.x2.grid(padx = 3, row =0, column =6 )
            self.y2 = Entry(self.panelBotones, width = 2)
            self.y2.grid(padx = 5, row =0, column =7 )            

            self.imprimir = Button(self.panelBotones, text = 'Imprimir', command = lambda: self.Imprimir(), bg = 'salmon')
            self.imprimir.grid(padx=5, row = 0, column = 8)
        if self.operacionSeleccionada == 'lineah':
            self.widgetsLineas()
        if self.operacionSeleccionada == 'lineav':
            self.widgetsLineas()
        if self.operacionSeleccionada == 'addrectangulo':
            self.coordenanda1 = Label(self.panelBotones, text = 'Coordenada inicial:')
            self.coordenanda1.grid(padx= 5, row = 0, column = 2)
            self.x1 = Entry(self.panelBotones, width = 2)
            self.x1.grid(padx = 3, row =0, column =3 )
            self.y1 = Entry(self.panelBotones, width = 2)
            self.y1.grid(padx = 5, row =0, column =4 )
            self.labelalto = Label(self.panelBotones, text = 'Alto:')
            self.labelalto.grid(padx= 5, row = 0, column = 5)
            self.altroentry = Entry(self.panelBotones, width = 2)
            self.altroentry.grid(padx = 3, row =0, column =6 )
            self.labelancho = Label(self.panelBotones, text = 'Ancho:')
            self.labelancho.grid(padx= 5, row = 0, column = 7)
            self.anchoentry = Entry(self.panelBotones, width = 2)
            self.anchoentry.grid(padx = 3, row =0, column =8 )
            self.imprimir = Button(self.panelBotones, text = 'Imprimir', command = lambda: self.Imprimir(), bg = 'salmon')
            self.imprimir.grid(padx=5, row = 0, column = 9)
        if self.operacionSeleccionada == 'addtriangulo':
            self.coordenanda1 = Label(self.panelBotones, text = 'Coordenada inicial:')
            self.coordenanda1.grid(padx= 5, row = 0, column = 2)
            self.x1 = Entry(self.panelBotones, width = 2)
            self.x1.grid(padx = 3, row =0, column =3 )
            self.y1 = Entry(self.panelBotones, width = 2)
            self.y1.grid(padx = 5, row =0, column =4 )
            self.filascolumnas = Label(self.panelBotones, text = 'Filas x Columnas:')
            self.filascolumnas.grid(padx= 5, row = 0, column = 5)
            self.dantoentry = Entry(self.panelBotones, width = 2)
            self.dantoentry.grid(padx = 3, row =0, column =6 )
            self.imprimir = Button(self.panelBotones, text = 'Imprimir', command = lambda: self.Imprimir(), bg = 'salmon')
            self.imprimir.grid(padx=5, row = 0, column = 7)



    def botonApachado(self, valor):
        if valor == 1:
            self.limpiarFramesMatrices()
            self.titulo.configure(text = 'Giro horizontal de una imagen',)            
            self.inicializarWidgets()
            self.operacionSeleccionada = 'horizontal'
        if valor == 2:
            self.limpiarFramesMatrices()
            self.titulo.configure(text = 'Giro vertical de una imagen')
            self.inicializarWidgets()
            self.operacionSeleccionada = 'vertical'
        if valor == 3:
            self.limpiarFramesMatrices()
            self.titulo.configure(text = 'Transpuesta de una imagen')
            self.inicializarWidgets()
            self.operacionSeleccionada = 'transpuesta'
        if valor == 4:
            self.limpiarFramesMatrices()
            self.titulo.configure(text = 'Limpiar zona de una imagen')
            self.operacionSeleccionada = 'area'
            self.inicializarWidgets2()
        if valor == 5:
            self.limpiarFramesMatrices()
            self.titulo.configure(text = 'Linea horizontal en una imagen')
            self.operacionSeleccionada = 'lineah'
            self.inicializarWidgets2()
        if valor == 6:
            self.limpiarFramesMatrices()
            self.titulo.configure(text = 'Linea vertical en una imagen')
            self.operacionSeleccionada = 'lineav'
            self.inicializarWidgets2()
        if valor == 7:
            self.limpiarBotones()
            self.titulo.configure(text= 'Agregar rectangulo a una imagen')
            self.operacionSeleccionada = 'addrectangulo'
            self.inicializarWidgets2()
        if valor == 8:            
            self.limpiarBotones()
            self.titulo.configure(text= 'Agregar triangulo rectangulo')
            self.operacionSeleccionada = 'addtriangulo'
            self.inicializarWidgets2()
            
            
    
    def Imprimir(self):
        if self.operacionSeleccionada =='horizontal':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            self.giroHorizontal(namematriz)
        if self.operacionSeleccionada == 'vertical':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            self.giroVertical(namematriz)
        if self.operacionSeleccionada == 'transpuesta':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            self.Transpuesta(namematriz)
        if self.operacionSeleccionada == 'area':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            self.LimpiarZona(namematriz,int(self.x1.get()), int(self.y1.get()),int(self.x2.get()), int(self.y2.get()))


    def matrizSeleccionada(self, nombre):
        for a in range(self.matrices.tamanio):
            if nombre == self.matrices.retornarEn(a+1).nombre:
                return self.matrices.retornarEn(a+1)            

    def giroHorizontal(self, nombre):        
        matrix = self.matrizSeleccionada(nombre)
        x = int(matrix.filas)
        y = int(matrix.columnas)
        #IMPRESIÓN
        for a in range(x):
            for b in range(y):
                #IMPRESIÓN NORMAL
                celda = Entry(self.panelOriginal, width = 3)
                celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if matrix.retornarNodoEn(a+1, b+1) != None:
                    celda.insert(0,'*')
                    celda.configure({'background': "#454545"})
                    celda.config(justify = 'center', fg = 'white')
                #IMPRESIÓN GIRADA        
                nuevacelda = Entry(self.panelResultado, width = 3)    
                nuevacelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)                
                if matrix.retornarNodoEn(x-a, b+1) != None:
                    nuevacelda.insert(0,'*')
                    nuevacelda.configure({'background': "#454545"})
                    nuevacelda.config(justify = 'center', fg = 'white')        
    
    def giroVertical(self, nombre):        
        matrix = self.matrizSeleccionada(nombre)
        x = int(matrix.filas)
        y = int(matrix.columnas)
        #IMPRESIÓN
        for a in range(x):
            for b in range(y):
                #IMPRESIÓN NORMAL
                celda = Entry(self.panelOriginal, width = 3)
                celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if matrix.retornarNodoEn(a+1, b+1) != None:
                    celda.insert(0,'*')
                    celda.configure({'background': "#454545"})
                    celda.config(justify = 'center', fg = 'white')
                #IMPRESIÓN GIRADA        
                nuevacelda = Entry(self.panelResultado, width = 3)    
                nuevacelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)                
                if matrix.retornarNodoEn(a+1, y-b) != None:
                    nuevacelda.insert(0,'*')
                    nuevacelda.configure({'background': "#454545"})
                    nuevacelda.config(justify = 'center', fg = 'white')        
    
    def Transpuesta(self, nombre):        
        matrix = self.matrizSeleccionada(nombre)
        x = int(matrix.filas)
        y = int(matrix.columnas)
        #IMPRESIÓN
        for a in range(x):
            for b in range(y):
                #IMPRESIÓN NORMAL
                celda = Entry(self.panelOriginal, width = 3)
                celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if matrix.retornarNodoEn(a+1, b+1) != None:
                    celda.insert(0,'*')
                    celda.configure({'background': "#454545"})
                    celda.config(justify = 'center', fg = 'white')
                #IMPRESIÓN GIRADA        
                nuevacelda = Entry(self.panelResultado, width = 3)    
                nuevacelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)                
                if matrix.retornarNodoEn(b+1, a+1) != None:
                    nuevacelda.insert(0,'*')
                    nuevacelda.configure({'background': "#454545"})
                    nuevacelda.config(justify = 'center', fg = 'white')
    
    def LimpiarZona(self, nombre, x1,y1,x2,y2):    
        #print(str(x1)+","+str(y1)+"  "+str(x2)+","+str(y2))    
        matrix = self.matrizSeleccionada(nombre)
        x = int(matrix.filas)
        y = int(matrix.columnas)
        #IMPRESIÓN
        for a in range(x):
            for b in range(y):
                #IMPRESIÓN NORMAL
                celda = Entry(self.panelOriginal, width = 3)
                celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if matrix.retornarNodoEn(a+1, b+1) != None:
                    celda.insert(0,'*')
                    celda.configure({'background': "#454545"})
                    celda.config(justify = 'center', fg = 'white')
                
                #IMPRESIÓN ZONA LIMPIA 
                nuevacelda = Entry(self.panelResultado, width = 3)    
                nuevacelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)                
                
                if matrix.retornarNodoEn(a+1, b+1) != None:
                    nuevacelda.insert(0,'*')
                    nuevacelda.configure({'background': "#454545"})
                    nuevacelda.config(justify = 'center', fg = 'white')
                    if (a>=(x1-1) and a<=(x2-1)) and (b>=(y1-1) and b<=(y2-1)):
                        nuevacelda.configure({'backgroun':'MediumPurple1'})
                        nuevacelda.delete(0, tk.END)
                if (a>=(x1-1) and a<=(x2-1)) and (b>=(y1-1) and b<=(y2-1)):
                    nuevacelda.configure({'backgroun':'MediumPurple1'})
                    nuevacelda.delete(0, tk.END)
                                                 
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
        self.titulo.configure(text = 'Eliga una operación para las matrices')
        self.matrices.mostrarNodos()
        self.matrices.retornarEn(1).recorrerFilas()
    
    def limpiarFramesMatrices(self):
        try:
            for child in self.panelOriginal.winfo_children():
                child.destroy()

            for child in self.panelResultado.winfo_children():
                child.destroy()
        except: 
            print('Excepción controlada')
    
    def limpiarBotones(self):
        try:
            for child in self.panelBotones.winfo_children():
                child.destroy()
        except: 
            print('Excepción controlada')


ventana = Interfaz()
