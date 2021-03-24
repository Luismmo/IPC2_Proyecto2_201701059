from tkinter import *
from tkinter import filedialog, ttk, font
import os
from xml.dom import minidom
from ListaEnlazada import ListaEnlazada
from MatrizOrtogonal import *

class Interfaz():
    def __init__(self):
        self.opcionSeleccionada = ''
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
        self.operacionesMatriz.add_command(label="Giro vertical")
        self.operacionesMatriz.add_command(label="Transpuesta")
        self.operacionesMatriz.add_command(label="Limpiar zona")
        self.operacionesMatriz.add_command(label="Agregar linea horizontal")
        self.operacionesMatriz.add_command(label="Agregar linea vertical")
        self.operacionesMatriz.add_command(label="Agregar rectangulo")
        self.operacionesMatriz.add_command(label="Agregar triangulo rectangulo")
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

        self.titulo = Label(self.root)
        #FRAME BOTONES
        self.panelBotones = Frame(self.root, borderwidth = 2, relief = 'raised')        

        #FRAME MATRIZ ORIGINAL NUMERO UNO
        self.panelOriginal = Frame(self.root, borderwidth = 2, relief = 'raised', bg="lightblue")             

        #FRAME MATRIZ ORIGINAL NUMERO DOS
        self.panelOriginal2 = Frame(self.root, borderwidth = 2, relief = 'raised', bg="lightblue")             

        #FRAME MATRIZ RESULTADO
        self.panelResultado = Frame(self.root, borderwidth = 2, relief = 'raised', bg="gold")        

        # Finalmente bucle de la aplicación
        self.root.geometry('1100x590')
        #self.root.resizable(False,False)
        self.root.mainloop()
    
    def inicializarWidgets(self):
        #AGREGO LOS FRAMES
        self.titulo.grid(row =0, sticky = (N, S, E, W))
        self.panelBotones.grid(row = 1, padx = 5,pady = 5, sticky = (N, S, E, W))        
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
        self.imprimir = Button(self.panelBotones, text = 'Imprimir', command = lambda: self.Imprimir())
        self.imprimir.grid(padx=5, row = 0, column = 2)

    def botonApachado(self, valor):
        if valor == 1:
            self.titulo.configure(text = 'Giro horizontal')
            self.titulo.config(font = ('Verdana', 18))
            self.inicializarWidgets()
            
    
    def Imprimir(self):
        namematriz = self.comboMatrices.get()
        self.giroHorizontal(namematriz)

    def matrizSeleccionada(self, nombre):
        for a in range(self.matrices.tamanio):
            if nombre == self.matrices.retornarEn(a+1).nombre:
                return self.matrices.retornarEn(a+1)            

    def giroHorizontal(self, nombre):        
        matrix = self.matrizSeleccionada(nombre)
        x = int(matrix.filas)
        y = int(matrix.columnas)
        #IMPRESIÓN NORMAL
        for a in range(x):
            for b in range(y):
                celda = Entry(self.panelOriginal, width = 3)
                celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)

                if matrix.retornarNodoEn(a+1, b+1) != None:
                    celda.insert(0,'*')
                    celda.configure({'background': "#454545"})
                    celda.config(justify = 'center', fg = 'white')
        #IMPRESIÓN GIRADA
        for a in range(x):
            for b in range(y):                
                if matrix.retornarNodoEn(a+1, b+1) != None:                    
                    nuevacelda = Entry(self.panelResultado, width = 3)    
                    #CAMBIANDO COORDENADAS
                    newfila = x - (a+1)
                    nuevacelda.insert(0,'*')
                    nuevacelda.configure({'background': "#454545"})
                    nuevacelda.config(justify = 'center', fg = 'white')
                    nuevacelda.grid(padx = 5, pady = 5, row = newfila, column = b, columnspan = 1)                
                else:
                    celda = Entry(self.panelResultado, width = 3)
                    celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)                
                


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

ventana = Interfaz()