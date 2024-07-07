import pygame  # Importa la biblioteca Pygame para gráficos y eventos
import math  # Importa la biblioteca Math para operaciones matemáticas (aunque no se usa en este código)
from queue import PriorityQueue  # Importa PriorityQueue para la cola de prioridad en el algoritmo A*

# Dimensiones de la ventana
ANCHO = 800
VENTANA = pygame.display.set_mode((ANCHO, ANCHO))  # Crea una ventana de Pygame con tamaño ANCHO x ANCHO
pygame.display.set_caption("Algoritmo de Búsqueda A*")  # Establece el título de la ventana

# Definición de colores en formato RGB
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 255, 0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
PURPURA = (128, 0, 128)
NARANJA = (255, 165, 0)
GRIS = (128, 128, 128)
TURQUESA = (64, 224, 208)

class Celda:
    # Constructor de la clase Celda, que representa una celda en la cuadrícula
    def __init__(self, fila, columna, ancho, total_filas):
        self.fila = fila  # Fila de la celda
        self.columna = columna  # Columna de la celda
        self.x = fila * ancho  # Coordenada x de la celda en la ventana
        self.y = columna * ancho  # Coordenada y de la celda en la ventana
        self.color = BLANCO  # Color inicial de la celda (blanco)
        self.vecinos = []  # Lista de vecinos de la celda
        self.ancho = ancho  # Ancho de la celda
        self.total_filas = total_filas  # Número total de filas en la cuadrícula

    def obtener_pos(self):
        return self.fila, self.columna  # Devuelve la posición de la celda (fila, columna)

    def esta_cerrado(self):
        return self.color == ROJO  # Comprueba si la celda está cerrada (rojo)

    def esta_abierto(self):
        return self.color == VERDE  # Comprueba si la celda está abierta (verde)

    def es_barrera(self):
        return self.color == NEGRO  # Comprueba si la celda es una barrera (negro)

    def es_inicio(self):
        return self.color == NARANJA  # Comprueba si la celda es el punto de inicio (naranja)

    def es_final(self):
        return self.color == TURQUESA  # Comprueba si la celda es el punto final (turquesa)

    def reiniciar(self):
        self.color = BLANCO  # Restablece el color de la celda a blanco

    def hacer_inicio(self):
        self.color = NARANJA  # Marca la celda como el punto de inicio (naranja)

    def hacer_cerrado(self):
        self.color = ROJO  # Marca la celda como cerrada (rojo)

    def hacer_abierto(self):
        self.color = VERDE  # Marca la celda como abierta (verde)

    def hacer_barrera(self):
        self.color = NEGRO  # Marca la celda como una barrera (negro)

    def hacer_final(self):
        self.color = TURQUESA  # Marca la celda como el punto final (turquesa)

    def hacer_camino(self):
        self.color = PURPURA  # Marca la celda como parte del camino (púrpura)

    def dibujar(self, ventana):
        # Dibuja la celda en la ventana
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizar_vecinos(self, cuadricula):
        # Actualiza la lista de vecinos de la celda que no son barreras
        self.vecinos = []
        if self.fila < self.total_filas - 1 and not cuadricula[self.fila + 1][self.columna].es_barrera():  # Abajo
            self.vecinos.append(cuadricula[self.fila + 1][self.columna])

        if self.fila > 0 and not cuadricula[self.fila - 1][self.columna].es_barrera():  # Arriba
            self.vecinos.append(cuadricula[self.fila - 1][self.columna])

        if self.columna < self.total_filas - 1 and not cuadricula[self.fila][self.columna + 1].es_barrera():  # Derecha
            self.vecinos.append(cuadricula[self.fila][self.columna + 1])

        if self.columna > 0 and not cuadricula[self.fila][self.columna - 1].es_barrera():  # Izquierda
            self.vecinos.append(cuadricula[self.fila][self.columna - 1])

    def __lt__(self, otro):
        # Método necesario para la cola de prioridad, pero no se usa aquí
        return False

# Función heurística que calcula la distancia Manhattan entre dos puntos
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Función para reconstruir el camino desde el nodo final al nodo inicial
def reconstruir_camino(de_donde_vino, actual, dibujar):
    while actual in de_donde_vino:
        actual = de_donde_vino[actual]
        actual.hacer_camino()  # Marca las celdas del camino
        dibujar()  # Dibuja la cuadrícula

# Implementación del algoritmo A*
def algoritmo(dibujar, cuadricula, inicio, final):
    contador = 0
    conjunto_abierto = PriorityQueue()  # Cola de prioridad para nodos abiertos
    conjunto_abierto.put((0, contador, inicio))  # Añade el nodo inicial a la cola
    de_donde_vino = {}  # Diccionario para reconstruir el camino
    g_score = {celda: float("inf") for fila in cuadricula for celda in fila}  # Inicializa g_score para todos los nodos
    g_score[inicio] = 0  # g_score del nodo inicial es 0
    f_score = {celda: float("inf") for fila in cuadricula for celda in fila}  # Inicializa f_score para todos los nodos
    f_score[inicio] = h(inicio.obtener_pos(), final.obtener_pos())  # f_score del nodo inicial

    conjunto_abierto_hash = {inicio}  # Conjunto para seguimiento de nodos abiertos

    while not conjunto_abierto.empty():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()  # Maneja el evento de salida de Pygame

        actual = conjunto_abierto.get()[2]  # Obtiene el nodo con el menor f_score
        conjunto_abierto_hash.remove(actual)  # Elimina el nodo actual del conjunto de nodos abiertos

        if actual == final:  # Si el nodo actual es el final
            reconstruir_camino(de_donde_vino, final, dibujar)  # Reconstruye el camino
            final.hacer_final()  # Marca el nodo final
            return True  # Termina el algoritmo

        for vecino in actual.vecinos:  # Para cada vecino del nodo actual
            temp_g_score = g_score[actual] + 1  # Calcula el g_score temporal

            if temp_g_score < g_score[vecino]:  # Si el nuevo g_score es mejor
                de_donde_vino[vecino] = actual  # Actualiza el camino
                g_score[vecino] = temp_g_score  # Actualiza g_score
                f_score[vecino] = temp_g_score + h(vecino.obtener_pos(), final.obtener_pos())  # Actualiza f_score
                if vecino not in conjunto_abierto_hash:
                    contador += 1
                    conjunto_abierto.put((f_score[vecino], contador, vecino))  # Añade el vecino a la cola de prioridad
                    conjunto_abierto_hash.add(vecino)  # Añade el vecino al conjunto de nodos abiertos
                    vecino.hacer_abierto()  # Marca el vecino como abierto

        dibujar()  # Dibuja la cuadrícula

        if actual != inicio:
            actual.hacer_cerrado()  # Marca el nodo actual como cerrado

    return False  # Retorna False si no encuentra un camino

# Función para crear la cuadrícula
def crear_cuadricula(filas, ancho):
    cuadricula = []
    gap = ancho // filas  # Ancho de cada celda
    for i in range(filas):
        cuadricula.append([])
        for j in range(filas):
            celda = Celda(i, j, gap, filas)
            cuadricula[i].append(celda)

    return cuadricula

# Función para dibujar las líneas de la cuadrícula
def dibujar_cuadricula(ventana, filas, ancho):
    gap = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * gap), (ancho, i * gap))  # Dibuja líneas horizontales
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * gap, 0), (j * gap, ancho))  # Dibuja líneas verticales

# Función para dibujar todo en la ventana
def dibujar(ventana, cuadricula, filas, ancho):
    ventana.fill(BLANCO)  # Rellena la ventana con color blanco

    for fila in cuadricula:
        for celda in fila:
            celda.dibujar(ventana)  # Dibuja cada celda

    dibujar_cuadricula(ventana, filas, ancho)  # Dibuja las líneas de la cuadrícula
    pygame.display.update()  # Actualiza la pantalla

# Función para obtener la posición del clic en la cuadrícula
def obtener_pos_clic(pos, filas, ancho):
    gap = ancho // filas
    y, x = pos

    fila = y // gap
    columna = x // gap

    return fila, columna  # Devuelve la fila y columna del clic

# Función principal
def principal(ventana, ancho):
    FILAS = 50  # Número de filas en la cuadrícula
    cuadricula = crear_cuadricula(FILAS, ancho)  # Crea la cuadrícula

    inicio = None  # Punto de inicio
    final = None  # Punto final

    correr = True
    while correr:
        dibujar(ventana, cuadricula, FILAS, ancho)  # Dibuja la cuadrícula
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False  # Sale del bucle si se cierra la ventana

            if pygame.mouse.get_pressed()[0]:  # Si se hace clic izquierdo
                pos = pygame.mouse.get_pos()
                fila, columna = obtener_pos_clic(pos, FILAS, ancho)
                celda = cuadricula[fila][columna]
                if not inicio and celda != final:
                    inicio = celda
                    inicio.hacer_inicio()  # Marca el punto de inicio

                elif not final and celda != inicio:
                    final = celda
                    final.hacer_final()  # Marca el punto final

                elif celda != final and celda != inicio:
                    celda.hacer_barrera()  # Marca una barrera

            elif pygame.mouse.get_pressed()[2]:  # Si se hace clic derecho
                pos = pygame.mouse.get_pos()
                fila, columna = obtener_pos_clic(pos, FILAS, ancho)
                celda = cuadricula[fila][columna]
                celda.reiniciar()  # Resetea la celda
                if celda == inicio:
                    inicio = None
                elif celda == final:
                    final = None

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and inicio and final:
                    for fila in cuadricula:
                        for celda in fila:
                            celda.actualizar_vecinos(cuadricula)  # Actualiza los vecinos

                    algoritmo(lambda: dibujar(ventana, cuadricula, FILAS, ancho), cuadricula, inicio, final)  # Ejecuta A*

                if evento.key == pygame.K_c:
                    inicio = None
                    final = None
                    cuadricula = crear_cuadricula(FILAS, ancho)  # Resetea la cuadrícula

    pygame.quit()  # Cierra Pygame

principal(VENTANA, ANCHO)  # Ejecuta la función principal
