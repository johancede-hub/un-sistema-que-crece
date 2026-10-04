# ==============================================================================
# SISTEMA DE INVENTARIO Y CRAFTEO
#   Componente A: Mochila (lista enlazada) + Historial (pila) para "deshacer"
#   Componente B: Catálogo de objetos (Árbol Binario de Búsqueda)
#   Componente C: Relaciones de crafteo (Grafo con listas de adyacencia)
#   Componente D: Un contrato (IPila), dos implementaciones (arreglo y lista)
# ==============================================================================


# ==============================================================================
# MOCHILA: EL CONTRATO Y SUS DOS IMPLEMENTACIONES
# ==============================================================================

# --- EL CONTRATO (Interfaz conceptual) ---
class IMochila:
    def mostrar_inventario(self):
        pass

    def agregar_objeto(self, objeto):
        pass

    def quitar_objeto(self, objeto):
        pass

    def buscar_objeto(self, objeto):
        pass


# --- IMPLEMENTACIÓN 1: Usando Arreglo ---
class MochilaArreglo(IMochila):
    def __init__(self, capacidad=4):
        self._capacidad = capacidad
        self._mochila = [None] * capacidad

    def _existe(self, objeto):
        """Auxiliar (NUEVO): revisa si el objeto ya está, sin imprimir nada."""
        for i in range(len(self._mochila)):
            if self._mochila[i] == objeto:
                return True
        return False

    def mostrar_inventario(self):
        print("\n[Mochila de Arreglo] INVENTARIO ACTUAL")
        for i in range(len(self._mochila)):
            if self._mochila[i] is None:
                print(f"Slot [{i}]: [ VACÍO ]")
            else:
                print(f"Slot [{i}]: {self._mochila[i]}")
        print("-------------------------\n")

    def agregar_objeto(self, objeto):
        # NUEVO: control de objeto repetido
        if self._existe(objeto):
            print(f"'{objeto}' ya está en la mochila. No se permiten repetidos.")
            return False

        for i in range(len(self._mochila)):
            if self._mochila[i] is None:
                self._mochila[i] = objeto
                print(f"¡Éxito! Guardaste '{objeto}' en el slot [{i}].")
                return True

        print(f"¡Inventario lleno! No puedes guardar '{objeto}'. La mochila ha llegado a su límite de {self._capacidad} espacios.")
        return False

    def quitar_objeto(self, objeto):
        for i in range(len(self._mochila)):
            if self._mochila[i] == objeto:
                self._mochila[i] = None
                print(f"¡Objeto retirado! Sacaste '{objeto}' del slot [{i}].")
                return True
        print(f"El objeto '{objeto}' no se encuentra en la mochila.")
        return False

    def buscar_objeto(self, objeto):
        for i in range(len(self._mochila)):
            if self._mochila[i] == objeto:
                print(f"¡Objeto '{objeto}' encontrado en el slot [{i}]!")
                return True
        print(f"El objeto '{objeto}' no se encuentra en la mochila.")
        return False


# ==============================================================================
# COMPONENTE A: LISTA ENLAZADA SIMPLE (la mochila)
# Variante elegida: SIMPLE. Solo necesitamos avanzar hacia adelante (recorrer,
# buscar, eliminar), así que un segundo enlace por nodo (lista doble) sería
# memoria que no aprovechamos.
# ==============================================================================

class NodoObjeto:
    def __init__(self, objeto):
        self._dato = objeto       # El objeto que guardamos (ej. "Piedra")
        self._siguiente = None    # El apuntador al siguiente nodo (nace valiendo None)

    @property
    def dato(self):
        return self._dato

    @property
    def siguiente(self):
        return self._siguiente

    @siguiente.setter
    def siguiente(self, nodo):
        self._siguiente = nodo


class MochilaListaEnlazada(IMochila):

    def __init__(self):
        self._cabeza = None      # La cabeza de la lista (el inicio de la cadena)

    def _existe(self, objeto):
        """Auxiliar (NUEVO): revisa si el objeto ya está, sin imprimir nada."""
        actual = self._cabeza
        while actual is not None:
            if actual.dato == objeto:
                return True
            actual = actual.siguiente
        return False

    def agregar_objeto(self, objeto):
        # NUEVO: control de objeto repetido (clave repetida)
        if self._existe(objeto):
            print(f"'{objeto}' ya está en la mochila. No se permiten repetidos.")
            return False

        # 1. Creamos un nuevo nodo con el objeto que nos pasaron
        nuevo_nodo = NodoObjeto(objeto)

        # 2. Caso especial: si la mochila está totalmente vacía
        if self._cabeza is None:
            self._cabeza = nuevo_nodo
            print(f"¡Éxito! Guardaste '{objeto}' en la cabeza de la lista.")
            return True

        # 3. Si ya hay elementos, recorremos la cadena hasta llegar al final
        actual = self._cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente

        # 4. Cuando encontramos el último nodo, le pegamos el nuevo nodo al final
        actual.siguiente = nuevo_nodo
        print(f"¡Éxito! Guardaste '{objeto}' al final de la lista enlazada.")
        return True

    def quitar_objeto(self, objeto):
        # Caso especial 1: La mochila está vacía
        if self._cabeza is None:
            print(f"La mochila está vacía. El objeto '{objeto}' no se encuentra.")
            return False

        # Caso especial 2: El objeto está justo en la cabeza
        # (esto incluye el caso de eliminar el ÚNICO elemento: la cabeza queda en None)
        if self._cabeza.dato == objeto:
            self._cabeza = self._cabeza.siguiente
            print(f"¡Objeto retirado! Sacaste '{objeto}' de la cabeza.")
            return True

        # Caso general: Buscar en el resto de la cadena
        actual = self._cabeza
        while actual.siguiente is not None:
            if actual.siguiente.dato == objeto:
                # Saltamos el nodo que queremos borrar para "desconectarlo"
                actual.siguiente = actual.siguiente.siguiente
                print(f"¡Objeto retirado! Sacaste '{objeto}'.")
                return True
            actual = actual.siguiente

        # Si recorrimos todo y no estaba
        print(f"El objeto '{objeto}' no se encuentra en la mochila.")
        return False

    def buscar_objeto(self, objeto):
        actual = self._cabeza
        posicion = 0
        while actual is not None:
            if actual.dato == objeto:
                print(f"¡Objeto '{objeto}' ENCONTRADO en el nodo/posición [{posicion}]!")
                return True
            actual = actual.siguiente
            posicion += 1
        print(f"El objeto '{objeto}' NO se encuentra en la mochila.")
        return False

    def mostrar_inventario(self):
        print("\n[Mochila de Lista Enlazada] INVENTARIO ACTUAL")

        if self._cabeza is None:
            print("El inventario está completamente [ VACÍO ]")
            print("-----------------------------------------\n")
            return

        actual = self._cabeza
        contador = 0
        while actual is not None:
            print(f"Slot/Nodo [{contador}]: {actual.dato}")
            actual = actual.siguiente
            contador += 1

        print("-----------------------------------------\n")


# ==============================================================================
# COMPONENTE D: CONTRATO DE LA PILA (un contrato, dos implementaciones)
# La pila sirve para "deshacer": lo ÚLTIMO que hiciste es lo PRIMERO que se
# revierte (LIFO). Una cola sacaría lo más antiguo, y eso no sirve para deshacer.
# ==============================================================================

class IPila:
    def apilar(self, objeto):
        pass

    def desapilar(self):
        pass

    def ver_cima(self):
        pass

    def esta_vacia(self):
        pass


# --- IMPLEMENTACIÓN 1 DE LA PILA: Usando Arreglo Estático ---
class PilaArreglo(IPila):
    def __init__(self, capacidad=5):
        self._capacidad = capacidad
        self._elementos = [None] * capacidad
        self._cima = -1  # Índice que marca el tope de la pila (-1 significa vacía)

    def apilar(self, objeto):
        if self._cima >= self._capacidad - 1:
            print("[Pila Arreglo] ¡Desbordamiento! La pila está llena.")
            return False
        self._cima += 1
        self._elementos[self._cima] = objeto
        print(f"[Pila Arreglo] Acción apilada: {objeto}")
        return True

    def desapilar(self):
        if self.esta_vacia():
            print("[Pila Arreglo] La pila está vacía. No hay acciones que deshacer.")
            return None
        objeto = self._elementos[self._cima]
        self._elementos[self._cima] = None
        self._cima -= 1
        print(f"[Pila Arreglo] Acción sacada del historial: {objeto}")
        return objeto

    def ver_cima(self):
        if self.esta_vacia():
            return None
        return self._elementos[self._cima]

    def esta_vacia(self):
        return self._cima == -1


# --- IMPLEMENTACIÓN 2 DE LA PILA: Usando Lista Enlazada ---
class NodoPila:
    def __init__(self, objeto):
        self._dato = objeto
        self._siguiente = None

    @property
    def dato(self):
        return self._dato

    @property
    def siguiente(self):
        return self._siguiente

    @siguiente.setter
    def siguiente(self, nodo):
        self._siguiente = nodo


class PilaListaEnlazada(IPila):
    def __init__(self):
        self._cima = None  # Apunta al nodo que está en el tope

    def apilar(self, objeto):
        nuevo_nodo = NodoPila(objeto)
        nuevo_nodo.siguiente = self._cima   # 1) el nuevo apunta a la cima actual
        self._cima = nuevo_nodo             # 2) la cima ahora es el nuevo
        print(f"[Pila Lista Enlazada] Acción apilada: {objeto}")
        return True

    def desapilar(self):
        if self.esta_vacia():
            print("[Pila Lista Enlazada] La pila está vacía. No hay acciones que deshacer.")
            return None
        objeto_removido = self._cima.dato
        self._cima = self._cima.siguiente  # La cima baja al siguiente nodo
        print(f"[Pila Lista Enlazada] Acción sacada del historial: {objeto_removido}")
        return objeto_removido

    def ver_cima(self):
        if self.esta_vacia():
            return None
        return self._cima.dato

    def esta_vacia(self):
        return self._cima is None


# ==============================================================================
# COMPONENTE B: ÍNDICE DE BÚSQUEDA (ÁRBOL BINARIO DE BÚSQUEDA - ABB)
# ==============================================================================

class NodoArbol:
    """Nodo para el Árbol Binario de Búsqueda."""
    def __init__(self, clave, nombre_objeto):
        self._clave = clave                # ID numérico único del objeto (Ej: 101)
        self._nombre = nombre_objeto       # Nombre del objeto (Ej: "Palo")
        self._izquierda = None             # Subárbol izquierdo
        self._derecha = None               # Subárbol derecho

    @property
    def clave(self):
        return self._clave

    @property
    def nombre(self):
        return self._nombre

    @property
    def izquierda(self):
        return self._izquierda

    @izquierda.setter
    def izquierda(self, nodo):
        self._izquierda = nodo

    @property
    def derecha(self):
        return self._derecha

    @derecha.setter
    def derecha(self, nodo):
        self._derecha = nodo


class ArbolBinarioBusqueda:
    """Catálogo de Objetos usando un Árbol Binario de Búsqueda (ABB)."""
    def __init__(self):
        self._raiz = None

    def insertar(self, clave, nombre_objeto):
        self._raiz = self._insertar_recursivo(self._raiz, clave, nombre_objeto)

    def _insertar_recursivo(self, actual, clave, nombre_objeto):
        if actual is None:   # CASO BASE: encontramos el hueco
            print(f"[ABB] Objeto '{nombre_objeto}' registrado con ID [{clave}].")
            return NodoArbol(clave, nombre_objeto)

        if clave < actual.clave:
            actual.izquierda = self._insertar_recursivo(actual.izquierda, clave, nombre_objeto)
        elif clave > actual.clave:
            actual.derecha = self._insertar_recursivo(actual.derecha, clave, nombre_objeto)
        else:
            print(f"[ABB Error] La clave/ID {clave} ya existe ({actual.nombre}). No se permiten claves duplicadas.")
        return actual

    def buscar(self, clave):
        return self._buscar_recursivo(self._raiz, clave)

    def _buscar_recursivo(self, actual, clave):
        if actual is None:           # CASO BASE 1: no existe
            return None
        if clave == actual.clave:    # CASO BASE 2: lo encontramos
            return actual
        if clave < actual.clave:     # Divide y vencerás: descartamos la mitad derecha
            return self._buscar_recursivo(actual.izquierda, clave)
        return self._buscar_recursivo(actual.derecha, clave)  # descartamos la izquierda

    # --- RECORRIDOS RECURSIVOS ---

    def inorden(self):
        """Imprime el listado ordenado del catálogo por ID."""
        print("\n--- CATÁLOGO ORDENADO (Recorrido Inorden) ---")
        if self._raiz is None:   # NUEVO: caso límite, árbol vacío
            print("  (el catálogo está vacío)")
        else:
            self._inorden_recursivo(self._raiz)
        print("---------------------------------------------")

    def _inorden_recursivo(self, actual):
        if actual is not None:   # si es None, es el caso base: no hace nada
            self._inorden_recursivo(actual.izquierda)
            print(f"  ID: [{actual.clave}] -> Objeto: {actual.nombre}")
            self._inorden_recursivo(actual.derecha)

    def preorden(self):
        print("\n--- RECORRIDO PREORDEN ---")
        self._preorden_recursivo(self._raiz)
        print("--------------------------")

    def _preorden_recursivo(self, actual):
        if actual is not None:
            print(f"  ID: [{actual.clave}] -> Objeto: {actual.nombre}")
            self._preorden_recursivo(actual.izquierda)
            self._preorden_recursivo(actual.derecha)

    def postorden(self):
        print("\n--- RECORRIDO POSTORDEN ---")
        self._postorden_recursivo(self._raiz)
        print("---------------------------")

    def _postorden_recursivo(self, actual):
        if actual is not None:
            self._postorden_recursivo(actual.izquierda)
            self._postorden_recursivo(actual.derecha)
            print(f"  ID: [{actual.clave}] -> Objeto: {actual.nombre}")

    # --- MÉTODO PARA EL EXPERIMENTO DE ALTURAS ---

    def calcular_altura(self):
        """Calcula la altura máxima del árbol recursivamente."""
        return self._calcular_altura_recursiva(self._raiz)

    def _calcular_altura_recursiva(self, actual):
        if actual is None:
            return 0
        altura_izq = self._calcular_altura_recursiva(actual.izquierda)
        altura_der = self._calcular_altura_recursiva(actual.derecha)
        return 1 + max(altura_izq, altura_der)


# ==============================================================================
# COMPONENTE C: RELACIONES (GRAFO CON LISTAS DE ADYACENCIA)
# CAMBIO: antes se usaba un diccionario y listas de Python. Como el enunciado
# pide estructuras propias, ahora cada objeto (vértice) guarda su lista de
# vecinos como una LISTA ENLAZADA hecha por nosotros.
# ==============================================================================

class NodoVecino:
    """Un nodo de la lista de adyacencia: guarda el nombre de un vecino."""
    def __init__(self, nombre):
        self._nombre = nombre
        self._siguiente = None

    @property
    def nombre(self):
        return self._nombre

    @property
    def siguiente(self):
        return self._siguiente

    @siguiente.setter
    def siguiente(self, nodo):
        self._siguiente = nodo


class ListaVecinos:
    """Lista enlazada con los vecinos de UN objeto."""
    def __init__(self):
        self._cabeza = None
        self._tamano = 0

    def existe(self, nombre):
        actual = self._cabeza
        while actual is not None:
            if actual.nombre == nombre:
                return True
            actual = actual.siguiente
        return False

    def agregar(self, nombre):
        """Agrega al final. Devuelve False si ya estaba (evita aristas repetidas)."""
        if self.existe(nombre):
            return False
        nuevo = NodoVecino(nombre)
        if self._cabeza is None:
            self._cabeza = nuevo
        else:
            actual = self._cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._tamano += 1
        return True

    def cantidad(self):
        return self._tamano

    def copiar_a_lista(self):
        """Devuelve una COPIA para mostrar (así nadie modifica la lista interna)."""
        resultado = []
        actual = self._cabeza
        while actual is not None:
            resultado.append(actual.nombre)
            actual = actual.siguiente
        return resultado


class NodoVertice:
    """Un objeto del grafo, con su lista de vecinos."""
    def __init__(self, nombre):
        self._nombre = nombre
        self._vecinos = ListaVecinos()
        self._siguiente = None   # los vértices también forman una lista enlazada

    @property
    def nombre(self):
        return self._nombre

    @property
    def vecinos(self):
        return self._vecinos

    @property
    def siguiente(self):
        return self._siguiente

    @siguiente.setter
    def siguiente(self, nodo):
        self._siguiente = nodo


class Grafo:
    """
    Representa relaciones no jerárquicas entre objetos (Recetas de Crafteo)
    usando Listas de Adyacencia.
    """
    def __init__(self):
        self._cabeza = None   # lista enlazada de vértices

    def _buscar_vertice(self, nombre):
        actual = self._cabeza
        while actual is not None:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None

    def agregar_vertice(self, nombre):
        if self._buscar_vertice(nombre) is not None:
            return
        nuevo = NodoVertice(nombre)
        nuevo.siguiente = self._cabeza   # se inserta al inicio de la lista de vértices
        self._cabeza = nuevo

    def agregar_arista(self, objeto1, objeto2):
        """Crea una combinación bidireccional (Grafo no dirigido)."""
        if objeto1 == objeto2:
            print("[Grafo] Un objeto no se puede combinar consigo mismo.")
            return False
        self.agregar_vertice(objeto1)
        self.agregar_vertice(objeto2)
        v1 = self._buscar_vertice(objeto1)
        v2 = self._buscar_vertice(objeto2)
        nueva = v1.vecinos.agregar(objeto2)
        v2.vecinos.agregar(objeto1)
        if not nueva:
            print(f"[Grafo] La combinación {objeto1}-{objeto2} ya existía.")
        return nueva

    # Consulta 1: Listar vecinos (Objetos combinables directamente)
    def listar_vecinos(self, objeto):
        vertice = self._buscar_vertice(objeto)
        if vertice is None:
            print(f"[Grafo] El objeto '{objeto}' no existe en la red de crafteo.")
            return []
        return vertice.vecinos.copiar_a_lista()

    # Consulta 2: Grado (cuántas combinaciones directas tiene un objeto)
    def grado(self, objeto):
        vertice = self._buscar_vertice(objeto)
        if vertice is None:
            print(f"[Grafo] El objeto '{objeto}' no existe en la red de crafteo.")
            return 0
        return vertice.vecinos.cantidad()

    # Consulta 3: Verificar si dos objetos están conectados directamente
    def estan_conectados(self, objeto1, objeto2):
        vertice = self._buscar_vertice(objeto1)
        if vertice is None:
            return False
        return vertice.vecinos.existe(objeto2)


# ==============================================================================
# NUEVO: INVENTARIO = une mochila + historial (pila) + catálogo (ABB)
# Aquí se conectan los componentes. Recibe CUALQUIER mochila y CUALQUIER pila:
# por eso se puede cambiar la implementación sin tocar nada más.
# ==============================================================================

class Accion:
    """Una acción guardada en el historial (para poder deshacerla)."""
    def __init__(self, tipo, objeto):
        self._tipo = tipo        # "agregar" o "quitar"
        self._objeto = objeto

    @property
    def tipo(self):
        return self._tipo

    @property
    def objeto(self):
        return self._objeto

    def __str__(self):
        return f"{self._tipo} '{self._objeto}'"


class Inventario:
    def __init__(self, mochila, historial):
        self._mochila = mochila          # IMochila (arreglo o lista)
        self._historial = historial      # IPila (arreglo o lista)
        self._catalogo = ArbolBinarioBusqueda()

    def registrar_en_catalogo(self, clave, nombre):
        self._catalogo.insertar(clave, nombre)

    def listar_catalogo(self):
        self._catalogo.inorden()

    def agregar(self, clave):
        """Busca el ID en el catálogo (ABB) y guarda el objeto en la mochila."""
        nodo = self._catalogo.buscar(clave)
        if nodo is None:
            print(f"[Inventario] El ID {clave} no existe en el catálogo.")
            return False
        if self._mochila.agregar_objeto(nodo.nombre):
            if not self._historial.apilar(Accion("agregar", nodo.nombre)):
                print("   (Aviso: historial lleno, esta acción no se podrá deshacer)")
            return True
        return False

    def quitar(self, clave):
        nodo = self._catalogo.buscar(clave)
        if nodo is None:
            print(f"[Inventario] El ID {clave} no existe en el catálogo.")
            return False
        if self._mochila.quitar_objeto(nodo.nombre):
            if not self._historial.apilar(Accion("quitar", nodo.nombre)):
                print("   (Aviso: historial lleno, esta acción no se podrá deshacer)")
            return True
        return False

    def buscar(self, clave):
        """Busca el ID en el catálogo (ABB) y luego revisa si está en la mochila."""
        nodo = self._catalogo.buscar(clave)
        if nodo is None:
            print(f"[Inventario] El ID {clave} no existe en el catálogo.")
            return False
        return self._mochila.buscar_objeto(nodo.nombre)

    def deshacer(self):
        """Saca la última acción de la pila y hace lo contrario."""
        accion = self._historial.desapilar()
        if accion is None:
            return False
        if accion.tipo == "agregar":
            self._mochila.quitar_objeto(accion.objeto)
        else:
            self._mochila.agregar_objeto(accion.objeto)
        return True

    def mostrar(self):
        self._mochila.mostrar_inventario()


# ==============================================================================
# DEMOSTRACIÓN DEL INVENTARIO (se usa con cualquier mochila y cualquier pila)
# ==============================================================================

def probar_inventario(mochila, historial):
    print(f"Mochila: {mochila.__class__.__name__} | Historial: {historial.__class__.__name__}")
    inv = Inventario(mochila, historial)

    inv.registrar_en_catalogo(30, "Piedra")
    inv.registrar_en_catalogo(10, "Palo")
    inv.registrar_en_catalogo(50, "Hierro")
    inv.registrar_en_catalogo(20, "Pluma")

    print("\n-- Funcionamiento normal --")
    inv.agregar(30)
    inv.agregar(10)
    inv.agregar(50)
    inv.mostrar()

    print("-- Buscar un objeto que SÍ está y uno que NO está en la mochila --")
    inv.buscar(10)
    inv.buscar(20)

    inv.quitar(10)
    inv.mostrar()
    print("-- Deshacer la última acción (volver a guardar el Palo) --")
    inv.deshacer()
    inv.mostrar()

    print("-- [Caso Límite] Quitar un objeto que no está en la mochila: --")
    inv.quitar(20)

    print("-- [Caso Límite] Objeto repetido en la mochila: --")
    inv.agregar(30)

    print("-- [Caso Límite] ID que no existe en el catálogo: --")
    inv.agregar(999)

    print("-- [Caso Límite] Quitar vaciando la mochila (incluye el único elemento): --")
    inv.quitar(30)
    inv.quitar(10)
    inv.quitar(50)
    inv.mostrar()

    print("-- [Caso Límite] Quitar en mochila vacía: --")
    inv.quitar(50)

    print("-- [Caso Límite] Deshacer hasta que el historial quede vacío: --")
    while inv.deshacer():
        pass
    inv.deshacer()   # historial vacío


# ==============================================================================
# PRUEBA Y DEMOSTRACIÓN GENERAL DEL SISTEMA (MAIN)
# ==============================================================================

if __name__ == "__main__":
    print("======================================================================")
    print("      DEMOSTRACIÓN DEL SISTEMA DE INVENTARIO Y CRAFTEO")
    print("======================================================================")

    # --------------------------------------------------------------------------
    # 1. COMPONENTE D: UN CONTRATO, DOS IMPLEMENTACIONES
    # --------------------------------------------------------------------------
    print("\n>>> 1. PRUEBA DE LA PILA (Un contrato, dos implementaciones)")

    # >>> ÚNICA LÍNEA QUE CAMBIA para usar la otra implementación <<<
    pila_historial = PilaListaEnlazada()      # o: PilaArreglo(capacidad=5)

    print(f"Usando implementación: {pila_historial.__class__.__name__}")
    pila_historial.apilar("Guardó Piedra")
    pila_historial.apilar("Guardó Palo")
    pila_historial.desapilar()
    pila_historial.desapilar()

    print("--- [Caso Límite] Desapilar en pila vacía: ---")
    pila_historial.desapilar()

    print("--- [Caso Límite] Pila de arreglo llena (capacidad 2): ---")
    pila_pequena = PilaArreglo(capacidad=2)
    pila_pequena.apilar("Acción 1")
    pila_pequena.apilar("Acción 2")
    pila_pequena.apilar("Acción 3")   # desbordamiento

    # --------------------------------------------------------------------------
    # 2. COMPONENTES A, B y D JUNTOS: INVENTARIO CON MOCHILA, CATÁLOGO E HISTORIAL
    # --------------------------------------------------------------------------
    print("\n>>> 2. INVENTARIO: mochila de LISTA + historial de LISTA")
    probar_inventario(MochilaListaEnlazada(), PilaListaEnlazada())

    print("\n>>> 2b. MISMO PROGRAMA con ARREGLOS (mochila y pila)")
    probar_inventario(MochilaArreglo(capacidad=4), PilaArreglo(capacidad=10))

    print("\n>>> 2c. [Caso Límite] MOCHILA DE ARREGLO LLENA (capacidad 2)")
    inv_pequeno = Inventario(MochilaArreglo(capacidad=2), PilaArreglo(capacidad=10))
    inv_pequeno.registrar_en_catalogo(30, "Piedra")
    inv_pequeno.registrar_en_catalogo(10, "Palo")
    inv_pequeno.registrar_en_catalogo(50, "Hierro")
    inv_pequeno.agregar(30)
    inv_pequeno.agregar(10)
    inv_pequeno.agregar(50)   # no cabe: inventario lleno
    inv_pequeno.mostrar()

    # --------------------------------------------------------------------------
    # 3. DEMOSTRACIÓN DEL GRAFO (COMPONENTE C)
    # --------------------------------------------------------------------------
    print("\n>>> 3. PRUEBA DEL GRAFO (Relaciones de Crafteo entre Objetos)")
    crafteo = Grafo()

    crafteo.agregar_arista("Piedra", "Palo")     # Piedra + Palo = Antorcha
    crafteo.agregar_arista("Piedra", "Hierro")   # Piedra + Hierro = Hacha
    crafteo.agregar_arista("Palo", "Pluma")      # Palo + Pluma = Flecha

    print("Vecinos/Combinaciones posibles con 'Piedra':", crafteo.listar_vecinos("Piedra"))
    print("Grado de 'Piedra':", crafteo.grado("Piedra"))
    print("¿Están conectados 'Piedra' y 'Hierro'?:", crafteo.estan_conectados("Piedra", "Hierro"))
    print("¿Están conectados 'Piedra' y 'Pluma'?:", crafteo.estan_conectados("Piedra", "Pluma"))
    print("--- [Caso Límite] Objeto que no existe y arista repetida: ---")
    crafteo.listar_vecinos("Diamante")
    crafteo.agregar_arista("Piedra", "Palo")

    # --------------------------------------------------------------------------
    # 4. ÁRBOL: BÚSQUEDA, RECORRIDOS Y EXPERIMENTO DE ALTURAS
    # --------------------------------------------------------------------------
    print("\n======================================================================")
    print("      EXPERIMENTO DEL ÁRBOL (15 CLAVES)")
    print("======================================================================")

    # CAMBIO: el orden anterior formaba un árbol perfecto. Este está más mezclado.
    claves_desordenadas = [40, 15, 70, 5, 55, 90, 25, 10, 62, 80, 33, 48, 100, 3, 20]
    claves_ordenadas    = [3, 5, 10, 15, 20, 25, 33, 40, 48, 55, 62, 70, 80, 90, 100]

    arbol_desordenado = ArbolBinarioBusqueda()
    for clave in claves_desordenadas:
        arbol_desordenado.insertar(clave, f"Item_{clave}")

    arbol_ordenado = ArbolBinarioBusqueda()
    for clave in claves_ordenadas:
        arbol_ordenado.insertar(clave, f"Item_{clave}")

    print("\n--- [Caso Límite] Insertar clave duplicada (40): ---")
    arbol_desordenado.insertar(40, "Item_Duplicado")

    print("\n--- [Caso Límite] Buscar clave que existe y una que no: ---")
    encontrado = arbol_desordenado.buscar(33)
    print("Buscar 33:", encontrado.nombre if encontrado else "No existe")
    encontrado = arbol_desordenado.buscar(999)
    print("Buscar 999:", encontrado.nombre if encontrado else "No existe")

    print("\n--- [Caso Límite] Recorrer un árbol vacío: ---")
    ArbolBinarioBusqueda().inorden()

    arbol_desordenado.inorden()
    arbol_desordenado.preorden()
    arbol_desordenado.postorden()

    altura_desorden = arbol_desordenado.calcular_altura()
    altura_orden = arbol_ordenado.calcular_altura()

    print("\n======================================================================")
    print("            TABLA RESULTADO DEL EXPERIMENTO DE ALTURAS")
    print("======================================================================")
    print("| Condición de Inserción | Cantidad Datos | Altura Obtenida |")
    print("|------------------------|----------------|-----------------|")
    print(f"| Claves en Desorden     |       15       |       {altura_desorden:<2}        |")
    print(f"| Claves Ordenadas       |       15       |       {altura_orden:<2}        |")
    print("======================================================================\n")
