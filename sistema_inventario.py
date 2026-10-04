# ==============================================================================
# SISTEMA DE INVENTARIO Y CRAFTEO DE VIDEOJUEGOS
# ==============================================================================

# ==============================================================================
# 1. MOCHILA (CLASE BASE / CONTRATO)
# ==============================================================================
class Mochila:
    def mostrar_inventario(self):
        pass

    def agregar_objeto(self, objeto):
        pass

    def quitar_objeto(self, objeto):
        pass

    def buscar_objeto(self, objeto):
        pass


# ==============================================================================
# 2. IMPLEMENTACIONES DE LA MOCHILA
# ==============================================================================

# --- Implementation 1: Mochila con Arreglo ---
class MochilaArreglo(Mochila):
    def __init__(self, capacidad=4):
        self.capacidad = capacidad
        self.mochila = [None] * capacidad

    def _existe(self, objeto):
        """Función auxiliar: revisa si el objeto ya está en el arreglo."""
        for i in range(len(self.mochila)):
            if self.mochila[i] == objeto:
                return True
        return False

    def mostrar_inventario(self):
        print("\n[Mochila Arreglo] INVENTARIO:")
        for i in range(len(self.mochila)):
            if self.mochila[i] is None:
                print(f"  Slot [{i}]: [ VACÍO ]")
            else:
                print(f"  Slot [{i}]: {self.mochila[i]}")

    def agregar_objeto(self, objeto):
        if self._existe(objeto):
            print(f"  [Aviso] '{objeto}' ya está en la mochila.")
            return False

        for i in range(len(self.mochila)):
            if self.mochila[i] is None:
                self.mochila[i] = objeto
                print(f"  [Éxito] Guardado '{objeto}' en slot [{i}].")
                return True

        print(f"  [Error] Mochila llena. No cabe '{objeto}'.")
        return False

    def quitar_objeto(self, objeto):
        for i in range(len(self.mochila)):
            if self.mochila[i] == objeto:
                self.mochila[i] = None
                print(f"  [Éxito] Sacado '{objeto}' del slot [{i}].")
                return True
        print(f"  [Error] '{objeto}' no está en la mochila.")
        return False

    def buscar_objeto(self, objeto):
        for i in range(len(self.mochila)):
            if self.mochila[i] == objeto:
                print(f"  [Éxito] '{objeto}' encontrado en slot [{i}].")
                return True
        print(f"  [Info] '{objeto}' no está en la mochila.")
        return False


# --- Nodo para la Lista Enlazada ---
class NodoObjeto:
    def __init__(self, objeto):
        self.dato = objeto
        self.siguiente = None


# --- Implementation 2: Mochila con Lista Enlazada ---
class MochilaListaEnlazada(Mochila):
    def __init__(self):
        self.cabeza = None

    def _existe(self, objeto):
        """Función auxiliar: revisa si el objeto ya está en los nodos."""
        actual = self.cabeza
        while actual is not None:
            if actual.dato == objeto:
                return True
            actual = actual.siguiente
        return False

    def mostrar_inventario(self):
        print("\n[Mochila Lista Enlazada] INVENTARIO:")
        if self.cabeza is None:
            print("  [ VACÍO ]")
            return
        actual = self.cabeza
        pos = 0
        while actual is not None:
            print(f"  Nodo [{pos}]: {actual.dato}")
            actual = actual.siguiente
            pos += 1

    def agregar_objeto(self, objeto):
        if self._existe(objeto):
            print(f"  [Aviso] '{objeto}' ya está en la mochila.")
            return False

        nuevo = NodoObjeto(objeto)
        if self.cabeza is None:
            self.cabeza = nuevo
            print(f"  [Éxito] Guardado '{objeto}' en la cabeza.")
            return True

        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo
        print(f"  [Éxito] Guardado '{objeto}' al final.")
        return True

    def quitar_objeto(self, objeto):
        if self.cabeza is None:
            print(f"  [Error] Mochila vacía. No se encuentra '{objeto}'.")
            return False

        # Si está en la cabeza (incluye borrar el único elemento)
        if self.cabeza.dato == objeto:
            self.cabeza = self.cabeza.siguiente
            print(f"  [Éxito] Sacado '{objeto}' de la cabeza.")
            return True

        # Buscar en el resto de nodos
        actual = self.cabeza
        while actual.siguiente is not None:
            if actual.siguiente.dato == objeto:
                actual.siguiente = actual.siguiente.siguiente
                print(f"  [Éxito] Sacado '{objeto}'.")
                return True
            actual = actual.siguiente

        print(f"  [Error] '{objeto}' no está en la mochila.")
        return False

    def buscar_objeto(self, objeto):
        actual = self.cabeza
        pos = 0
        while actual is not None:
            if actual.dato == objeto:
                print(f"  [Éxito] '{objeto}' encontrado en nodo [{pos}].")
                return True
            actual = actual.siguiente
            pos += 1
        print(f"  [Info] '{objeto}' no está en la mochila.")
        return False


# ==============================================================================
# 3. PILA (CLASE BASE E IMPLEMENTACIONES PARA DESHACER)
# ==============================================================================

class Pila:
    def apilar(self, objeto):
        pass

    def desapilar(self):
        pass

    def ver_cima(self):
        pass

    def esta_vacia(self):
        pass


# --- Implementation 1: Pila en Arreglo ---
class PilaArreglo(Pila):
    def __init__(self, capacidad=5):
        self.capacidad = capacidad
        self.elementos = [None] * capacidad
        self.cima = -1

    def apilar(self, objeto):
        if self.cima >= self.capacidad - 1:
            print("  [Pila Arreglo] ¡Pila llena!")
            return False
        self.cima += 1
        self.elementos[self.cima] = objeto
        print(f"  [Pila Arreglo] Apilado: {objeto}")
        return True

    def desapilar(self):
        if self.esta_vacia():
            print("  [Pila Arreglo] Pila vacía. Nada que deshacer.")
            return None
        objeto = self.elementos[self.cima]
        self.elementos[self.cima] = None
        self.cima -= 1
        return objeto

    def ver_cima(self):
        if self.esta_vacia():
            return None
        return self.elementos[self.cima]

    def esta_vacia(self):
        return self.cima == -1


# --- Nodo para Pila en Lista ---
class NodoPila:
    def __init__(self, objeto):
        self.dato = objeto
        self.siguiente = None


# --- Implementation 2: Pila en Lista Enlazada ---
class PilaListaEnlazada(Pila):
    def __init__(self):
        self.cima = None

    def apilar(self, objeto):
        nuevo = NodoPila(objeto)
        nuevo.siguiente = self.cima
        self.cima = nuevo
        print(f"  [Pila Lista] Apilado: {objeto}")
        return True

    def desapilar(self):
        if self.esta_vacia():
            print("  [Pila Lista] Pila vacía. Nada que deshacer.")
            return None
        objeto = self.cima.dato
        self.cima = self.cima.siguiente
        return objeto

    def ver_cima(self):
        if self.esta_vacia():
            return None
        return self.cima.dato

    def esta_vacia(self):
        return self.cima is None


# ==============================================================================
# 4. ÁRBOL BINARIO DE BÚSQUEDA (CATÁLOGO POR ID)
# EXPLICACIÓN RÁPIDA PARA EL VIDEO:
# - Es una estructura jerárquica para buscar rápido por clave (ID).
# - Regla: Si la clave a insertar es MENOR va a la IZQUIERDA. Si es MAYOR va a la DERECHA.
# ==============================================================================

class NodoArbol:
    def __init__(self, clave, nombre_objeto):
        self.clave = clave
        self.nombre = nombre_objeto
        self.izquierda = None
        self.derecha = None


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, clave, nombre_objeto):
        self.raiz = self._insertar_rec(self.raiz, clave, nombre_objeto)

    def _insertar_rec(self, actual, clave, nombre_objeto):
        if actual is None:  # Encontramos la posición vacía
            return NodoArbol(clave, nombre_objeto)

        if clave < actual.clave:
            actual.izquierda = self._insertar_rec(actual.izquierda, clave, nombre_objeto)
        elif clave > actual.clave:
            actual.derecha = self._insertar_rec(actual.derecha, clave, nombre_objeto)
        else:
            print(f"  [ABB Error] La clave {clave} ya existe.")
        return actual

    def buscar(self, clave):
        return self._buscar_rec(self.raiz, clave)

    def _buscar_rec(self, actual, clave):
        if actual is None or actual.clave == clave:
            return actual
        if clave < actual.clave:
            return self._buscar_rec(actual.izquierda, clave)
        return self._buscar_rec(actual.derecha, clave)

    # Recorridos recursivos
    def inorden(self):
        """Recorre Izquierda -> Raíz -> Derecha. Entrega los datos ordenados."""
        print("\n--- CATÁLOGO ORDENADO (Inorden) ---")
        self._inorden_rec(self.raiz)

    def _inorden_rec(self, actual):
        if actual is not None:
            self._inorden_rec(actual.izquierda)
            print(f"  ID [{actual.clave}] -> Objeto: {actual.nombre}")
            self._inorden_rec(actual.derecha)

    def preorden(self):
        print("\n--- RECORRIDO PREORDEN ---")
        self._preorden_rec(self.raiz)

    def _preorden_rec(self, actual):
        if actual is not None:
            print(f"  ID [{actual.clave}] -> Objeto: {actual.nombre}")
            self._preorden_rec(actual.izquierda)
            self._preorden_rec(actual.derecha)

    def postorden(self):
        print("\n--- RECORRIDO POSTORDEN ---")
        self._postorden_rec(self.raiz)

    def _postorden_rec(self, actual):
        if actual is not None:
            self._postorden_rec(actual.izquierda)
            self._postorden_rec(actual.derecha)
            print(f"  ID [{actual.clave}] -> Objeto: {actual.nombre}")

    # Experimento de Alturas
    def calcular_altura(self):
        return self._altura_rec(self.raiz)

    def _altura_rec(self, actual):
        if actual is None:
            return 0
        return 1 + max(self._altura_rec(actual.izquierda), self._altura_rec(actual.derecha))


# ==============================================================================
# 5. GRAFO CON LISTA DE ADYACENCIA (RECETAS DE CRAFTEO)
# EXPLICACIÓN RÁPIDA PARA EL VIDEO:
# - Un Grafo no es jerárquico (no hay padre/hijo, solo conexiones directas).
# - Cada objeto es un Vértice. Sus 'vecinos' son los objetos con los que se combina.
# - Reutilizamos nuestra propia MochilaListaEnlazada para guardar esos vecinos.
# ==============================================================================

class NodoVertice:
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = MochilaListaEnlazada()  # Lista enlazada con los objetos combinables
        self.siguiente = None                  # Enlace para conectar los vértices del grafo


class Grafo:
    def __init__(self):
        self.cabeza = None  # Lista enlazada de vértices

    def _buscar_vertice(self, nombre):
        actual = self.cabeza
        while actual is not None:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None

    def agregar_vertice(self, nombre):
        if self._buscar_vertice(nombre) is None:
            nuevo = NodoVertice(nombre)
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo

    def agregar_arista(self, objeto1, objeto2):
        """Crea la combinación bidireccional (Grafo no dirigido)."""
        self.agregar_vertice(objeto1)
        self.agregar_vertice(objeto2)
        v1 = self._buscar_vertice(objeto1)
        v2 = self._buscar_vertice(objeto2)

        v1.vecinos.agregar_objeto(objeto2)
        v2.vecinos.agregar_objeto(objeto1)

    # Consulta 1: Listar vecinos (combinaciones directas)
    def listar_vecinos(self, objeto):
        vertice = self._buscar_vertice(objeto)
        if vertice is None:
            print(f"  [Grafo] '{objeto}' no existe en la red.")
            return
        print(f"\nCombinaciones de crafteo para '{objeto}':")
        vertice.vecinos.mostrar_inventario()

    # Consulta 2: Calcular grado (cuántas combinaciones tiene)
    def grado(self, objeto):
        vertice = self._buscar_vertice(objeto)
        if vertice is None:
            return 0
        actual = vertice.vecinos.cabeza
        conteo = 0
        while actual is not None:
            conteo += 1
            actual = actual.siguiente
        return conteo

    # Consulta 3: Verificar si dos objetos se pueden combinar directamente
    def estan_conectados(self, objeto1, objeto2):
        vertice = self._buscar_vertice(objeto1)
        if vertice is None:
            return False
        return vertice.vecinos._existe(objeto2)


# ==============================================================================
# PRUEBA GENERAL Y EXPERIMENTO DE ALTURAS (MAIN)
# ==============================================================================
if __name__ == "__main__":
    print("======================================================================")
    print("      DEMOSTRACIÓN DEL SISTEMA COMPLETO DE INVENTARIO Y CRAFTEO")
    print("======================================================================")

    # 1. PRUEBA DE MOCHILA Y PILA (COMPONENTE A y D)
    print("\n>>> 1. PROBANDO MOCHILA E HISTORIAL (PILA)")
    
    # ÚNICA LÍNEA QUE CAMBIA PARA EL COMPONENTE D:
    mochila = MochilaListaEnlazada()   # o: MochilaArreglo(4)
    historial = PilaListaEnlazada()     # o: PilaArreglo(5)

    mochila.agregar_objeto("Madera")
    historial.apilar("Agregar Madera")

    mochila.agregar_objeto("Hierro")
    historial.apilar("Agregar Hierro")

    mochila.mostrar_inventario()

    print("\n-- Deshaciendo última acción desde la Pila --")
    accion = historial.desapilar()
    if accion:
        mochila.quitar_objeto("Hierro")

    mochila.mostrar_inventario()

    # 2. PRUEBA DEL ÁRBOL BINARIO DE BÚSQUEDA (COMPONENTE B)
    print("\n>>> 2. PROBANDO ÁRBOL BINARIO DE BÚSQUEDA (CATÁLOGO)")
    catalogo = ArbolBinarioBusqueda()
    catalogo.insertar(30, "Madera")
    catalogo.insertar(10, "Palo")
    catalogo.insertar(50, "Hierro")

    catalogo.inorden()

    # 3. PRUEBA DEL GRAFO DE RECETAS (COMPONENTE C)
    print("\n>>> 3. PROBANDO GRAFO (RECETAS DE CRAFTEO)")
    crafteo = Grafo()
    crafteo.agregar_arista("Madera", "Palo")
    crafteo.agregar_arista("Madera", "Hierro")

    crafteo.listar_vecinos("Madera")
    print(f"\nGrado de 'Madera' (cuántos ítems se combinan con ella): {crafteo.grado('Madera')}")
    print(f"¿Están conectados 'Madera' y 'Hierro'?: {crafteo.estan_conectados('Madera', 'Hierro')}")

    # 4. EXPERIMENTO DE ALTURAS (PUNTO 3 DE LA GUÍA)
    print("\n======================================================================")
    print("      EXPERIMENTO DEL ÁRBOL (15 CLAVES)")
    print("======================================================================")

    claves_desordenadas = [40, 15, 70, 5, 55, 90, 25, 10, 62, 80, 33, 48, 100, 3, 20]
    claves_ordenadas    = [3, 5, 10, 15, 20, 25, 33, 40, 48, 55, 62, 70, 80, 90, 100]

    abb_desordenado = ArbolBinarioBusqueda()
    for c in claves_desordenadas:
        abb_desordenado.insertar(c, f"Item_{c}")

    abb_ordenado = ArbolBinarioBusqueda()
    for c in claves_ordenadas:
        abb_ordenado.insertar(c, f"Item_{c}")

    h_desorden = abb_desordenado.calcular_altura()
    h_orden = abb_ordenado.calcular_altura()

    print("\n| Condición de Inserción | Cantidad Datos | Altura Obtenida |")
    print("|------------------------|----------------|-----------------|")
    print(f"| Claves Desordenadas    |       15       |        {h_desorden}        |")
    print(f"| Claves Ordenadas       |       15       |       {h_orden}        |")
    print("======================================================================\n")