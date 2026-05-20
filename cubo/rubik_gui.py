"""
Taller: Algoritmo BFS - Cubo Rubik 3x3x3 (Interfaz Tkinter)
Autor: [Tu nombre]
Descripción: GUI que visualiza el cubo en forma de cruz 2D, permite aplicar
             movimientos manualmente y resolver con BFS automáticamente.
             Importa toda la lógica desde rubik_bfs.py (debe estar en la misma carpeta).
"""

import tkinter as tk
from tkinter import messagebox
import threading
import random

# Importar lógica del archivo principal del taller
from rubik_bfs import (
    create_solved_cube, scramble_cube, bfs_solve,
    is_solved, MOVES, U, L, F, R, B, D
)

# =============================================================================
# CONFIGURACIÓN VISUAL
# Colores reales de cada cara según el PDF del taller
# =============================================================================
FACE_COLORS = {
    0: "#FFFFFF",  # Blanco  -> cara U (Up)
    1: "#00A651",  # Verde   -> cara L (Left)
    2: "#B71234",  # Rojo    -> cara F (Front)
    3: "#0046AD",  # Azul    -> cara R (Right)
    4: "#FF5800",  # Naranja -> cara B (Back)
    5: "#FFD500",  # Amarillo-> cara D (Down)
}
FACE_LABELS = {U: "UP", L: "LEFT", F: "FRONT", R: "RIGHT", B: "BACK", D: "DOWN"}

# Tamaño de cada celda en píxeles
CELL = 42
GAP  = 3   # separación entre celdas


class RubikApp:
    """
    Aplicación principal con Tkinter.
    Contiene el canvas del cubo, los botones de movimientos y el panel BFS.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Cubo Rubik - BFS Taller")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # Estado inicial: cubo resuelto
        self.cube = create_solved_cube()
        self.solution_steps = []   # Lista de movimientos de la solución BFS
        self.step_index = 0        # Paso actual al reproducir solución

        self._build_ui()
        self.draw_cube()

    # -------------------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ
    # -------------------------------------------------------------------------

    def _build_ui(self):
        """Construye todos los widgets de la ventana."""

        # --- Título ---
        tk.Label(self.root, text="Cubo Rubik — BFS Solver",
                 font=("Consolas", 15, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=(12, 0))

        # --- Canvas donde se dibuja el cubo en cruz 2D ---
        # La cruz ocupa 4 caras de ancho x 3 de alto; padding mínimo
        canvas_w = (CELL + GAP) * 3 * 4 + 20
        canvas_h = (CELL + GAP) * 3 * 3 + 30
        self.canvas = tk.Canvas(self.root, width=canvas_w, height=canvas_h,
                                bg="#181825", highlightthickness=0)
        self.canvas.pack(padx=20, pady=6)

        # --- Panel de movimientos manuales ---
        # 3 secciones: X (filas), Y (columnas), Z (capas)
        move_frame = tk.Frame(self.root, bg="#1e1e2e")
        move_frame.pack(pady=(0, 6))

        tk.Label(move_frame, text="Movimientos manuales",
                 font=("Consolas", 11, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").grid(row=0, column=0,
                 columnspan=14, pady=(0, 6))

        # Eje X: filas horizontales
        tk.Label(move_frame, text="X  Filas  ←→",
                 font=("Consolas", 9, "bold"), bg="#1e1e2e", fg="#a6e3a1")            .grid(row=1, column=0, columnspan=2, padx=(0,8), sticky="e")
        x_moves = [("X1R","← Der"), ("X1L","→ Izq"), ("X2R","← Der"), ("X2L","→ Izq"), ("X3R","← Der"), ("X3L","→ Izq")]
        x_labels = ["Fila 1", "Fila 1", "Fila 2", "Fila 2", "Fila 3", "Fila 3"]
        for i, ((mv, arrow), lbl) in enumerate(zip(x_moves, x_labels)):
            f = tk.Frame(move_frame, bg="#1e1e2e")
            f.grid(row=1, column=i+2, padx=3)
            tk.Label(f, text=lbl, font=("Consolas", 7), bg="#1e1e2e", fg="#585b70").pack()
            tk.Button(f, text=mv, width=5,
                      font=("Consolas", 9, "bold"), bg="#313244", fg="#a6e3a1",
                      activebackground="#45475a", relief="flat", cursor="hand2",
                      command=lambda m=mv: self.apply_move(m)).pack()

        # Eje Y: columnas verticales
        tk.Label(move_frame, text="Y  Cols   ↑↓",
                 font=("Consolas", 9, "bold"), bg="#1e1e2e", fg="#89b4fa")            .grid(row=2, column=0, columnspan=2, padx=(0,8), sticky="e", pady=(6,0))
        y_moves = [("Y1U","↑ Arr"), ("Y1D","↓ Abj"), ("Y2U","↑ Arr"), ("Y2D","↓ Abj"), ("Y3U","↑ Arr"), ("Y3D","↓ Abj")]
        y_labels = ["Col 1", "Col 1", "Col 2", "Col 2", "Col 3", "Col 3"]
        for i, ((mv, arrow), lbl) in enumerate(zip(y_moves, y_labels)):
            f = tk.Frame(move_frame, bg="#1e1e2e")
            f.grid(row=2, column=i+2, padx=3, pady=(6,0))
            tk.Label(f, text=lbl, font=("Consolas", 7), bg="#1e1e2e", fg="#585b70").pack()
            tk.Button(f, text=mv, width=5,
                      font=("Consolas", 9, "bold"), bg="#313244", fg="#89b4fa",
                      activebackground="#45475a", relief="flat", cursor="hand2",
                      command=lambda m=mv: self.apply_move(m)).pack()

        # Eje Z: capas frontales
        tk.Label(move_frame, text="Z  Capas  ↻↺",
                 font=("Consolas", 9, "bold"), bg="#1e1e2e", fg="#fab387")            .grid(row=3, column=0, columnspan=2, padx=(0,8), sticky="e", pady=(6,0))
        z_moves = [("Z1R","↻ Hor"), ("Z1L","↺ Ant"), ("Z2R","↻ Hor"), ("Z2L","↺ Ant"), ("Z3R","↻ Hor"), ("Z3L","↺ Ant")]
        z_labels = ["Capa 1", "Capa 1", "Capa 2", "Capa 2", "Capa 3", "Capa 3"]
        for i, ((mv, arrow), lbl) in enumerate(zip(z_moves, z_labels)):
            f = tk.Frame(move_frame, bg="#1e1e2e")
            f.grid(row=3, column=i+2, padx=3, pady=(6,0))
            tk.Label(f, text=lbl, font=("Consolas", 7), bg="#1e1e2e", fg="#585b70").pack()
            tk.Button(f, text=mv, width=5,
                      font=("Consolas", 9, "bold"), bg="#313244", fg="#fab387",
                      activebackground="#45475a", relief="flat", cursor="hand2",
                      command=lambda m=mv: self.apply_move(m)).pack()

        # --- Panel BFS ---
        bfs_frame = tk.Frame(self.root, bg="#1e1e2e")
        bfs_frame.pack(pady=6)

        # Slider de profundidad máxima del BFS
        tk.Label(bfs_frame, text="Profundidad BFS:",
                 font=("Consolas", 10), bg="#1e1e2e", fg="#cdd6f4")\
            .grid(row=0, column=0, padx=6)

        self.depth_var = tk.IntVar(value=5)
        tk.Scale(bfs_frame, from_=1, to=8, orient="horizontal",
                 variable=self.depth_var, bg="#313244", fg="#cdd6f4",
                 troughcolor="#45475a", highlightthickness=0, length=120)\
            .grid(row=0, column=1, padx=6)

        # Botones de acción principales
        btn_style = dict(font=("Consolas", 10, "bold"), relief="flat",
                         cursor="hand2", padx=10, pady=4)

        tk.Button(bfs_frame, text="🔀 Mezclar", bg="#89b4fa", fg="#1e1e2e",
                  command=self.scramble, **btn_style)\
            .grid(row=0, column=2, padx=6)

        tk.Button(bfs_frame, text="🔍 Resolver BFS", bg="#a6e3a1", fg="#1e1e2e",
                  command=self.run_bfs, **btn_style)\
            .grid(row=0, column=3, padx=6)

        tk.Button(bfs_frame, text="↺ Reset", bg="#f38ba8", fg="#1e1e2e",
                  command=self.reset, **btn_style)\
            .grid(row=0, column=4, padx=6)

        # --- Barra de estado / log ---
        self.status_var = tk.StringVar(value="Listo. Mezcla el cubo y presiona Resolver BFS.")
        tk.Label(self.root, textvariable=self.status_var,
                 font=("Consolas", 9), bg="#1e1e2e", fg="#a6adc8",
                 wraplength=600, justify="center").pack(pady=(0, 4))

        # --- Panel de solución paso a paso ---
        sol_frame = tk.Frame(self.root, bg="#1e1e2e")
        sol_frame.pack(pady=(0, 10))

        self.sol_label = tk.Label(sol_frame, text="",
                                  font=("Consolas", 10), bg="#1e1e2e", fg="#f9e2af")
        self.sol_label.grid(row=0, column=0, columnspan=3)

        self.prev_btn = tk.Button(sol_frame, text="◀ Anterior", state="disabled",
                                  font=("Consolas", 9, "bold"), bg="#313244",
                                  fg="#cdd6f4", relief="flat", cursor="hand2",
                                  command=self.prev_step)
        self.prev_btn.grid(row=1, column=0, padx=8, pady=4)

        self.next_btn = tk.Button(sol_frame, text="Siguiente ▶", state="disabled",
                                  font=("Consolas", 9, "bold"), bg="#313244",
                                  fg="#cdd6f4", relief="flat", cursor="hand2",
                                  command=self.next_step)
        self.next_btn.grid(row=1, column=2, padx=8, pady=4)

        self.auto_btn = tk.Button(sol_frame, text="▶▶ Auto", state="disabled",
                                  font=("Consolas", 9, "bold"), bg="#89b4fa",
                                  fg="#1e1e2e", relief="flat", cursor="hand2",
                                  command=self.auto_solve)
        self.auto_btn.grid(row=1, column=1, padx=8, pady=4)

    # -------------------------------------------------------------------------
    # DIBUJO DEL CUBO EN FORMA DE CRUZ 2D
    # Disposición igual al PDF del taller:
    #       [U]
    #  [L][F][R][B]
    #       [D]
    # -------------------------------------------------------------------------

    def draw_cube(self):
        """Dibuja el cubo completo en el canvas en formato de cruz 2D."""
        self.canvas.delete("all")
        step = CELL + GAP

        # Posición (col, row) de la esquina superior izquierda de cada cara
        # en unidades de 'step'
        face_positions = {
            U: (1, 0),   # Arriba al centro
            L: (0, 1),   # Izquierda en la fila del medio
            F: (1, 1),   # Frente en el centro
            R: (2, 1),   # Derecha
            B: (3, 1),   # Atrás a la derecha
            D: (1, 2),   # Abajo al centro
        }

        # Offset global: margen mínimo
        ox = 8
        oy = 8

        for face_idx, (fc, fr) in face_positions.items():
            for row in range(3):
                for col in range(3):
                    # Coordenadas en píxeles de cada celda
                    x1 = ox + (fc * 3 + col) * step
                    y1 = oy + (fr * 3 + row) * step
                    x2 = x1 + CELL
                    y2 = y1 + CELL
                    color_id = self.cube[face_idx][row][col]
                    fill = FACE_COLORS[color_id]

                    # Dibujar celda con borde redondeado (simulado)
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=fill, outline="#11111b", width=2
                    )

            # Etiqueta centrada debajo de la cara
            lx = ox + (fc * 3 + 1) * step + CELL // 2
            ly = oy + (fr * 3 + 3) * step - GAP + 6
            self.canvas.create_text(lx, ly,
                text=FACE_LABELS[face_idx],
                font=("Consolas", 8, "bold"),
                fill="#6c7086")

    # -------------------------------------------------------------------------
    # ACCIONES
    # -------------------------------------------------------------------------

    def apply_move(self, move_name):
        """Aplica un movimiento manual al cubo y redibuja."""
        self.cube = MOVES[move_name](self.cube)
        self.draw_cube()
        self.status_var.set(f"Movimiento aplicado: {move_name}")
        # Limpiar solución previa si se mueve manualmente
        self._clear_solution()

    def scramble(self):
        """Mezcla el cubo con movimientos aleatorios y redibuja."""
        depth = self.depth_var.get()
        moves = random.choices(list(MOVES.keys()), k=depth)
        self.cube = scramble_cube(create_solved_cube(), moves)
        self.draw_cube()
        self.status_var.set(f"Cubo mezclado con {depth} movimientos: {' → '.join(moves)}")
        self._clear_solution()

    def reset(self):
        """Reinicia el cubo al estado resuelto."""
        self.cube = create_solved_cube()
        self.draw_cube()
        self.status_var.set("Cubo reiniciado al estado resuelto.")
        self._clear_solution()

    def run_bfs(self):
        """
        Lanza el BFS en un hilo separado para no bloquear la interfaz.
        BFS: explora nivel por nivel desde el estado inicial hasta el estado final.
        Complejidad Temporal O(V+E), Complejidad Espacial O(V).
        """
        if is_solved(self.cube):
            messagebox.showinfo("¡Ya resuelto!", "El cubo ya está en el estado final.")
            return

        self.status_var.set("⏳ Ejecutando BFS... (puede tardar según la profundidad)")
        self._clear_solution()

        # Guardar snapshot del cubo actual para la animación paso a paso
        self._bfs_start_cube = [row[:] for face in self.cube for row in face]
        import copy
        self._bfs_start_cube = copy.deepcopy(self.cube)

        def bfs_thread():
            solution = bfs_solve(self.cube, max_depth=self.depth_var.get())
            # Actualizar UI desde el hilo principal usando after()
            self.root.after(0, lambda: self._on_bfs_done(solution))

        threading.Thread(target=bfs_thread, daemon=True).start()

    def _on_bfs_done(self, solution):
        """Callback ejecutado cuando el BFS termina (en el hilo principal)."""
        if solution is None:
            self.status_var.set(
                f" BFS no encontró solución con profundidad {self.depth_var.get()}. "
                "Aumenta la profundidad o reduce la mezcla.")
            return

        if len(solution) == 0:
            self.status_var.set(" El cubo ya estaba resuelto.")
            return

        # Guardar solución y preparar reproducción paso a paso
        self.solution_steps = solution
        self.step_index = 0
        self._sol_cube = self._bfs_start_cube  # cubo en el inicio de la solución

        self.status_var.set(
            f" BFS encontró solución en {len(solution)} movimientos: "
            f"{' → '.join(solution)}")
        self._update_solution_ui()

    # -------------------------------------------------------------------------
    # REPRODUCCIÓN PASO A PASO DE LA SOLUCIÓN
    # -------------------------------------------------------------------------

    def _update_solution_ui(self):
        """Actualiza el label de pasos y habilita/deshabilita botones."""
        total = len(self.solution_steps)
        if total == 0:
            return

        self.sol_label.config(
            text=f"Paso {self.step_index}/{total}  —  "
                 f"Siguiente: {self.solution_steps[self.step_index] if self.step_index < total else '✓ Resuelto'}"
        )
        self.prev_btn.config(state="normal" if self.step_index > 0 else "disabled")
        self.next_btn.config(state="normal" if self.step_index < total else "disabled")
        self.auto_btn.config(state="normal" if self.step_index < total else "disabled")

    def next_step(self):
        """Aplica el siguiente movimiento de la solución."""
        if self.step_index < len(self.solution_steps):
            move = self.solution_steps[self.step_index]
            self.cube = MOVES[move](self.cube)
            self.step_index += 1
            self.draw_cube()
            self._update_solution_ui()
            if self.step_index == len(self.solution_steps):
                self.status_var.set("🎉 ¡Cubo resuelto con BFS!")

    def prev_step(self):
        """
        Retrocede un paso: rehace el cubo desde el inicio hasta step_index - 1.
        (Más simple que calcular el inverso del movimiento.)
        """
        if self.step_index > 0:
            self.step_index -= 1
            self.cube = scramble_cube(self._sol_cube,
                                      self.solution_steps[:self.step_index])
            self.draw_cube()
            self._update_solution_ui()

    def auto_solve(self):
        """Reproduce automáticamente todos los pasos restantes con animación."""
        def step():
            if self.step_index < len(self.solution_steps):
                self.next_step()
                self.root.after(600, step)   # 600ms entre pasos

        step()

    def _clear_solution(self):
        """Limpia el estado de la solución BFS actual."""
        self.solution_steps = []
        self.step_index = 0
        self.sol_label.config(text="")
        self.prev_btn.config(state="disabled")
        self.next_btn.config(state="disabled")
        self.auto_btn.config(state="disabled")



if __name__ == "__main__":
    root = tk.Tk()
    app = RubikApp(root)
    root.mainloop()
