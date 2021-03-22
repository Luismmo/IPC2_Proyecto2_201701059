class Nodo(object):
    def __init__(self, dato, fila, columna):
        self.fila = fila
        self.columna = columna
        self.dato = dato
        self.izquierda = None
        self.derecha = None
        self.abajo = None
        self.arriba = None

class Encabezado(object):
    def __init__(self, numero):
        self.numero = numero
        self.siguiente = None
        self.anterior = None
        #acceso es un puntero al Nodo
        self.acceso = None

class ListaEncabazado(object):
    def __init__(self):
        self.inicio = None
        self.tamanio = 0

    #metodo insertar nuevo nodo clase Encabezado
    def insertar(self, numero):
        nuevo = Encabezado(numero)
        if self.esVacia()==True: #insertar cuando está VACÍO
            self.inicio = nuevo
            #self.inicio.siguiente = self.inicio
            #self.tamanio+=1
            print('que indice estoy comparando?'+ str(self.inicio.numero))
        else:            
            
            if int(nuevo.numero) < int(self.inicio.numero): # insertar al INICIO
                nuevo.siguiente = self.inicio
                self.inicio.anterior = nuevo
                self.inicio = nuevo
            else:
                temporal = self.inicio
                while temporal.siguiente != None:
                    if int(nuevo.numero) < int(temporal.siguiente.numero): # insertar en MEDIO
                        nuevo.siguiente = temporal.siguiente
                        temporal.siguiente.anterior = nuevo
                        nuevo.anterior = temporal
                        break
                    temporal = temporal.siguiente
                
                if temporal.siguiente == None: # insertar al FINAL
                    temporal.siguiente = nuevo
                    nuevo.anterior = temporal
                
    #metodo obtener en tal posicion
    def retornarEn(self, numero):
        temporal = self.inicio        
        while temporal != None:
            if temporal.numero == numero:
                return temporal
            temporal = temporal.siguiente
        
        return None
    
    def esVacia(self):
        if self.inicio == None:
            return True
        else:
            return False

class Matriz(object):
    def __init__(self):
        self.eFilas = ListaEncabazado()
        self.eColumnas = ListaEncabazado()

    # metodo insertar
    def insertar(self, dato, fila, columna):
        nuevo = Nodo(dato,fila,columna)
        #INSERCIÓN DE FILAS
        encabezadoFila = self.eFilas.retornarEn(fila)
        if encabezadoFila == None: #INSERCION SI NO EXISTE NINGUN ENCABEZADO
            encabezadoFila = Encabezado(fila)
            encabezadoFila.acceso = nuevo
            self.eFilas.insertar(encabezadoFila)            
        else: 
            #INSERTAR AL INICIO 
            if int(nuevo.columna) < int(encabezadoFila.acceso.columna):
                nuevo.derecha = encabezadoFila.acceso
                encabezadoFila.acceso.izquierda = nuevo
                encabezadoFila.acceso = nuevo
            else:
                temporal = encabezadoFila.acceso
                while temporal.derecha !=None:
                    if int(nuevo.columna) < int(temporal.derecha.columna): #INSERTAR EN MEDIO 
                        nuevo.derecha = temporal.derecha
                        temporal.derecha.izquierda = nuevo
                        nuevo.izquierda = temporal
                        temporal.derecha = nuevo
                        break
                    temporal = temporal.derecha
                
                if temporal.derecha == None: #INSERTAR AL FINALs
                    temporal.derecha = nuevo
                    nuevo.izquierda = temporal
        #INSERCIÓN DE COLUMNAS
        encabezadoColumna = self.eColumnas.retornarEn(columna)
        if encabezadoColumna == None: # SI NO EXISTE ENCABEZADO SE CREA UNO
            encabezadoColumna = Encabezado(columna)
            self.eColumnas.insertar(encabezadoColumna)
            encabezadoColumna.acceso = nuevo
        else: 
            if int(nuevo.fila) < int(encabezadoColumna.acceso.fila): #INSERTAR AL INICIO
                nuevo.abajo = encabezadoColumna.acceso
                encabezadoColumna.acceso.arriba = nuevo
                encabezadoColumna.acceso = nuevo
            else:
                temporal = encabezadoColumna.acceso
                while temporal.abajo != None:
                    if int(nuevo.fila) < int(temporal.abajo.fila): # INSERTAR EN MEDIO
                        nuevo.abajo = temporal.abajo
                        temporal.abajo.arriba = nuevo
                        nuevo.arriba = temporal
                        temporal.abajo = nuevo
                        break
                    temporal = temporal.abajo
                if temporal.abajo == None: #INSERTAR AL FINAL
                    temporal.abajo = nuevo
                    nuevo.arriba = temporal
    # metodo recorrer filas 
    def recorrerFilas(self):
        encabezadoFila = self.eFilas.inicio
        print('Recorrido por filas')
        while(encabezadoFila != None):
            temporal = encabezadoFila.acceso
            while(temporal != None):
                print(temporal.dato)
                if encabezadoFila.siguiente != None or temporal.derecha != None:
                    print('->')
                temporal = temporal.siguiente
            encabezadoFila = encabezadoFila.siguiente
        print('Fin filas')
    
    # metodo recorrer columnas  
    def recorrerColumnas(self):
        encabezadoColumna = self.eColumnas.inicio
        print('Recorrido por columnas')
        while encabezadoColumna != None:
            temporal = encabezadoColumna.acceso
            while temporal != None:
                print(temporal.dato)
                if encabezadoColumna.siguiente !=None or temporal.abajo != None:
                    print('->')
                temporal = temporal.siguiente
            encabezadoColumna = encabezadoColumna.siguiente
        print('Fin columnas')