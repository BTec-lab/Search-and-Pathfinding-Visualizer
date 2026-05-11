import tkinter as tk
import heapq
import time
import random

ROWS, COLS = 25, 35
CELL = 22

BLACK  = "#1e1e2e"
WHITE  = "#cdd6f4"
BLUE   = "#89b4fa"
GRAY   = "#45475a"

TERRAIN = {
    "empty":   {"color": "#1e1e2e", "weight": 1,  "label": "Empty"},
    "swamp":   {"color": "#6b3a2a", "weight": 5,  "label": "Swamp (5)"},
    "wall":    {"color": "#313244", "weight": -1, "label": "Wall"},
    "start":   {"color": "#a6e3a1", "weight": 1,  "label": "Start"},
    "end":     {"color": "#f38ba8", "weight": 1,  "label": "End"},
    "visited": {"color": "#4455aa", "weight": 0,  "label": "Visited"},
    "path":    {"color": "#f9e2af", "weight": 0,  "label": "Shortest Path"},
}

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra - Weighted Maze Visualizer")
        self.root.configure(bg=BLACK)

        self.grid = [["empty"]*COLS for _ in range(ROWS)]
        self.start_cell = None
        self.end_cell = None
        self.mode = "start"
        self.brush = "wall"
        self.running = False
        self.visited = set()
        self.path = set()

        top = tk.Frame(root, bg=BLACK)
        top.pack(pady=6)

        self.info = tk.Label(top, text="1. Click the start cell",
                             font=("Arial", 11), fg=WHITE, bg=BLACK, width=38)
        self.info.pack(side=tk.LEFT, padx=8)

        self.run_btn = tk.Button(top, text="Run", font=("Arial", 11, "bold"),
                                 bg=BLUE, fg=BLACK, relief=tk.FLAT,
                                 padx=12, pady=3, command=self.run, state=tk.DISABLED)
        self.run_btn.pack(side=tk.LEFT, padx=4)

        self.reset_btn = tk.Button(top, text="Reset", font=("Arial", 11),
                                   bg=GRAY, fg=WHITE, relief=tk.FLAT,
                                   padx=12, pady=3, command=self.reset)
        self.reset_btn.pack(side=tk.LEFT, padx=4)

        self.gen_btn = tk.Button(top, text="Generate Maze", font=("Arial", 11),
                                 bg="#cba6f7", fg=BLACK, relief=tk.FLAT,
                                 padx=12, pady=3, command=self.generate_maze)
        self.gen_btn.pack(side=tk.LEFT, padx=4)

        brush_frame = tk.Frame(root, bg=BLACK)
        brush_frame.pack(pady=4)

        tk.Label(brush_frame, text="Draw:", font=("Arial", 10),
                 fg=WHITE, bg=BLACK).pack(side=tk.LEFT, padx=6)

        self.brush_btns = {}
        for name in ["wall", "swamp", "empty"]:
            data = TERRAIN[name]
            btn = tk.Button(brush_frame, text=data["label"],
                           font=("Arial", 9),
                           bg=data["color"], fg=WHITE,
                           relief=tk.FLAT, padx=8, pady=2,
                           command=lambda n=name: self.set_brush(n))
            btn.pack(side=tk.LEFT, padx=3)
            self.brush_btns[name] = btn

        leg = tk.Frame(root, bg=BLACK)
        leg.pack(pady=2)
        for name in ["start","end","visited","path"]:
            data = TERRAIN[name]
            tk.Label(leg, bg=data["color"], width=2, height=1).pack(side=tk.LEFT, padx=2)
            tk.Label(leg, text=data["label"], font=("Arial", 8),
                    fg=WHITE, bg=BLACK).pack(side=tk.LEFT, padx=4)

        W = COLS * CELL
        H = ROWS * CELL
        self.canvas = tk.Canvas(root, width=W, height=H,
                                bg="#11111b", highlightthickness=0)
        self.canvas.pack(padx=10, pady=6)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        self.highlight_brush()
        self.draw()

    def set_brush(self, name):
        self.brush = name
        self.highlight_brush()

    def highlight_brush(self):
        for name, btn in self.brush_btns.items():
            btn.config(relief=tk.SUNKEN if name == self.brush else tk.FLAT)

    def draw(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c*CELL, r*CELL
                x2, y2 = x1+CELL, y1+CELL
                cell = self.grid[r][c]

                if (r,c) == self.start_cell:
                    color, label = TERRAIN["start"]["color"], "S"
                elif (r,c) == self.end_cell:
                    color, label = TERRAIN["end"]["color"], "E"
                elif (r,c) in self.path:
                    color, label = TERRAIN["path"]["color"], ""
                elif (r,c) in self.visited:
                    color, label = TERRAIN["visited"]["color"], ""
                else:
                    color = TERRAIN[cell]["color"]
                    w = TERRAIN[cell]["weight"]
                    label = str(w) if w > 1 else ""

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="#2a2a3a", width=0.5)
                if label:
                    self.canvas.create_text(x1+CELL//2, y1+CELL//2,
                                           text=label, fill="#1a1a1a",
                                           font=("Arial", 8, "bold"))

    def get_cell(self, event):
        r = event.y // CELL
        c = event.x // CELL
        if 0 <= r < ROWS and 0 <= c < COLS:
            return r, c
        return None

    def on_click(self, event):
        if self.running:
            return
        cell = self.get_cell(event)
        if not cell:
            return
        r, c = cell

        if self.mode == "start":
            self.start_cell = (r,c)
            self.grid[r][c] = "empty"
            self.mode = "end"
            self.info.config(text="2. Click the end cell")
        elif self.mode == "end":
            if (r,c) != self.start_cell:
                self.end_cell = (r,c)
                self.grid[r][c] = "empty"
                self.mode = "draw"
                self.info.config(text="3. Draw terrain, then click Run")
                self.run_btn.config(state=tk.NORMAL)
        elif self.mode == "draw":
            if (r,c) != self.start_cell and (r,c) != self.end_cell:
                self.grid[r][c] = self.brush
        self.draw()

    def on_drag(self, event):
        if self.running or self.mode != "draw":
            return
        cell = self.get_cell(event)
        if not cell:
            return
        r, c = cell
        if (r,c) != self.start_cell and (r,c) != self.end_cell:
            self.grid[r][c] = self.brush
        self.draw()

    def get_neighbors(self, r, c):
        result = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                t = self.grid[nr][nc]
                if t != "wall":
                    result.append((nr, nc, TERRAIN[t]["weight"]))
        return result

    def run(self):
        if not self.start_cell or not self.end_cell:
            return
        self.running = True
        self.run_btn.config(state=tk.DISABLED)
        self.visited = set()
        self.path = set()

        dist = {(r,c): float('inf') for r in range(ROWS) for c in range(COLS)}
        prev = {}
        dist[self.start_cell] = 0
        pq = [(0, self.start_cell)]

        found = False
        while pq:
            cost, u = heapq.heappop(pq)
            if u in self.visited:
                continue
            self.visited.add(u)

            if u == self.end_cell:
                found = True
                break

            for nr, nc, w in self.get_neighbors(u[0], u[1]):
                v = (nr, nc)
                nd = dist[u] + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))

            if len(self.visited) % 2 == 0:
                self.draw()
                self.root.update()
                time.sleep(0.015)

        if found:
            node = self.end_cell
            while node in prev:
                self.path.add(node)
                node = prev[node]
            self.path.add(self.start_cell)
            self.draw()
            self.info.config(text=f"Found! Total cost: {dist[self.end_cell]}")
        else:
            self.draw()
            self.info.config(text="No path found!")

        self.running = False
        self.run_btn.config(state=tk.NORMAL)

    def generate_maze(self):
        self.reset()
        for r in range(ROWS):
            for c in range(COLS):
                rnd = random.random()
                if rnd < 0.18:
                    self.grid[r][c] = "wall"
                elif rnd < 0.28:
                    self.grid[r][c] = "swamp"
        self.start_cell = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
        self.end_cell = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
        while self.end_cell == self.start_cell:
            self.end_cell = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
        self.grid[self.start_cell[0]][self.start_cell[1]] = "empty"
        self.grid[self.end_cell[0]][self.end_cell[1]] = "empty"
        self.mode = "draw"
        self.run_btn.config(state=tk.NORMAL)
        self.info.config(text="Maze generated! Click Run or draw more terrain")
        self.draw()

    def reset(self):
        self.grid = [["empty"]*COLS for _ in range(ROWS)]
        self.start_cell = None
        self.end_cell = None
        self.mode = "start"
        self.running = False
        self.visited = set()
        self.path = set()
        self.run_btn.config(state=tk.DISABLED)
        self.info.config(text="1. Click the start cell")
        self.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()