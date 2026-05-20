"""
Taller: Algoritmo de búsqueda BFS para resolución del Cubo Rubik 3x3x3
Autor: [Tu nombre]
Tema: Algoritmos de Búsqueda BFS
Descripción: Abstracción del cubo Rubik como sistema de estados y resolución
             usando BFS (Breadth-First Search / Búsqueda en Anchura).
             El cubo se representa como una matriz 12x9 desenrollada en memoria.
Nomenclatura de movimientos (según el PDF):
    - X#R / X#L : Giro horizontal de la fila # hacia la derecha / izquierda
    - Y#U / Y#D : Giro vertical de la columna # hacia arriba / abajo
    - Z#R / Z#L : Giro frontal de la capa # hacia la derecha / izquierda
"""
# -*- coding: utf-8 -*-

from collections import deque  # Cola FIFO para el BFS
import copy                     # Para copiar estados del cubo sin alterar el original

# =============================================================================
# REPRESENTACIÓN DEL CUBO
# Cada cara se identifica por su posición en la cruz 2D:
#   - UP    (U): cara superior    -> índice 0
#   - LEFT  (L): cara izquierda   -> índice 1
#   - FRONT (F): cara frontal     -> índice 2
#   - RIGHT (R): cara derecha     -> índice 3
#   - BACK  (B): cara trasera     -> índice 4
#   - DOWN  (D): cara inferior    -> índice 5
#
# Colores según el PDF: Blanco(U), Verde(L), Rojo(F), Azul(R), Naranja(B), Amarillo(D)
# =============================================================================

# Índices de las caras
U, L, F, R, B, D = 0, 1, 2, 3, 4, 5

# Color de cada cara en el estado resuelto
COLOR_NAMES = {0: 'W', 1: 'G', 2: 'R', 3: 'B', 4: 'O', 5: 'Y'}

def create_solved_cube():
    """
    Crea y retorna el estado resuelto del cubo.
    Cada cara es una lista 3x3 donde todos los elementos tienen el mismo color.
    Estado Final(f): todos los lados tienen un solo color.
    """
    cube = []
    for face_id in range(6):
        # Cada cara tiene 9 stickers (3 filas x 3 columnas) del mismo color
        face = [[face_id] * 3 for _ in range(3)]
        cube.append(face)
    return cube

def cube_to_tuple(cube):
    """
    Convierte el cubo (lista de listas) en una tupla plana inmutable.
    Necesario para usar el estado como clave en el conjunto 'visited' del BFS.
    Los estados visitados se guardan como tuplas para poder almacenarlos en sets.
    Estructura: 6 caras × 3 filas × 3 columnas = 54 enteros en la tupla.
    """
    flat = []
    for face in cube:
        for row in face:
            for cell in row:
                flat.append(cell)
    return tuple(flat)

def tuple_to_cube(t):
    """
    Convierte una tupla plana de 54 enteros de vuelta a la estructura de cubo.
    Útil para reconstruir el camino solución dentro del BFS.
    """
    cube = []
    idx = 0
    for _ in range(6):          # 6 caras
        face = []
        for _ in range(3):      # 3 filas por cara
            face.append(list(t[idx:idx+3]))
            idx += 3
        cube.append(face)
    return cube

# =============================================================================
# MOVIMIENTOS DEL CUBO
# Nomenclatura del taller:
#   X#R / X#L : fila horizontal (# = 1 abajo, 2 medio, 3 arriba)
#   Y#U / Y#D : columna vertical (# = 1 izquierda, 2 medio, 3 derecha)
#   Z#R / Z#L : capa frontal (# = 1 frente, 2 medio, 3 atrás)
# =============================================================================

def rotate_face_cw(face):
    """Rota una cara 90° en sentido horario (clockwise)."""
    return [
        [face[2][0], face[1][0], face[0][0]],
        [face[2][1], face[1][1], face[0][1]],
        [face[2][2], face[1][2], face[0][2]],
    ]

def rotate_face_ccw(face):
    """Rota una cara 90° en sentido antihorario (counter-clockwise)."""
    return [
        [face[0][2], face[1][2], face[2][2]],
        [face[0][1], face[1][1], face[2][1]],
        [face[0][0], face[1][0], face[2][0]],
    ]

# --- Movimientos X (filas horizontales) ---

def move_X1R(cube):
    """
    X1R: Gira la fila inferior (row=2) hacia la derecha.
    Afecta: cara L, F, R, B en su fila inferior.
    """
    c = copy.deepcopy(cube)
    # Guardar fila inferior de cada cara lateral
    tmp = c[L][2][:]
    c[L][2] = c[B][2][:]
    c[B][2] = c[R][2][:]
    c[R][2] = c[F][2][:]
    c[F][2] = tmp
    # La cara inferior (D) rota en sentido horario
    c[D] = rotate_face_cw(c[D])
    return c

def move_X1L(cube):
    """
    X1L: Gira la fila inferior (row=2) hacia la izquierda.
    Inverso de X1R.
    """
    c = copy.deepcopy(cube)
    tmp = c[L][2][:]
    c[L][2] = c[F][2][:]
    c[F][2] = c[R][2][:]
    c[R][2] = c[B][2][:]
    c[B][2] = tmp
    c[D] = rotate_face_ccw(c[D])
    return c

def move_X2R(cube):
    """
    X2R: Gira la fila media (row=1) hacia la derecha.
    No afecta ninguna cara completa, solo las filas medias laterales.
    """
    c = copy.deepcopy(cube)
    tmp = c[L][1][:]
    c[L][1] = c[B][1][:]
    c[B][1] = c[R][1][:]
    c[R][1] = c[F][1][:]
    c[F][1] = tmp
    return c

def move_X2L(cube):
    """X2L: Gira la fila media (row=1) hacia la izquierda. Inverso de X2R."""
    c = copy.deepcopy(cube)
    tmp = c[L][1][:]
    c[L][1] = c[F][1][:]
    c[F][1] = c[R][1][:]
    c[R][1] = c[B][1][:]
    c[B][1] = tmp
    return c

def move_X3R(cube):
    """
    X3R: Gira la fila superior (row=0) hacia la derecha.
    La cara superior (U) rota en sentido antihorario.
    """
    c = copy.deepcopy(cube)
    tmp = c[L][0][:]
    c[L][0] = c[B][0][:]
    c[B][0] = c[R][0][:]
    c[R][0] = c[F][0][:]
    c[F][0] = tmp
    c[U] = rotate_face_ccw(c[U])
    return c

def move_X3L(cube):
    """X3L: Gira la fila superior (row=0) hacia la izquierda. Inverso de X3R."""
    c = copy.deepcopy(cube)
    tmp = c[L][0][:]
    c[L][0] = c[F][0][:]
    c[F][0] = c[R][0][:]
    c[R][0] = c[B][0][:]
    c[B][0] = tmp
    c[U] = rotate_face_cw(c[U])
    return c

# --- Movimientos Y (columnas verticales) ---

def move_Y1U(cube):
    """
    Y1U: Gira la columna izquierda (col=0) hacia arriba.
    La cara izquierda (L) rota en sentido horario.
    """
    c = copy.deepcopy(cube)
    tmp = [c[U][r][0] for r in range(3)]
    for r in range(3):
        c[U][r][0] = c[F][r][0]
        c[F][r][0] = c[D][r][0]
        c[D][r][0] = c[B][2-r][2]   # cara trasera invertida
        c[B][2-r][2] = tmp[r]
    c[L] = rotate_face_cw(c[L])
    return c

def move_Y1D(cube):
    """Y1D: Gira la columna izquierda (col=0) hacia abajo. Inverso de Y1U."""
    c = copy.deepcopy(cube)
    tmp = [c[U][r][0] for r in range(3)]
    for r in range(3):
        c[U][r][0] = c[B][2-r][2]
        c[B][2-r][2] = c[D][r][0]
        c[D][r][0] = c[F][r][0]
        c[F][r][0] = tmp[r]
    c[L] = rotate_face_ccw(c[L])
    return c

def move_Y2U(cube):
    """Y2U: Gira la columna central (col=1) hacia arriba."""
    c = copy.deepcopy(cube)
    tmp = [c[U][r][1] for r in range(3)]
    for r in range(3):
        c[U][r][1] = c[F][r][1]
        c[F][r][1] = c[D][r][1]
        c[D][r][1] = c[B][2-r][1]
        c[B][2-r][1] = tmp[r]
    return c

def move_Y2D(cube):
    """Y2D: Gira la columna central (col=1) hacia abajo. Inverso de Y2U."""
    c = copy.deepcopy(cube)
    tmp = [c[U][r][1] for r in range(3)]
    for r in range(3):
        c[U][r][1] = c[B][2-r][1]
        c[B][2-r][1] = c[D][r][1]
        c[D][r][1] = c[F][r][1]
        c[F][r][1] = tmp[r]
    return c

def move_Y3U(cube):
    """
    Y3U: Gira la columna derecha (col=2) hacia arriba.
    La cara derecha (R) rota en sentido antihorario.
    """
    c = copy.deepcopy(cube)
    tmp = [c[U][r][2] for r in range(3)]
    for r in range(3):
        c[U][r][2] = c[F][r][2]
        c[F][r][2] = c[D][r][2]
        c[D][r][2] = c[B][2-r][0]
        c[B][2-r][0] = tmp[r]
    c[R] = rotate_face_ccw(c[R])
    return c

def move_Y3D(cube):
    """Y3D: Gira la columna derecha (col=2) hacia abajo. Inverso de Y3U."""
    c = copy.deepcopy(cube)
    tmp = [c[U][r][2] for r in range(3)]
    for r in range(3):
        c[U][r][2] = c[B][2-r][0]
        c[B][2-r][0] = c[D][r][2]
        c[D][r][2] = c[F][r][2]
        c[F][r][2] = tmp[r]
    c[R] = rotate_face_cw(c[R])
    return c

# --- Movimientos Z (capas frontales) ---

def move_Z1R(cube):
    """
    Z1R: Gira la capa frontal (cara F) hacia la derecha (sentido horario).
    Afecta la fila inferior de U, columna derecha de L, fila superior de D, columna izq de R.
    """
    c = copy.deepcopy(cube)
    tmp = c[U][2][:]
    c[U][2] = [c[L][2][2], c[L][1][2], c[L][0][2]]
    c[L][0][2] = c[D][0][0]
    c[L][1][2] = c[D][0][1]
    c[L][2][2] = c[D][0][2]
    c[D][0] = [c[R][2][0], c[R][1][0], c[R][0][0]]
    c[R][0][0] = tmp[0]
    c[R][1][0] = tmp[1]
    c[R][2][0] = tmp[2]
    c[F] = rotate_face_cw(c[F])
    return c

def move_Z1L(cube):
    """Z1L: Gira la capa frontal hacia la izquierda. Inverso de Z1R."""
    c = copy.deepcopy(cube)
    tmp = c[U][2][:]
    c[U][2] = [c[R][0][0], c[R][1][0], c[R][2][0]]
    c[R][0][0] = c[D][0][2]
    c[R][1][0] = c[D][0][1]
    c[R][2][0] = c[D][0][0]
    c[D][0] = [c[L][0][2], c[L][1][2], c[L][2][2]]
    c[L][0][2] = tmp[2]
    c[L][1][2] = tmp[1]
    c[L][2][2] = tmp[0]
    c[F] = rotate_face_ccw(c[F])
    return c

def move_Z2R(cube):
    """Z2R: Gira la capa media frontal (entre F y B) hacia la derecha."""
    c = copy.deepcopy(cube)
    tmp = c[U][1][:]
    c[U][1] = [c[L][2][1], c[L][1][1], c[L][0][1]]
    c[L][0][1] = c[D][1][0]
    c[L][1][1] = c[D][1][1]
    c[L][2][1] = c[D][1][2]
    c[D][1] = [c[R][2][1], c[R][1][1], c[R][0][1]]
    c[R][0][1] = tmp[0]
    c[R][1][1] = tmp[1]
    c[R][2][1] = tmp[2]
    return c

def move_Z2L(cube):
    """Z2L: Gira la capa media frontal hacia la izquierda. Inverso de Z2R."""
    c = copy.deepcopy(cube)
    tmp = c[U][1][:]
    c[U][1] = [c[R][0][1], c[R][1][1], c[R][2][1]]
    c[R][0][1] = c[D][1][2]
    c[R][1][1] = c[D][1][1]
    c[R][2][1] = c[D][1][0]
    c[D][1] = [c[L][0][1], c[L][1][1], c[L][2][1]]
    c[L][0][1] = tmp[2]
    c[L][1][1] = tmp[1]
    c[L][2][1] = tmp[0]
    return c

def move_Z3R(cube):
    """
    Z3R: Gira la capa trasera (cara B) hacia la derecha.
    La cara trasera (B) rota en sentido antihorario desde la perspectiva frontal.
    """
    c = copy.deepcopy(cube)
    tmp = c[U][0][:]
    c[U][0] = [c[L][0][0], c[L][1][0], c[L][2][0]]
    c[L][0][0] = c[D][2][2]
    c[L][1][0] = c[D][2][1]
    c[L][2][0] = c[D][2][0]
    c[D][2] = [c[R][2][2], c[R][1][2], c[R][0][2]]
    c[R][0][2] = tmp[0]
    c[R][1][2] = tmp[1]
    c[R][2][2] = tmp[2]
    c[B] = rotate_face_ccw(c[B])
    return c

def move_Z3L(cube):
    """Z3L: Gira la capa trasera hacia la izquierda. Inverso de Z3R."""
    c = copy.deepcopy(cube)
    tmp = c[U][0][:]
    c[U][0] = [c[R][0][2], c[R][1][2], c[R][2][2]]
    c[R][0][2] = c[D][2][0]
    c[R][1][2] = c[D][2][1]
    c[R][2][2] = c[D][2][2]
    c[D][2] = [c[L][2][0], c[L][1][0], c[L][0][0]]
    c[L][0][0] = tmp[2]
    c[L][1][0] = tmp[1]
    c[L][2][0] = tmp[0]
    c[B] = rotate_face_cw(c[B])
    return c

# =============================================================================
# DICCIONARIO DE MOVIMIENTOS
# Todos los 18 movimientos posibles del cubo según la nomenclatura del taller.
# Cada movimiento es un operador (acción) que transforma un estado en otro.
# =============================================================================

MOVES = {
    'X1R': move_X1R, 'X1L': move_X1L,
    'X2R': move_X2R, 'X2L': move_X2L,
    'X3R': move_X3R, 'X3L': move_X3L,
    'Y1U': move_Y1U, 'Y1D': move_Y1D,
    'Y2U': move_Y2U, 'Y2D': move_Y2D,
    'Y3U': move_Y3U, 'Y3D': move_Y3D,
    'Z1R': move_Z1R, 'Z1L': move_Z1L,
    'Z2R': move_Z2R, 'Z2L': move_Z2L,
    'Z3R': move_Z3R, 'Z3L': move_Z3L,
}

# =============================================================================
# ALGORITMO BFS
# Implementación del pseudocódigo del taller:
#   BFS(grafo, inicio):
#       crear cola Q
#       marcar inicio como visitado
#       Q.encolar(inicio)
#       mientras Q no esté vacía:
#           v = Q.desencolar()
#           para cada vecino u de v:
#               si u no ha sido visitado:
#                   marcar u como visitado
#                   Q.encolar(u)
# =============================================================================

def is_solved(cube):
    """
    Verifica si el cubo está en el estado final (resuelto).
    Estado Final(f): cada cara tiene todos sus stickers del mismo color.
    """
    for face in cube:
        color = face[0][0]           # Color de referencia: esquina superior izquierda
        for row in face:
            if any(c != color for c in row):
                return False
    return True

def bfs_solve(initial_cube, max_depth=6):
    """
    Algoritmo BFS para resolver el cubo Rubik.
    
    Parámetros:
        initial_cube: estado inicial del cubo (Estado Inicial s0)
        max_depth: profundidad máxima de búsqueda (limita la exploración)
    
    Retorna:
        Lista de movimientos que resuelven el cubo, o None si no se encontró solución.
    
    Complejidad Temporal: O(V + E) donde V = estados y E = movimientos entre estados
    Complejidad Espacial: O(V) para almacenar nodos en la cola y el conjunto de visitados
    """
    start_state = cube_to_tuple(initial_cube)
    goal_state  = cube_to_tuple(create_solved_cube())

    # Caso trivial: el cubo ya está resuelto
    if start_state == goal_state:
        return []

    # Cola FIFO: cada elemento es (estado_actual, lista_de_movimientos_realizados)
    # BFS garantiza que el primer camino encontrado al goal es el más corto (óptimo)
    queue = deque()
    queue.append((start_state, []))    # Encolar estado inicial sin movimientos

    # Conjunto de estados visitados para evitar ciclos (explorar mismo estado dos veces)
    visited = set()
    visited.add(start_state)          # Marcar inicio como visitado

    nodes_explored = 0               # Contador para estadísticas

    # Bucle principal del BFS: mientras la cola no esté vacía
    while queue:
        current_state, path = queue.popleft()   # Desencolar (FIFO)
        nodes_explored += 1

        # Limitar profundidad para evitar explosión de estados
        if len(path) >= max_depth:
            continue

        # Explorar todos los vecinos (aplicar cada movimiento posible)
        for move_name, move_func in MOVES.items():
            current_cube = tuple_to_cube(current_state)
            next_cube = move_func(current_cube)            # Aplicar operador
            next_state = cube_to_tuple(next_cube)

            # Si el vecino no ha sido visitado
            if next_state not in visited:
                new_path = path + [move_name]

                # Verificar si llegamos al estado final
                if next_state == goal_state:
                    print(f"[BFS] Solución encontrada en {len(new_path)} movimientos.")
                    print(f"[BFS] Nodos explorados: {nodes_explored}")
                    return new_path

                visited.add(next_state)                    # Marcar como visitado
                queue.append((next_state, new_path))       # Encolar

    print(f"[BFS] No se encontró solución en profundidad {max_depth}.")
    print(f"[BFS] Nodos explorados: {nodes_explored}")
    return None

# =============================================================================
# UTILIDADES DE VISUALIZACIÓN
# =============================================================================

def print_cube(cube):
    """
    Imprime el cubo en formato de cruz 2D (como en el PDF del taller).
    Muestra las 6 caras en su disposición: U arriba, L-F-R-B en el centro, D abajo.
    """
    print("\n        [UP - Blanco]")
    for row in cube[U]:
        print("        " + " ".join(COLOR_NAMES[c] for c in row))
    print("[L-Green] [F-Red]   [R-Blue] [B-Orange]")
    for r in range(3):
        line = ""
        for face in [L, F, R, B]:
            line += " ".join(COLOR_NAMES[c] for c in cube[face][r]) + "  "
        print(line)
    print("        [DOWN - Amarillo]")
    for row in cube[D]:
        print("        " + " ".join(COLOR_NAMES[c] for c in row))
    print()

def scramble_cube(cube, moves_list):
    """
    Aplica una secuencia de movimientos al cubo para mezclarlo.
    moves_list: lista de strings con nombres de movimientos (ej: ['X1R', 'Y2U', 'Z3L'])
    Retorna el cubo mezclado.
    """
    c = copy.deepcopy(cube)
    for move in moves_list:
        if move in MOVES:
            c = MOVES[move](c)
        else:
            print(f"[!] Movimiento desconocido: {move}")
    return c

# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("=" * 55)
    print("  Taller: BFS para resolución del Cubo Rubik 3x3x3")
    print("  Tema: Algoritmos de Búsqueda BFS")
    print("=" * 55)

    # Estado Final (f): cubo resuelto
    solved = create_solved_cube()
    print("\n[1] Estado FINAL (cubo resuelto):")
    print_cube(solved)

    # Estado Inicial (s0): cubo mezclado aplicando movimientos conocidos
    # Se mezcla con pocos movimientos para que BFS pueda resolverlo en tiempo razonable
    scramble_sequence = ['X1R', 'Y3U', 'Z1R']
    scrambled = scramble_cube(solved, scramble_sequence)

    print(f"[2] Estado INICIAL (mezcla: {' -> '.join(scramble_sequence)}):")
    print_cube(scrambled)

    # Ejecutar BFS
    print("[3] Ejecutando BFS...")
    print(f"    Espacio de estados del cubo Rubik: ~4.3 × 10^19 combinaciones")
    print(f"    Movimientos posibles por estado: {len(MOVES)} (18 operadores)")
    print()

    solution = bfs_solve(scrambled, max_depth=len(scramble_sequence) + 2)

    if solution:
        print(f"\n[4] Secuencia de solución: {' -> '.join(solution)}")
        # Verificar aplicando la solución al cubo mezclado
        result = scramble_cube(scrambled, solution)
        print(f"\n[5] Estado tras aplicar la solución:")
        print_cube(result)
        print(f"    ¿Resuelto? {'SÍ ✓' if is_solved(result) else 'NO ✗'}")
    else:
        print("\n[!] BFS no encontró solución con la profundidad configurada.")
        print("    Aumenta 'max_depth' para explorar más niveles del grafo.")

    print("\n[INFO] BFS garantiza la solución ÓPTIMA (mínimo de movimientos)")
    print("       en grafos sin pesos, como el espacio de estados del cubo.")
