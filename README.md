# Sistema de Inventario y Crafteo

**Estructura de datos | Actividad evaluativa final: "Un sistema que crece"**
**Autor:** Johan Sebastian Cedeño
**Lenguaje:** Python 3

---

## 1. El caso (explicado sin tecnicismos)

Es el inventario de un videojuego. El jugador lleva una **mochila** donde guarda objetos (Piedra, Palo, Hierro, Pluma). Todos los objetos que existen en el juego están registrados en un **catálogo**, y cada uno tiene un número de identificación (ID).

El sistema permite:

- **Guardar y sacar** objetos de la mochila, buscar si un objeto está en ella y ver su contenido.
- **Deshacer** la última acción (si sacaste algo por error, vuelve a la mochila).
- **Consultar el catálogo** ordenado por ID y encontrar un objeto rápidamente a partir de su ID.
- **Saber qué objetos se pueden combinar** entre sí (crafteo): por ejemplo, Piedra + Palo.

## 2. Estructuras usadas y por qué

Todas las estructuras son de implementación propia (no se usan `LinkedList`, `deque`, etc.).

| Componente | Estructura | Para qué se usa | Por qué esa estructura |
|---|---|---|---|
| A | **Lista enlazada simple** (`MochilaListaEnlazada`) | Guardar los objetos de la mochila | Solo se necesita avanzar hacia adelante (recorrer, buscar, eliminar). La lista doble gastaría un enlace extra por nodo sin necesidad. No tiene límite fijo de espacios. |
| A | **Pila** (`PilaListaEnlazada`) | Historial para deshacer | Lo último que se hizo es lo primero que se deshace (LIFO). Una cola sacaría lo más antiguo, que no sirve para deshacer. |
| B | **Árbol binario de búsqueda** (`ArbolBinarioBusqueda`) | Catálogo de objetos por ID | Permite buscar por clave descartando la mitad de los datos en cada paso, y el recorrido inorden entrega el listado ordenado. |
| C | **Grafo con listas de adyacencia** (`Grafo`) | Relaciones de crafteo | La relación "se pueden combinar" no es jerárquica: un objeto puede combinarse con varios y va en ambos sentidos. Las listas de adyacencia guardan solo las conexiones que existen. |
| D | **Un contrato, dos implementaciones** (`IPila`) | Pila con arreglo y pila con lista enlazada | Permite cambiar la implementación sin modificar el resto del programa. |

### Cómo se conectan

La clase `Inventario` une los componentes:

1. Al **agregar** un objeto por ID, busca el ID en el catálogo (árbol), guarda el nombre en la mochila (lista) y apila la acción en el historial (pila).
2. Al **deshacer**, desapila la última acción y hace lo contrario.
3. El grafo usa los mismos objetos del inventario.

## 3. Estructura del código

El archivo `sistema_inventario.py` sigue este orden:

1. `IMochila`: contrato de la mochila (mostrar, agregar, quitar, buscar)
2. `MochilaArreglo`: mochila con arreglo de tamaño fijo
3. `NodoObjeto` y `MochilaListaEnlazada`: mochila con lista enlazada
4. `IPila`: contrato de la pila (apilar, desapilar, ver cima, está vacía)
5. `PilaArreglo`: pila con arreglo de tamaño fijo
6. `NodoPila` y `PilaListaEnlazada`: pila con lista enlazada
7. `NodoArbol` y `ArbolBinarioBusqueda`: catálogo (inserción, búsqueda, preorden, inorden, postorden y altura, todos recursivos)
8. `NodoVecino`, `ListaVecinos`, `NodoVertice` y `Grafo`: relaciones de crafteo
9. `Accion` e `Inventario`: unen todos los componentes
10. `main`: demostración

Los atributos de todas las clases son privados (guion bajo) y se acceden mediante métodos o `@property`.

## 4. Cómo ejecutarlo

Requiere Python 3. No usa librerías externas.

```bash
python sistema_inventario.py
```

### Cambiar la implementación de la pila

En el bloque `main` hay una sola línea que decide qué pila se usa:

```python
pila_historial = PilaListaEnlazada()      # o: PilaArreglo(capacidad=5)
```

Además, la función `probar_inventario(mochila, historial)` ejecuta la misma demostración con lista enlazada y con arreglo, y el resultado es equivalente.

## 5. Casos especiales controlados

| Caso | Dónde se maneja |
|---|---|
| Estructura vacía | Mochila vacía, pila vacía, árbol vacío |
| Eliminar el único elemento | `quitar_objeto` de la lista enlazada |
| Clave que no existe | Búsqueda en el árbol, mochila y grafo |
| Clave repetida | Árbol (ID duplicado), mochila (objeto repetido), grafo (conexión repetida) |
| Estructura llena | Mochila de arreglo y pila de arreglo |

## 6. Experimento del árbol

Se insertaron las mismas 15 claves en dos árboles distintos y se midió la altura con un método recursivo.

| Orden de inserción | Cantidad de datos | Altura |
|---|---|---|
| En desorden | 15 | 4 |
| Ordenadas de menor a mayor | 15 | 15 |

**Explicación:** el árbol binario de búsqueda no se reorganiza solo. Con datos ordenados, cada clave nueva es mayor que todas las anteriores y siempre va a la derecha, así que el árbol se convierte en una cadena, parecida a una lista enlazada. Con datos en desorden, las claves se reparten entre izquierda y derecha y el árbol queda más compacto.

**Efecto en la búsqueda:** en el árbol compacto, cada comparación descarta aproximadamente la mitad de los datos, por lo que se necesitan pocos pasos. En el árbol en cadena hay que recorrer casi todos los nodos, igual que en una lista. Un árbol AVL evita este problema porque rota los nodos al detectar un desbalance y mantiene la altura baja.

*(El dibujo a mano de las rotaciones AVL se muestra en el video.)*

## 7. Limitaciones y mejoras posibles

- **El árbol no se autobalancea.** Con datos ordenados se degrada a una cadena. Mejora: implementar un árbol AVL.
- **Agregar a la mochila recorre toda la lista** hasta llegar al final. Mejora: guardar un puntero a la cola para insertar en tiempo constante.
- **Al deshacer un "quitar", el objeto vuelve al final de la lista**, no a su posición original.
- **La pila de arreglo tiene capacidad fija**: si el historial se llena, las nuevas acciones no se pueden deshacer.
- **El grafo solo permite consultar conexiones directas.** Mejora: agregar recorridos (BFS/DFS) para saber si dos objetos se pueden obtener mediante varias combinaciones.

## 8. Video

[Pega aquí el enlace del video]

## 9. Dibujos
![AVL](dibujos/1_avl_rotaciones.png)
![ABB](dibujos/2_abb_inserciones.png)
![Lista enlazada](dibujos/3_lista_insercion_eliminacion.png)