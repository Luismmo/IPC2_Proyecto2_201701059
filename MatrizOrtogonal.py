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
    def __init__(self, id):
        self.id = id
        self.siguiente = None
        self.anterior = None
        #acceso es un puntero al Nodo
        self.acceso = None

class ListaEncabazado(object):
    def __init__(self):
        self.inicio = None
        self.tamanio = 0

    #metodo insertar nuevo nodo clase Encabezado
    def insertar(self, dato):
        nuevo = Encabezado(dato)
        if self.inicio is None: #insertar cuando está VACÍO
            self.inicio = nuevo
            #self.inicio.siguiente = self.inicio
            #self.tamanio+=1
        else:            
            if nuevo.id < self.inicio.id: # insertar al INICIO
                nuevo.siguiente = self.inicio
                self.inicio.anterior = nuevo
                self.inicio = nuevo
            else:
                temporal = self.inicio
                while temporal.siguiente != None:
                    if nuevo.id < temporal.siguiente.id: # insertar en MEDIO
                        nuevo.siguiente = temporal.siguiente
                        temporal.siguiente.anterior = nuevo
                        nuevo.anterior = temporal
                        break
                    temporal = temporal.siguiente
                
                if temporal.siguiente == None: # insertar al FINAL
                    temporal.siguiente = nuevo
                    nuevo.anterior = temporal
                
    #metodo obtener en tal posicion
    def retornarEn(self, id):
        temporal = self.inicio        
        while temporal != None:
            if temporal.id == id:
                return temporal
            temporal = temporal.siguiente
        
        return None

class Matriz(object):
    def __init__(self):
        self.eFilas = ListaEncabazado()
        self.eColumnas = ListaEncabazado()

    # metodo insertar
    def insertar(self, dato, fila, columna):
        nuevo = Nodo(dato,fila,columna)
        #inserción de filas
        encabezadoFila = self.eFilas.retornarEn(fila)
        if encabezadoFila == None: #INSERCION SI NO EXISTE NINGUN ENCABEZADO
            encabezadoFila = Encabezado(fila)
            self.eFilas.insertar(encabezadoFila)
            encabezadoFila.acceso = nuevo
        else: 
            #insercion al inicio 
            if nuevo.columna < encabezadoFila.acceso.columna:
                nuevo.derecha = encabezadoFila.acceso
                encabezadoFila.acceso.izquierda = nuevo
                encabezadoFila.acceso = nuevo
            else:
                temporal = encabezadoFila.acceso
                while temporal.derecha !=None:

    # metodo recorrer filas 

    # metodo recorrer columnas  