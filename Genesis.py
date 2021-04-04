import tkinter as tk
from tkinter import *
from tkinter import filedialog, font, messagebox, ttk
import os
from xml.dom import minidom
from ListaEnlazada import ListaEnlazada
from MatrizOrtogonal import *
import datetime
from webbrowser import open_new_tab

class Interfaz():
    def __init__(self):
        self.matrizAgregada = ''
        self.operacionesHechas = ''
        self.operacionSeleccionada = ''
        self.matrices = ListaEnlazada()            
        # Configuración de la raíz
        self.root = Tk()
        self.root.title("Proyecto 2 - IPC2")
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.scrollbarVertical = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        #self.scrollbarVertical.pack()
        self.scrollbarHorizontal = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        #self.scrollbarHorizontal.pack()

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
        self.operacionesMatriz.add_command(label="Unión A, B", command = lambda: self.botonApachado(9))
        self.operacionesMatriz.add_command(label="Inersección A, B", command = lambda: self.botonApachado(10))
        self.operacionesMatriz.add_command(label="Diferencia A, B", command = lambda: self.botonApachado(11))
        self.operacionesMatriz.add_command(label="Diferencia simétrica A, B", command = lambda: self.botonApachado(12))

        self.reportemenu = Menu(self.menubar, tearoff = 0)
        self.reportemenu.add_command(label = "Desplegar HTML", command = lambda: self.generarHTML())

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Información del desarrollador", command = lambda: self.mostrarInformación())
        self.helpmenu.add_command(label="Documentación del programa", command = lambda: self.desplegarPDF())

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
    
    def widgets2MatricesOperacion(self):
        #LIMPIO LOS FRAMES
        self.limpiarBotones()
        self.limpiarFramesMatrices()
        #AGREGO LOS CUATRO FRAMES
        self.panelBotones.grid(columnspan = 2, row = 1, padx = 5,pady = 5, sticky = (N, S, E, W))        
        self.panelOriginal.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = (N, S, E, W))
        self.panelOriginal2.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = (N, S, E, W))
        self.panelResultado.grid(row = 2, column = 2, padx = 5, pady = 5, sticky = (N, S, E, W))
        #AGREGO LOS COMPONENTES NECESARIOS
        self.indicador = Label(self.panelBotones, text = 'Seleccione una matriz')
        self.indicador.grid(padx = 5,row = 0, column = 0)
        listaMatrices = []
        for a in range(self.matrices.tamanio):
            listaMatrices.append(str(self.matrices.retornarEn(a+1).nombre))
        self.comboMatrices = ttk.Combobox(self.panelBotones, values = listaMatrices)
        self.comboMatrices.set(listaMatrices[0])
        self.comboMatrices.grid(padx = 5, row = 0, column = 1)

        self.indicador2 = Label(self.panelBotones, text = 'Seleccione otra matriz')
        self.indicador2.grid(padx = 5,row = 0, column = 2)
        self.comboMatrices2 = ttk.Combobox(self.panelBotones, values = listaMatrices)
        self.comboMatrices2.set(listaMatrices[1])
        self.comboMatrices2.grid(padx = 5, row = 0, column = 3)
        self.imprimir = Button(self.panelBotones, text = 'Imprimir', command = lambda: self.Imprimir(), bg = 'salmon')
        self.imprimir.grid(padx=5, row = 0, column = 4)


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
            self.altoentry = Entry(self.panelBotones, width = 2)
            self.altoentry.grid(padx = 3, row =0, column =6 )
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
            self.datoentry = Entry(self.panelBotones, width = 2)
            self.datoentry.grid(padx = 3, row =0, column =6 )
            self.imprimir = Button(self.panelBotones, text = 'Imprimir', command = lambda: self.Imprimir(), bg = 'salmon')
            self.imprimir.grid(padx=5, row = 0, column = 7)



    def botonApachado(self, valor):
        try:
            if valor == 1:
                self.limpiarBotones()
                self.limpiarFramesMatrices()
                self.titulo.configure(text = 'Giro horizontal de una imagen',)            
                self.inicializarWidgets()
                self.operacionSeleccionada = 'horizontal'
            if valor == 2:
                self.limpiarBotones()
                self.limpiarFramesMatrices()
                self.titulo.configure(text = 'Giro vertical de una imagen')
                self.inicializarWidgets()
                self.operacionSeleccionada = 'vertical'
            if valor == 3:
                self.limpiarBotones()
                self.limpiarFramesMatrices()
                self.titulo.configure(text = 'Transpuesta de una imagen')
                self.inicializarWidgets()
                self.operacionSeleccionada = 'transpuesta'
            if valor == 4:
                self.limpiarBotones()
                self.limpiarFramesMatrices()
                self.titulo.configure(text = 'Limpiar zona de una imagen')
                self.operacionSeleccionada = 'area'
                self.inicializarWidgets2()
            if valor == 5:
                self.limpiarBotones()
                self.limpiarFramesMatrices()
                self.titulo.configure(text = 'Linea horizontal en una imagen')
                self.operacionSeleccionada = 'lineah'
                self.inicializarWidgets2()
            if valor == 6:
                self.limpiarBotones()
                self.limpiarFramesMatrices()
                self.titulo.configure(text = 'Linea vertical en una imagen')
                self.operacionSeleccionada = 'lineav'
                self.inicializarWidgets2()
            if valor == 7:
                self.limpiarFramesMatrices()
                self.limpiarBotones()
                self.titulo.configure(text= 'Agregar rectangulo a una imagen')
                self.operacionSeleccionada = 'addrectangulo'
                self.inicializarWidgets2()
            if valor == 8:            
                self.limpiarBotones()
                self.limpiarFramesMatrices()
                self.titulo.configure(text= 'Agregar triangulo rectangulo')
                self.operacionSeleccionada = 'addtriangulo'
                self.inicializarWidgets2()
            if valor == 9:        
                self.limpiarBotones()
                self.limpiarFramesMatrices()                
                self.titulo.configure(text= 'Unión entre A y B')
                self.operacionSeleccionada = 'unionab'
                self.widgets2MatricesOperacion()
            if valor == 10:     
                self.limpiarBotones()
                self.limpiarFramesMatrices()                   
                self.titulo.configure(text= 'Intersección entre A y B')
                self.operacionSeleccionada = 'interseccionab'
                self.widgets2MatricesOperacion()
            if valor == 11:
                self.limpiarBotones()
                self.limpiarFramesMatrices()
                self.titulo.configure(text= 'Diferencia entre A y B')
                self.operacionSeleccionada = 'diferenciaab'
                self.widgets2MatricesOperacion()
            if valor == 12:
                self.limpiarBotones()
                self.limpiarFramesMatrices()
                self.titulo.configure(text= 'Diferencia simétrica entre A y B')
                self.operacionSeleccionada = 'simetricaab'
                self.widgets2MatricesOperacion()
        except:
            messagebox.showinfo(message="Cargue un archivo XML previamente para hacer uso de las operaciones", title="Advertencia")
                
    def Imprimir(self):
        if self.operacionSeleccionada =='horizontal':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            self.giroHorizontal(namematriz)
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")
            descripcion = '-'
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Rotación horizontal</td><td>'+namematriz+'</td><td></td></tr>\n'
        if self.operacionSeleccionada == 'vertical':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            self.giroVertical(namematriz)
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")
            descripcion = '-'
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Rotación vertical</td><td>'+namematriz+'</td><td></td></tr>\n'
        if self.operacionSeleccionada == 'transpuesta':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            self.Transpuesta(namematriz)
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")
            descripcion = '-'
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Transpuesta de una matriz</td><td>'+namematriz+'</td><td></td></tr>\n'
        if self.operacionSeleccionada == 'area':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            descripcion = '-'
            if self.x1.get().isdigit() and self.y1.get().isdigit() and self.x2.get().isdigit() and self.y2.get().isdigit():
                descripcion = self.LimpiarZona(namematriz,int(self.x1.get()), int(self.y1.get()),int(self.x2.get()), int(self.y2.get()))
            else:
                descripcion = 'Error: valores ingresados no numéricos.'
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")            
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Limpiar área en una matriz</td><td>'+namematriz+'</td><td></td></tr>\n'
        if self.operacionSeleccionada == 'lineah':
            self.limpiarFramesMatrices()            
            namematriz = self.comboMatrices.get()
            descripcion = '-'
            if self.filaEntry.get().isdigit() and self.columnaEntry.get() and self.cantidadEntry.get().isdigit():
                descripcion = self.LimpiarZona(namematriz,int(self.filaEntry.get()), int(self.columnaEntry.get()),int(self.filaEntry.get()), int(self.columnaEntry.get())+int(self.cantidadEntry.get())-1)
            else:
                descripcion = 'Error: valores ingresados no numéricos.'
            #self.addLineaHorizontal(namematriz,int(self.filaEntry.get()), int(self.columnaEntry.get()), int(self.cantidadEntry.get()))
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")            
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Dibujar linea horizontal</td><td>'+namematriz+'</td><td></td></tr>\n'
        if self.operacionSeleccionada == 'lineav':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            descripcion = '-'
            if self.filaEntry.get().isdigit() and self.columnaEntry.get() and self.cantidadEntry.get().isdigit():
                descripcion = self.LimpiarZona(namematriz,int(self.filaEntry.get()), int(self.columnaEntry.get()),int(self.filaEntry.get())+int(self.cantidadEntry.get())-1, int(self.columnaEntry.get()))
            else:
                descripcion = 'Error: valores ingresados no numéricos.'
            #self.addLineaVertical(namematriz,int(self.filaEntry.get()), int(self.columnaEntry.get()), int(self.cantidadEntry.get()))
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")            
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Dibujar linea vertical</td><td>'+namematriz+'</td><td></td></tr>\n'
        if self.operacionSeleccionada =='addrectangulo':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()            
            descripcion = '-'
            if self.x1.get().isdigit() and self.y1.get().isdigit() and self.anchoentry.get().isdigit() and self.altoentry.get().isdigit():
                descripcion = self.dibujarRectangulo(namematriz,int(self.x1.get()), int(self.y1.get()), int(self.x1.get()) + int(self.altoentry.get())-1, int(self.y1.get()) + int(self.anchoentry.get())-1)
            else:
                descripcion = 'Error: valores ingresados no numéricos.'
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")            
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Dibujar rectangulo</td><td>'+namematriz+'</td><td></td></tr>\n'
        if self.operacionSeleccionada =='addtriangulo':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()            
            descripcion = '-'
            if self.x1.get().isdigit() and self.y1.get().isdigit() and self.datoentry.get().isdigit():
                descripcion = self.dibujarTriangulo(namematriz,int(self.x1.get()), int(self.y1.get()), int(self.x1.get()) + int(self.datoentry.get())-1, int(self.y1.get()) + int(self.datoentry.get())-1)
            else:
                descripcion = 'Error: valores ingresados no numéricos.'
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")            
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Dibujar triangulo rectangulo</td><td>'+namematriz+'</td><td></td></tr>\n'
        if self.operacionSeleccionada =='unionab':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            namematriz2 = self.comboMatrices2.get()
            self.unionAB(namematriz, namematriz2)
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")
            descripcion = '-'
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Unión matrices A-B</td><td>'+namematriz+'</td><td>'+namematriz2+'</td></tr>\n'
        if self.operacionSeleccionada =='interseccionab':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            namematriz2 = self.comboMatrices2.get()
            self.interseccionAB(namematriz, namematriz2)
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")
            descripcion = '-'
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Intersección matrices A-B</td><td>'+namematriz+'</td><td>'+namematriz2+'</td></tr>\n'
        if self.operacionSeleccionada =='diferenciaab':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            namematriz2 = self.comboMatrices2.get()
            self.diferenciaAB(namematriz, namematriz2)
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")
            descripcion = '-'
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Diferencia matrices A-B</td><td>'+namematriz+'</td><td>'+namematriz2+'</td></tr>\n'
        if self.operacionSeleccionada =='simetricaab':
            self.limpiarFramesMatrices()
            namematriz = self.comboMatrices.get()
            namematriz2 = self.comboMatrices2.get()
            self.diferenciaSimetricaAB(namematriz, namematriz2)
            ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")
            descripcion = '-'
            self.operacionesHechas +='<tr><td>'+ahora+'</td><td>'+descripcion+'</td><td>Diferencia simétrica matrices A-B</td><td>'+namematriz+'</td><td>'+namematriz2+'</td></tr>\n'

    def matrizSeleccionada(self, nombre):
        for a in range(self.matrices.tamanio):
            if nombre == self.matrices.retornarEn(a+1).nombre:
                return self.matrices.retornarEn(a+1)            

    def giroHorizontal(self, nombre):        
        matrix = self.matrizSeleccionada(nombre)
        x = int(matrix.filas)
        y = int(matrix.columnas)
        #IMPRESIÓN
        for a in range(x+1):
            for b in range(y+1):
                #IMPRESIÓN NORMAL
                celda = Entry(self.panelOriginal, width = 3)
                celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if a == 0 and b ==0:
                    celda.insert(0,'A')
                    celda.configure({'backgroun':'red3'})
                    celda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    celda.insert(0,b)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    celda.insert(0,a)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(a, b) != None:
                    celda.insert(0,'*')
                    celda.configure({'background': "#454545"})
                    celda.config(justify = 'center', fg = 'white')
                #IMPRESIÓN GIRADA        
                nuevacelda = Entry(self.panelResultado, width = 3)    
                nuevacelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if a == 0 and b ==0:
                    nuevacelda.insert(0,'A')
                    nuevacelda.configure({'backgroun':'red3'})
                    nuevacelda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    nuevacelda.insert(0,b)
                    nuevacelda.configure({'backgroun':'gray'})
                    nuevacelda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    nuevacelda.insert(0,a)
                    nuevacelda.configure({'backgroun':'gray'})
                    nuevacelda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(x-a+1, b) != None:
                    nuevacelda.insert(0,'*')
                    nuevacelda.configure({'background': "#454545"})
                    nuevacelda.config(justify = 'center', fg = 'white')        
    
    def giroVertical(self, nombre):        
        matrix = self.matrizSeleccionada(nombre)
        x = int(matrix.filas)
        y = int(matrix.columnas)
        #IMPRESIÓN
        for a in range(x+1):
            for b in range(y+1):
                #IMPRESIÓN NORMAL
                celda = Entry(self.panelOriginal, width = 3)
                celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if a == 0 and b ==0:
                    celda.insert(0,'A')
                    celda.configure({'backgroun':'red3'})
                    celda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    celda.insert(0,b)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    celda.insert(0,a)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(a, b) != None:
                    celda.insert(0,'*')
                    celda.configure({'background': "#454545"})
                    celda.config(justify = 'center', fg = 'white')
                #IMPRESIÓN GIRADA        
                nuevacelda = Entry(self.panelResultado, width = 3)    
                nuevacelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)                
                if a == 0 and b ==0:
                    nuevacelda.insert(0,'A')
                    nuevacelda.configure({'backgroun':'red3'})
                    nuevacelda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    nuevacelda.insert(0,b)
                    nuevacelda.configure({'backgroun':'gray'})
                    nuevacelda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    nuevacelda.insert(0,a)
                    nuevacelda.configure({'backgroun':'gray'})
                    nuevacelda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(a, y-b+1) != None:
                    nuevacelda.insert(0,'*')
                    nuevacelda.configure({'background': "#454545"})
                    nuevacelda.config(justify = 'center', fg = 'white')        
    
    def Transpuesta(self, nombre):        
        matrix = self.matrizSeleccionada(nombre)
        x = int(matrix.filas)
        y = int(matrix.columnas)
        #IMPRESIÓN
        for a in range(x+1):
            for b in range(y+1):
                #IMPRESIÓN NORMAL
                celda = Entry(self.panelOriginal, width = 3)
                celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if a == 0 and b ==0:
                    celda.insert(0,'A')
                    celda.configure({'backgroun':'red3'})
                    celda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    celda.insert(0,b)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    celda.insert(0,a)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(a, b) != None:
                    celda.insert(0,'*')
                    celda.configure({'background': "#454545"})
                    celda.config(justify = 'center', fg = 'white')
        for a in range(y+1):
            for b in range(x+1):                
                #IMPRESIÓN GIRADA        
                nuevacelda = Entry(self.panelResultado, width = 3)    
                nuevacelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)                
                if a == 0 and b ==0:
                    nuevacelda.insert(0,'A')
                    nuevacelda.configure({'backgroun':'red3'})
                    nuevacelda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    nuevacelda.insert(0,b)
                    nuevacelda.configure({'backgroun':'gray'})
                    nuevacelda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    nuevacelda.insert(0,a)
                    nuevacelda.configure({'backgroun':'gray'})
                    nuevacelda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(b, a) != None:
                    nuevacelda.insert(0,'*')
                    nuevacelda.configure({'background': "#454545"})
                    nuevacelda.config(justify = 'center', fg = 'white')
    
    def LimpiarZona(self, nombre, x1,y1,x2,y2):    
        #print(str(x1)+","+str(y1)+"  "+str(x2)+","+str(y2))    
        matrix = self.matrizSeleccionada(nombre)
        x = int(matrix.filas)
        y = int(matrix.columnas)
        #IMPRESIÓN
        for a in range(x+1):
            for b in range(y+1):
                #IMPRESIÓN NORMAL
                celda = Entry(self.panelOriginal, width = 3)
                celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if a == 0 and b ==0:
                    celda.insert(0,'A')
                    celda.configure({'backgroun':'red3'})
                    celda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    celda.insert(0,b)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    celda.insert(0,a)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(a, b) != None:
                    celda.insert(0,'*')
                    celda.configure({'background': "#454545"})
                    celda.config(justify = 'center', fg = 'white')

        if x1>0 and x2>0 and y1>0 and y2>0:
            for a in range(x+1):
                for b in range(y+1):        
                    if (x1<=x and x2<=x) and (y1<=y and y2<=y):
                        if x1<=x2 and y1<=y2:    
                            #IMPRESIÓN ZONA LIMPIA 
                            nuevacelda = Entry(self.panelResultado, width = 3)    
                            nuevacelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)                
                            if a == 0 and b ==0:
                                nuevacelda.insert(0,'A')
                                nuevacelda.configure({'backgroun':'red3'})
                                nuevacelda.config(justify = 'center',fg = 'white')
                            if a == 0 and b>0:
                                nuevacelda.insert(0,b)
                                nuevacelda.configure({'backgroun':'gray'})
                                nuevacelda.config(justify = 'center',fg = 'white')
                            if a > 0 and b==0:
                                nuevacelda.insert(0,a)
                                nuevacelda.configure({'backgroun':'gray'})
                                nuevacelda.config(justify = 'center',fg = 'white')
                            if matrix.retornarNodoEn(a, b) != None:
                                nuevacelda.insert(0,'*')
                                nuevacelda.configure({'background': "#454545"})
                                nuevacelda.config(justify = 'center', fg = 'white')
                                if (a>=(x1) and a<=(x2)) and (b>=(y1) and b<=(y2)):
                                    nuevacelda.configure({'backgroun':'purple1'})
                                    #nuevacelda.delete(0, tk.END)
                            if (a>=(x1) and a<=(x2)) and (b>=(y1) and b<=(y2)):
                                nuevacelda.configure({'backgroun':'purple1'})
                        else:
                            return 'Error: Incongruencia en las coordenadas ingresadas.'
                    else:
                        return 'Error: Las coordenadas ingresadas sobrepasan el tamaño de la matriz.'
            return '-'
        else:
            return 'Error: Coordenadas ingresadas son negativas.'

    def dibujarRectangulo(self, nombre, x1,y1,x2,y2):            
        matrix = self.matrizSeleccionada(nombre)
        x = int(matrix.filas)
        y = int(matrix.columnas)
        #IMPRESIÓN
        for a in range(x+1):
            for b in range(y+1):
                #IMPRESIÓN NORMAL
                celda = Entry(self.panelOriginal, width = 3)
                celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if a == 0 and b ==0:
                    celda.insert(0,'A')
                    celda.configure({'backgroun':'red3'})
                    celda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    celda.insert(0,b)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    celda.insert(0,a)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(a, b) != None:
                    celda.insert(0,'*')
                    celda.configure({'background': "#454545"})
                    celda.config(justify = 'center', fg = 'white')
        if x1>0 and x2>0 and y1>0 and y2>0:
            for a in range(x+1):
                for b in range(y+1):
                    if (x1<=x and x2<=x) and (y1<=y and y2<=y):
                        if x1<x2 and y1<y2:
                            #IMPRESIÓN DEL RECTANGULO
                            nuevacelda = Entry(self.panelResultado, width = 3)    
                            nuevacelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)                
                            if a == 0 and b ==0:
                                nuevacelda.insert(0,'A')
                                nuevacelda.configure({'backgroun':'red3'})
                                nuevacelda.config(justify = 'center',fg = 'white')
                            if a == 0 and b>0:
                                nuevacelda.insert(0,b)
                                nuevacelda.configure({'backgroun':'gray'})
                                nuevacelda.config(justify = 'center',fg = 'white')
                            if a > 0 and b==0:
                                nuevacelda.insert(0,a)
                                nuevacelda.configure({'backgroun':'gray'})
                                nuevacelda.config(justify = 'center',fg = 'white')
                            if matrix.retornarNodoEn(a, b) != None:
                                nuevacelda.insert(0,'*')
                                nuevacelda.configure({'background': "#454545"})
                                nuevacelda.config(justify = 'center', fg = 'white')
                                if (a==(x1)) and (b>=(y1) and b<=(y2)):
                                    nuevacelda.configure({'backgroun':'purple1'})
                                    #nuevacelda.delete(0, tk.END)
                                if (a==(x2)) and (b>=(y1) and b<=(y2)):
                                    nuevacelda.configure({'backgroun':'purple1'})
                                    #nuevacelda.delete(0, tk.END)
                                if (a>=(x1) and a<=(x2)) and (b==(y1)):
                                    nuevacelda.configure({'backgroun':'purple1'})
                                    #nuevacelda.delete(0, tk.END)
                                if (a>=(x1) and a<=(x2)) and (b==(y2)):
                                    nuevacelda.configure({'backgroun':'purple1'})
                                    #nuevacelda.delete(0, tk.END)
                            if (a==(x1)) and (b>=(y1) and b<=(y2)):
                                    nuevacelda.configure({'backgroun':'purple1'})
                                    #nuevacelda.delete(0, tk.END)
                            if (a==(x2)) and (b>=(y1) and b<=(y2)):
                                nuevacelda.configure({'backgroun':'purple1'})
                                #nuevacelda.delete(0, tk.END)
                            if (a>=(x1) and a<=(x2)) and (b==(y1)):
                                nuevacelda.configure({'backgroun':'purple1'})
                                #nuevacelda.delete(0, tk.END)
                            if (a>=(x1) and a<=(x2)) and (b==(y2)):
                                nuevacelda.configure({'backgroun':'purple1'})
                                #nuevacelda.delete(0, tk.END)
                        else:
                            return 'Error: Incongruencia en las coordenadas ingresadas.'
                    else:
                        return 'Error: Las coordenadas ingresadas sobrepasan el tamaño de la matriz.'
            return '-'
        else:
            return 'Error: Coordenadas ingresadas son negativas.'
    
    def dibujarTriangulo(self, nombre, x1, y1, x2, y2):            
        matrix = self.matrizSeleccionada(nombre)
        x = int(matrix.filas)
        y = int(matrix.columnas)
        contador = 1
        nuevaColumna = int(y1)+1
        nuevaFila = int(x1)+1
        #IMPRESIÓN
        for a in range(x+1):
            for b in range(y+1):
                
                #IMPRESIÓN NORMAL
                celda = Entry(self.panelOriginal, width = 3)
                celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if a == 0 and b ==0:
                    celda.insert(0,'A')
                    celda.configure({'backgroun':'red3'})
                    celda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    celda.insert(0,b)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    celda.insert(0,a)
                    celda.configure({'backgroun':'gray'})
                    celda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(a, b) != None:
                    celda.insert(0,'*')
                    celda.configure({'background': "#454545"})
                    celda.config(justify = 'center', fg = 'white')
        if x1>0 and x2>0 and y1>0 and y2>0:
            for a in range(x+1):
                for b in range(y+1):
                    if (x1<=x and x2<=x) and (y1<=y and y2<=y):
                        if x1<x2 and y1<y2:
                            #IMPRESIÓN DEL TRIANGULO RECTANGULO
                            nuevacelda = Entry(self.panelResultado, width = 3)    
                            nuevacelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)                
                            if a == 0 and b ==0:
                                nuevacelda.insert(0,'A')
                                nuevacelda.configure({'backgroun':'red3'})
                                nuevacelda.config(justify = 'center',fg = 'white')
                            if a == 0 and b>0:
                                nuevacelda.insert(0,b)
                                nuevacelda.configure({'backgroun':'gray'})
                                nuevacelda.config(justify = 'center',fg = 'white')
                            if a > 0 and b==0:
                                nuevacelda.insert(0,a)
                                nuevacelda.configure({'backgroun':'gray'})
                                nuevacelda.config(justify = 'center',fg = 'white')
                            if matrix.retornarNodoEn(a, b) != None:
                                nuevacelda.insert(0,'*')
                                nuevacelda.configure({'background': "#454545"})
                                nuevacelda.config(justify = 'center', fg = 'white')
                                if (a==(x2)) and (b>=(y1) and b<=(y2)):
                                    nuevacelda.configure({'backgroun':'purple1'})
                                    #nuevacelda.delete(0, tk.END)
                                if (a>=(x1) and a<=(x2)) and (b==(y1)):
                                    nuevacelda.configure({'backgroun':'purple1'})
                                    #nuevacelda.delete(0, tk.END)                    
                                
                                if (a>(x1) and a<(x2)) and (nuevaColumna==b) and (nuevaFila==a) and (b>(y1) and b<(y2)):
                                    nuevacelda.configure({'backgroun':'purple1'})
                                    #nuevacelda.delete(0, tk.END)              
                                    nuevaColumna+=1   
                                    nuevaFila+=1       
                            
                            if (a==(x2)) and (b>=(y1) and b<=(y2)):
                                nuevacelda.configure({'backgroun':'purple1'})
                                #nuevacelda.delete(0, tk.END)
                            if (a>=(x1) and a<=(x2)) and (b==(y1)):
                                nuevacelda.configure({'backgroun':'purple1'})
                                #nuevacelda.delete(0, tk.END)                                
                            if (a>(x1) and a<(x2)) and (nuevaColumna==b) and (nuevaFila==a) and (b>(y1) and b<(y2)):
                                nuevacelda.configure({'backgroun':'purple1'})
                                #nuevacelda.delete(0, tk.END)              
                                nuevaColumna+=1      
                                nuevaFila+=1
                        else:
                            return 'Error: Incongruencia en las coordenadas ingresadas.'
                    else:
                        return 'Error: Las coordenadas ingresadas sobrepasan el tamaño de la matriz.'
            return '-'
        else:
            return 'Error: Coordenadas ingresadas son negativas.'

    def unionAB(self, nombre, nombre2):        
        matrix = self.matrizSeleccionada(nombre)        
        x = int(matrix.filas)
        y = int(matrix.columnas)
        matrix2 = self.matrizSeleccionada(nombre2)
        xx = int(matrix2.filas)
        yy = int(matrix2.columnas)
        if x >= xx:
            fila = x
        else:
            fila = xx
        if y >= yy:
            columna = y
        else:
            columna = yy
        #IMPRESIÓN
        for a in range(fila+1):
            for b in range(columna+1):
                if a < x+1 and b < y+1:
                    #IMPRESIÓN NORMAL MATRIZ 1
                    celda = Entry(self.panelOriginal, width = 3)
                    celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                    if a == 0 and b ==0:
                        celda.insert(0,'A')
                        celda.configure({'backgroun':'red3'})
                        celda.config(justify = 'center',fg = 'white')
                    if a == 0 and b>0:
                        celda.insert(0,b)
                        celda.configure({'backgroun':'gray'})
                        celda.config(justify = 'center',fg = 'white')
                    if a > 0 and b==0:
                        celda.insert(0,a)
                        celda.configure({'backgroun':'gray'})
                        celda.config(justify = 'center',fg = 'white')
                    if matrix.retornarNodoEn(a, b) != None:
                        celda.insert(0,'*')
                        celda.configure({'background': "#454545"})
                        celda.config(justify = 'center', fg = 'white')
                if a < xx+1 and b < yy+1:
                    #IMPRESIÓN NORMAL MATRIZ 2
                    celda2 = Entry(self.panelOriginal2, width = 3)
                    celda2.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                    if a == 0 and b ==0:
                        celda2.insert(0,'A')
                        celda2.configure({'backgroun':'red3'})
                        celda2.config(justify = 'center',fg = 'white')
                    if a == 0 and b>0:
                        celda2.insert(0,b)
                        celda2.configure({'backgroun':'gray'})
                        celda2.config(justify = 'center',fg = 'white')
                    if a > 0 and b==0:
                        celda2.insert(0,a)
                        celda2.configure({'backgroun':'gray'})
                        celda2.config(justify = 'center',fg = 'white')
                    if matrix2.retornarNodoEn(a, b) != None:
                        celda2.insert(0,'*')
                        celda2.configure({'background': "#454545"})
                        celda2.config(justify = 'center', fg = 'white')        
                #IMPRESIÓN DE LA UNION
                nuevaCelda = Entry(self.panelResultado, width = 3)
                nuevaCelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if a == 0 and b ==0:
                    nuevaCelda.insert(0,'A')
                    nuevaCelda.configure({'backgroun':'red3'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    nuevaCelda.insert(0,b)
                    nuevaCelda.configure({'backgroun':'gray'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    nuevaCelda.insert(0,a)
                    nuevaCelda.configure({'backgroun':'gray'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(a, b) != None or matrix2.retornarNodoEn(a, b) != None:
                    nuevaCelda.insert(0,'*')
                    nuevaCelda.configure({'background': "#454545"})
                    nuevaCelda.config(justify = 'center', fg = 'white')

    def interseccionAB(self, nombre, nombre2):        
        matrix = self.matrizSeleccionada(nombre)        
        x = int(matrix.filas)
        y = int(matrix.columnas)
        matrix2 = self.matrizSeleccionada(nombre2)
        xx = int(matrix2.filas)
        yy = int(matrix2.columnas)
        if x >= xx:
            fila = x
        else:
            fila = xx
        if y >= yy:
            columna = y
        else:
            columna = yy
        #IMPRESIÓN
        for a in range(fila+1):
            for b in range(columna+1):
                if a < x+1 and b < y+1:
                    #IMPRESIÓN NORMAL MATRIZ 1
                    celda = Entry(self.panelOriginal, width = 3)
                    celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                    if a == 0 and b ==0:
                        celda.insert(0,'A')
                        celda.configure({'backgroun':'red3'})
                        celda.config(justify = 'center',fg = 'white')
                    if a == 0 and b>0:
                        celda.insert(0,b)
                        celda.configure({'backgroun':'gray'})
                        celda.config(justify = 'center',fg = 'white')
                    if a > 0 and b==0:
                        celda.insert(0,a)
                        celda.configure({'backgroun':'gray'})
                        celda.config(justify = 'center',fg = 'white')                    
                    if matrix.retornarNodoEn(a, b) != None:
                        celda.insert(0,'*')
                        celda.configure({'background': "#454545"})
                        celda.config(justify = 'center', fg = 'white')
                if a < xx+1 and b < yy+1:
                    #IMPRESIÓN NORMAL MATRIZ 2
                    celda2 = Entry(self.panelOriginal2, width = 3)
                    celda2.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                    
                    if a == 0 and b ==0:
                        celda2.insert(0,'A')
                        celda2.configure({'backgroun':'red3'})
                        celda2.config(justify = 'center',fg = 'white')
                    if a == 0 and b>0:
                        celda2.insert(0,b)
                        celda2.configure({'backgroun':'gray'})
                        celda2.config(justify = 'center',fg = 'white')
                    if a > 0 and b==0:
                        celda2.insert(0,a)
                        celda2.configure({'backgroun':'gray'})
                        celda2.config(justify = 'center',fg = 'white')
                    if matrix2.retornarNodoEn(a, b) != None:
                        celda2.insert(0,'*')
                        celda2.configure({'background': "#454545"})
                        celda2.config(justify = 'center', fg = 'white')        
                #IMPRESIÓN DE INTERSECCIÓN
                nuevaCelda = Entry(self.panelResultado, width = 3)
                nuevaCelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if a == 0 and b ==0:
                    nuevaCelda.insert(0,'A')
                    nuevaCelda.configure({'backgroun':'red3'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    nuevaCelda.insert(0,b)
                    nuevaCelda.configure({'backgroun':'gray'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    nuevaCelda.insert(0,a)
                    nuevaCelda.configure({'backgroun':'gray'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(a, b) != None and matrix2.retornarNodoEn(a, b) != None:
                    nuevaCelda.insert(0,'*')
                    nuevaCelda.configure({'background': "#454545"})
                    nuevaCelda.config(justify = 'center', fg = 'white')
        
    def diferenciaAB(self, nombre, nombre2):        
        matrix = self.matrizSeleccionada(nombre)        
        x = int(matrix.filas)
        y = int(matrix.columnas)
        matrix2 = self.matrizSeleccionada(nombre2)
        xx = int(matrix2.filas)
        yy = int(matrix2.columnas)
        if x >= xx:
            fila = x
        else:
            fila = xx
        if y >= yy:
            columna = y
        else:
            columna = yy
        #IMPRESIÓN
        for a in range(fila+1):
            for b in range(columna+1):
                if a < x+1 and b < y+1:
                    #IMPRESIÓN NORMAL MATRIZ 1
                    celda = Entry(self.panelOriginal, width = 3)
                    celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                    if a == 0 and b ==0:
                        celda.insert(0,'A')
                        celda.configure({'backgroun':'red3'})
                        celda.config(justify = 'center',fg = 'white')
                    if a == 0 and b>0:
                        celda.insert(0,b)
                        celda.configure({'backgroun':'gray'})
                        celda.config(justify = 'center',fg = 'white')
                    if a > 0 and b==0:
                        celda.insert(0,a)
                        celda.configure({'backgroun':'gray'})
                        celda.config(justify = 'center',fg = 'white')                    
                    if matrix.retornarNodoEn(a, b) != None:
                        celda.insert(0,'*')
                        celda.configure({'background': "#454545"})
                        celda.config(justify = 'center', fg = 'white')
                if a < xx+1 and b < yy+1:
                    #IMPRESIÓN NORMAL MATRIZ 2
                    celda2 = Entry(self.panelOriginal2, width = 3)
                    celda2.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                    if a == 0 and b ==0:
                        celda2.insert(0,'A')
                        celda2.configure({'backgroun':'red3'})
                        celda2.config(justify = 'center',fg = 'white')
                    if a == 0 and b>0:
                        celda2.insert(0,b)
                        celda2.configure({'backgroun':'gray'})
                        celda2.config(justify = 'center',fg = 'white')
                    if a > 0 and b==0:
                        celda2.insert(0,a)
                        celda2.configure({'backgroun':'gray'})
                        celda2.config(justify = 'center',fg = 'white')
                    if matrix2.retornarNodoEn(a, b) != None:
                        celda2.insert(0,'*')
                        celda2.configure({'background': "#454545"})
                        celda2.config(justify = 'center', fg = 'white')        
                #IMPRESIÓN DE DIFERENCIA
                nuevaCelda = Entry(self.panelResultado, width = 3)
                nuevaCelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if a == 0 and b ==0:
                    nuevaCelda.insert(0,'A')
                    nuevaCelda.configure({'backgroun':'red3'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    nuevaCelda.insert(0,b)
                    nuevaCelda.configure({'backgroun':'gray'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    nuevaCelda.insert(0,a)
                    nuevaCelda.configure({'backgroun':'gray'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(a, b) != None:
                    nuevaCelda.insert(0,'*')
                    nuevaCelda.configure({'background': "#454545"})
                    nuevaCelda.config(justify = 'center', fg = 'white')
                    if matrix2.retornarNodoEn(a, b) != None:                        
                        nuevaCelda.configure({'background': "white"})                        
                        nuevaCelda.delete(0, tk.END)

    def diferenciaSimetricaAB(self, nombre, nombre2):        
        matrix = self.matrizSeleccionada(nombre)        
        x = int(matrix.filas)
        y = int(matrix.columnas)
        matrix2 = self.matrizSeleccionada(nombre2)
        xx = int(matrix2.filas)
        yy = int(matrix2.columnas)
        if x >= xx:
            fila = x
        else:
            fila = xx
        if y >= yy:
            columna = y
        else:
            columna = yy
        #IMPRESIÓN
        for a in range(fila+1):
            for b in range(columna+1):
                if a < x+1 and b < y+1:
                    #IMPRESIÓN NORMAL MATRIZ 1
                    celda = Entry(self.panelOriginal, width = 3)
                    celda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                    if a == 0 and b ==0:
                        celda.insert(0,'A')
                        celda.configure({'backgroun':'red3'})
                        celda.config(justify = 'center',fg = 'white')
                    if a == 0 and b>0:
                        celda.insert(0,b)
                        celda.configure({'backgroun':'gray'})
                        celda.config(justify = 'center',fg = 'white')
                    if a > 0 and b==0:
                        celda.insert(0,a)
                        celda.configure({'backgroun':'gray'})
                        celda.config(justify = 'center',fg = 'white')                    
                    if matrix.retornarNodoEn(a, b) != None:
                        celda.insert(0,'*')
                        celda.configure({'background': "#454545"})
                        celda.config(justify = 'center', fg = 'white')
                if a < xx+1 and b < yy+1:
                    #IMPRESIÓN NORMAL MATRIZ 2
                    celda2 = Entry(self.panelOriginal2, width = 3)
                    celda2.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                    if a == 0 and b ==0:
                        celda2.insert(0,'A')
                        celda2.configure({'backgroun':'red3'})
                        celda2.config(justify = 'center',fg = 'white')
                    if a == 0 and b>0:
                        celda2.insert(0,b)
                        celda2.configure({'backgroun':'gray'})
                        celda2.config(justify = 'center',fg = 'white')
                    if a > 0 and b==0:
                        celda2.insert(0,a)
                        celda2.configure({'backgroun':'gray'})
                        celda2.config(justify = 'center',fg = 'white')
                    if matrix2.retornarNodoEn(a, b) != None:
                        celda2.insert(0,'*')
                        celda2.configure({'background': "#454545"})
                        celda2.config(justify = 'center', fg = 'white')        
                #IMPRESIÓN DE DIFERENCIA SIMÉTRICA
                nuevaCelda = Entry(self.panelResultado, width = 3)
                nuevaCelda.grid(padx = 5, pady = 5, row = a, column = b, columnspan = 1)
                if a == 0 and b ==0:
                    nuevaCelda.insert(0,'A')
                    nuevaCelda.configure({'backgroun':'red3'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if a == 0 and b>0:
                    nuevaCelda.insert(0,b)
                    nuevaCelda.configure({'backgroun':'gray'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if a > 0 and b==0:
                    nuevaCelda.insert(0,a)
                    nuevaCelda.configure({'backgroun':'gray'})
                    nuevaCelda.config(justify = 'center',fg = 'white')
                if matrix.retornarNodoEn(a, b) != None:
                    nuevaCelda.insert(0,'*')
                    nuevaCelda.configure({'background': "#454545"})
                    nuevaCelda.config(justify = 'center', fg = 'white')
                    if matrix2.retornarNodoEn(a, b) != None:
                        nuevaCelda.configure({'background': "white"})                        
                        nuevaCelda.delete(0, tk.END)
                if matrix2.retornarNodoEn(a, b) != None:
                    nuevaCelda.insert(0,'*')
                    nuevaCelda.configure({'background': "#454545"})
                    nuevaCelda.config(justify = 'center', fg = 'white')
                    if matrix.retornarNodoEn(a, b) != None:                        
                        nuevaCelda.configure({'background': "white"})                        
                        nuevaCelda.delete(0, tk.END)

    def generarHTML(self):
        html = open('Reporte HTML.html','w')
        html.write('<!DOCTYPE html>\n')
        html.write('<html>\n')
        html.write('<head>\n')
        html.write('<style>\n')
        html.write('table {\n')
        html.write('    border-collapse: collapse;\n')
        html.write('    width: 100%;\n')
        html.write('}')
        html.write('th, td {\n')
        html.write('    text-align: left;\n')
        html.write('    padding: 8px;\n')
        html.write('}')
        html.write('tr:nth-child(even) {\n')
        html.write('    background-color: #f2f2f2;\n')
        html.write('}')
        html.write('th {\n')
        html.write('    background-color: #4CAF50;\n')
        html.write('    color: white;\n')
        html.write('}')
        html.write('</style>\n')
        html.write('</head>\n')
        html.write('<body>\n')
        html.write('<h2>Matrices cargadas.</h2>\n')
        html.write('<table>\n')
        html.write('    <tr>\n')
        html.write('        <th>Fecha y hora</th>\n')
        html.write('        <th>Nombre de la matriz</th>\n')
        html.write('        <th>Espacios llenos</th>\n')
        html.write('        <th>Espacios vacíos</th>\n')
        html.write('    </tr>\n')
        #AQUI VA MI VARIABLE DE MATRICES AGREGADAS
        html.write(self.matrizAgregada)
        html.write('</table>\n')
        html.write('<h2>Bitácora de operaciones.</h2>\n')
        html.write('<table>\n')
        html.write('    <tr>\n')
        html.write('        <th>Fecha y hora</th>\n')
        html.write('        <th>Descripción del error</th>\n')
        html.write('        <th>Operación</th>\n')
        html.write('        <th>Matriz 1</th>\n')
        html.write('        <th>Matriz 2</th>\n')
        html.write('    </tr>\n')
        #AQUI VA MI VARIABLE DE OPERACIONES HECHAS
        html.write(self.operacionesHechas)
        html.write('</table>\n')

        html.write('</body>\n')
        html.write('</html>\n')
        html.close()
        open_new_tab('Reporte HTML.html')

    def abrirXML(self):
        try:
            archivo = filedialog.askopenfilename(initialdir = "/", title = "Seleccione el archivo XML: ", filetypes = (("archivos XML", "*.xml"),("all files","*.*")))        
            mixml = minidom.parse(archivo)        
            try:
                nombres = mixml.getElementsByTagName('matriz')
                for matriz in nombres:            
                    llenos = 0
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
                                    llenos+=1
                                columnaNodo+=1

                    
                    self.matrices.insertar(nuevaMatriz)
                    ahora = datetime.datetime.today().strftime("%d/%m/%Y - %H:%M:%S")
                    vacios = ((int(fil)*int(col))-llenos)
                    self.matrizAgregada +='<tr><td>'+ahora+'</td><td>'+nom+'</td><td>'+str(llenos)+'</td><td>'+str(vacios)+'</td></tr>\n'
                self.titulo.configure(text = 'Eliga una operación para las matrices')
                self.matrices.mostrarNodos()
                self.matrices.retornarEn(1).recorrerFilas()
            except:
                messagebox.showinfo(message="El formato del XML cargado es invalido, verifique su archivo", title="Advertencia")
        except:
            messagebox.showinfo(message="Debe cargar un archivo XML", title="Advertencia")
    
    def limpiarFramesMatrices(self):
        try:
            for child in self.panelOriginal.winfo_children():
                child.destroy()
            
            for child in self.panelOriginal2.winfo_children():
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

    def mostrarInformación(self):
        messagebox.showinfo(message='Nombre: Luis Amilcar Morales Xón\nCarnet: 201701059\nCurso:Introducción a la programación y computación 2',title='Información del desarrollador')
    
    def desplegarPDF(self):
        try:
            os.system('/Documentación/Documentación Proyecto2 - IPC2.pdf')
            open_new_tab('Reporte HTML.html')
        except:
            messagebox.showinfo(message="El archivo no se puede visualizar, puede que haya sido eliminado.", title="Advertencia")

ventana = Interfaz()
