import pygame
from queue import PriorityQueue
from collections import deque
import math

pygame.init()

GRID_SIZE   = 600         
PANEL_W     = 220          
WIDTH       = GRID_SIZE + PANEL_W
HEIGHT      = GRID_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")

BG          = (245, 247, 252)
PANEL_BG    = (225, 228, 242)
PANEL_EDGE  = (185, 190, 215)

C_EMPTY     = (255, 255, 255)  
C_BARRIER   = (35,  40,  65)   
C_START     = (255, 160,  40)  
C_END       = (0,  220, 180)  
C_OPEN      = (40, 200, 100)   
C_CLOSED    = (180,  50,  80)  
C_PATH      = (255, 220,  50)  
C_GRID_LINE = (205, 210, 228)

ACCENT      = (80, 140, 255)   
ACCENT2     = (0,  220, 180)   
TEXT_MAIN   = (30,  35,  70)
TEXT_DIM    = (100, 110, 150)
TEXT_WARN   = (255, 180,  50)
BTN_IDLE    = (210, 215, 235)
BTN_HOVER   = (195, 202, 228)
BTN_ACTIVE  = (50,  90, 200)
BTN_BORDER  = (160, 168, 205)

try:
    FONT_TITLE  = pygame.font.SysFont("consolas",    20, bold=True)
    FONT_LABEL  = pygame.font.SysFont("consolas",    14)
    FONT_SMALL  = pygame.font.SysFont("consolas",    12)
    FONT_KEY    = pygame.font.SysFont("consolas",    13, bold=True)
    FONT_BIG    = pygame.font.SysFont("consolas",    32, bold=True)
except Exception:
    FONT_TITLE  = pygame.font.SysFont("monospace", 20, bold=True)
    FONT_LABEL  = pygame.font.SysFont("monospace", 14)
    FONT_SMALL  = pygame.font.SysFont("monospace", 12)
    FONT_KEY    = pygame.font.SysFont("monospace", 13, bold=True)
    FONT_BIG    = pygame.font.SysFont("monospace", 32, bold=True)

ROWS = 40


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x   = col * width
        self.y   = row * width
        self.color = C_EMPTY
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def is_barrier(self): return self.color == C_BARRIER
    def reset(self):      self.color = C_EMPTY
    def make_start(self): self.color = C_START
    def make_closed(self):self.color = C_CLOSED
    def make_open(self):  self.color = C_OPEN
    def make_barrier(self):self.color = C_BARRIER
    def make_end(self):   self.color = C_END
    def make_path(self):  self.color = C_PATH

    def draw(self, win):
        r = self.color
        pygame.draw.rect(win, r,
                         (self.x + 1, self.y + 1,
                          self.width - 1, self.width - 1))
       
        if self.color in (C_START, C_END, C_PATH):
            s = pygame.Surface((self.width - 1, self.width - 1), pygame.SRCALPHA)
            alpha = 60
            s.fill((*r, alpha))
            win.blit(s, (self.x + 1, self.y + 1))

    def update_neighbors(self, grid):
        self.neighbors = []
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        for dr, dc in dirs:
            nr, nc = self.row + dr, self.col + dc
            if 0 <= nr < self.total_rows and 0 <= nc < self.total_rows:
                if not grid[nr][nc].is_barrier():
                    self.neighbors.append(grid[nr][nc])

    def __lt__(self, other): return False

def reconstruct_path(came_from, current, draw_fn):
    length = 0
    while current in came_from:
        current = came_from[current]
        if current.color != C_START:
            current.make_path()
        length += 1
        draw_fn()
    return length


def bfs(draw_fn, start, end):
    queue   = deque([start])
    visited = {start}
    came_from = {}

    while queue:
        current = queue.popleft()
        if current == end:
            return reconstruct_path(came_from, end, draw_fn)
        for n in current.neighbors:
            if n not in visited:
                visited.add(n)
                came_from[n] = current
                queue.append(n)
                if n != end: n.make_open()
        draw_fn()
        if current != start: current.make_closed()
    return 0


def dijkstra(draw_fn, grid, start, end):
    pq = PriorityQueue()
    pq.put((0, start))
    dist = {node: float("inf") for row in grid for node in row}
    dist[start] = 0
    came_from = {}

    while not pq.empty():
        d, current = pq.get()
        if current == end:
            return reconstruct_path(came_from, end, draw_fn)
        for n in current.neighbors:
            nd = dist[current] + 1
            if nd < dist[n]:
                dist[n] = nd
                came_from[n] = current
                pq.put((nd, n))
                if n != end: n.make_open()
        draw_fn()
        if current != start: current.make_closed()
    return 0

def make_grid(rows):
    gap  = GRID_SIZE // rows
    return [[Node(i, j, gap, rows) for j in range(rows)] for i in range(rows)]


def get_clicked_pos(pos, rows):
    gap  = GRID_SIZE // rows
    return pos[1] // gap, pos[0] // gap

class Button:
    def __init__(self, rect, label, key_hint, color_active=BTN_ACTIVE):
        self.rect         = pygame.Rect(rect)
        self.label        = label
        self.key_hint     = key_hint
        self.color_active = color_active
        self.active       = False
        self.hovered      = False

    def draw(self, win):
        bg = self.color_active if self.active else (BTN_HOVER if self.hovered else BTN_IDLE)
        pygame.draw.rect(win, bg, self.rect, border_radius=6)
        pygame.draw.rect(win, BTN_BORDER, self.rect, 1, border_radius=6)

        badge_w = 26
        badge_r = pygame.Rect(self.rect.x + 8, self.rect.centery - 10, badge_w, 20)
        pygame.draw.rect(win, PANEL_EDGE, badge_r, border_radius=4)
        k = FONT_KEY.render(self.key_hint, True, ACCENT if not self.active else (255,255,255))
        win.blit(k, (badge_r.centerx - k.get_width()//2,
                     badge_r.centery - k.get_height()//2))

        lbl = FONT_LABEL.render(self.label, True, TEXT_MAIN if self.active else TEXT_DIM)
        win.blit(lbl, (self.rect.x + badge_w + 18,
                       self.rect.centery - lbl.get_height()//2))

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def draw_legend_dot(win, x, y, color, label):
    pygame.draw.circle(win, color, (x + 7, y + 7), 7)
    pygame.draw.circle(win, PANEL_EDGE, (x + 7, y + 7), 7, 1)
    t = FONT_SMALL.render(label, True, TEXT_DIM)
    win.blit(t, (x + 20, y + 7 - t.get_height()//2))


def draw_panel(win, buttons, status, path_length, algo_name, nodes_visited,
               elapsed_ms):
    px = GRID_SIZE
    
    pygame.draw.rect(win, PANEL_BG, (px, 0, PANEL_W, HEIGHT))
    pygame.draw.line(win, PANEL_EDGE, (px, 0), (px, HEIGHT), 2)

    y = 18
    title = FONT_TITLE.render("PATHFINDER", True, ACCENT)
    win.blit(title, (px + PANEL_W//2 - title.get_width()//2, y))
    y += 24
    line_surf = pygame.Surface((PANEL_W - 20, 1))
    line_surf.fill(PANEL_EDGE)
    win.blit(line_surf, (px + 10, y))
    y += 10

    sec = FONT_SMALL.render("ALGORITHM", True, TEXT_DIM)
    win.blit(sec, (px + 12, y))
    y += 18
    for btn in buttons[:2]:
        btn.rect.x = px + 10
        btn.rect.y = y
        btn.rect.width = PANEL_W - 20
        btn.draw(win)
        y += btn.rect.height + 6

    y += 6
    win.blit(line_surf, (px + 10, y)); y += 10

    sec2 = FONT_SMALL.render("CONTROLS", True, TEXT_DIM)
    win.blit(sec2, (px + 12, y)); y += 18
    for btn in buttons[2:]:
        btn.rect.x = px + 10
        btn.rect.y = y
        btn.rect.width = PANEL_W - 20
        btn.draw(win)
        y += btn.rect.height + 6

    y += 6
    win.blit(line_surf, (px + 10, y)); y += 10

    sec3 = FONT_SMALL.render("STATS", True, TEXT_DIM)
    win.blit(sec3, (px + 12, y)); y += 18

    def stat_row(label, val, color=TEXT_MAIN):
        lbl = FONT_SMALL.render(label, True, TEXT_DIM)
        v   = FONT_SMALL.render(str(val), True, color)
        win.blit(lbl, (px + 12, y))
        win.blit(v,   (px + PANEL_W - 12 - v.get_width(), y))

    stat_row("Algorithm:", algo_name if algo_name else "—")
    y += 17
    stat_row("Path length:", path_length if path_length else "—",
             C_PATH if path_length else TEXT_MAIN)
    y += 17
    stat_row("Nodes visited:", nodes_visited if nodes_visited else "—")
    y += 17
    stat_row("Time (ms):", f"{elapsed_ms:.1f}" if elapsed_ms else "—")
    y += 20

    win.blit(line_surf, (px + 10, y)); y += 10

    sec4 = FONT_SMALL.render("LEGEND", True, TEXT_DIM)
    win.blit(sec4, (px + 12, y)); y += 16
    legends = [
        (C_START,   "Start"),
        (C_END,     "End"),
        (C_BARRIER, "Wall"),
        (C_OPEN,    "Frontier"),
        (C_CLOSED,  "Visited"),
        (C_PATH,    "Path"),
    ]
    for col, lbl in legends:
        draw_legend_dot(win, px + 12, y, col, lbl)
        y += 18

    y += 8
    win.blit(line_surf, (px + 10, y)); y += 10

    how = FONT_SMALL.render("HOW TO USE", True, TEXT_DIM)
    win.blit(how, (px + 12, y)); y += 16
    tips = [
        ("LClick", "Draw / place"),
        ("RClick", "Erase"),
    ]
    for k, v in tips:
        kt = FONT_KEY.render(k, True, ACCENT2)
        vt = FONT_SMALL.render(v, True, TEXT_DIM)
        win.blit(kt, (px + 12, y))
        win.blit(vt, (px + 12 + kt.get_width() + 8, y + 1))
        y += 16

    status_colors = {
        "idle":    TEXT_DIM,
        "running": TEXT_WARN,
        "done":    ACCENT2,
        "none":    (180, 60, 60),
    }
    sc = status_colors.get(status[0], TEXT_DIM)
    sb_rect = pygame.Rect(px + 10, HEIGHT - 34, PANEL_W - 20, 24)
    pygame.draw.rect(win, BTN_IDLE, sb_rect, border_radius=5)
    pygame.draw.rect(win, sc, sb_rect, 1, border_radius=5)
    st = FONT_SMALL.render(status[1], True, sc)
    win.blit(st, (sb_rect.centerx - st.get_width()//2,
                  sb_rect.centery - st.get_height()//2))


def draw_all(win, grid, rows, buttons, status, path_length, algo_name,
             nodes_visited, elapsed_ms):
    win.fill(BG)

    gap = GRID_SIZE // rows
    for i in range(rows + 1):
        pygame.draw.line(win, C_GRID_LINE, (0, i*gap), (GRID_SIZE, i*gap))
        pygame.draw.line(win, C_GRID_LINE, (i*gap, 0), (i*gap, GRID_SIZE))

    for row in grid:
        for node in row:
            node.draw(win)

    draw_panel(win, buttons, status, path_length, algo_name,
               nodes_visited, elapsed_ms)
    pygame.display.update()

def main():
    grid  = make_grid(ROWS)
    start = None
    end   = None

    path_length    = 0
    nodes_visited  = 0
    algo_name      = ""
    elapsed_ms     = 0.0
    status         = ("idle", "Click grid to place start & end")

    bfs_btn  = Button((0,0, 0, 38), "Breadth-First",  "B")
    dijk_btn = Button((0,0, 0, 38), "Dijkstra",        "D")
    clr_btn  = Button((0,0, 0, 38), "Clear Grid",      "C",  (80, 30, 30))
    buttons  = [bfs_btn, dijk_btn, clr_btn]

    clock = pygame.time.Clock()
    run   = True

    def draw_fn():
        draw_all(WIN, grid, ROWS, buttons, status, path_length,
                 algo_name, nodes_visited, elapsed_ms)

    while run:
        clock.tick(120)
        mx, my = pygame.mouse.get_pos()
        for btn in buttons:
            btn.check_hover((mx, my))

        draw_all(WIN, grid, ROWS, buttons, status, path_length,
                 algo_name, nodes_visited, elapsed_ms)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] < GRID_SIZE:
                    r, c = get_clicked_pos(pos, ROWS)
                    node = grid[r][c]
                    if not start and node != end:
                        start = node; start.make_start()
                        status = ("idle", "Now place the end node")
                    elif not end and node != start:
                        end = node; end.make_end()
                        status = ("idle", "Draw walls, then run algo")
                    elif node not in (start, end):
                        node.make_barrier()
                elif pos[0] >= GRID_SIZE:
                    for btn in buttons:
                        if btn.is_clicked(pos):
                            if btn == clr_btn:
                                start = end = None
                                path_length = nodes_visited = 0
                                algo_name = ""; elapsed_ms = 0.0
                                grid = make_grid(ROWS)
                                for b in buttons: b.active = False
                                status = ("idle", "Grid cleared")
                            elif btn in (bfs_btn, dijk_btn) and start and end:
                                for row in grid:
                                    for node in row: node.update_neighbors(grid)
                                for b in buttons: b.active = False
                                btn.active = True
                                if btn == bfs_btn:
                                    algo_name = "BFS"
                                    status = ("running", "BFS running…")
                                    draw_fn()
                                    t0 = pygame.time.get_ticks()
                                    path_length = bfs(draw_fn, start, end)
                                    elapsed_ms  = pygame.time.get_ticks() - t0
                                else:
                                    algo_name = "Dijkstra"
                                    status = ("running", "Dijkstra running…")
                                    draw_fn()
                                    t0 = pygame.time.get_ticks()
                                    path_length = dijkstra(draw_fn, grid, start, end)
                                    elapsed_ms  = pygame.time.get_ticks() - t0
                            
                                nv = sum(1 for row in grid for n in row
                                         if n.color in (C_CLOSED, C_PATH))
                                nodes_visited = nv
                                if path_length:
                                    status = ("done",
                                              f"Done! Path = {path_length} steps")
                                else:
                                    status = ("none", "No path found!")

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if pos[0] < GRID_SIZE:
                    r, c = get_clicked_pos(pos, ROWS)
                    node = grid[r][c]
                    node.reset()
                    if node == start: start = None
                    elif node == end:  end   = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and start and end:
                    for row in grid:
                        for node in row: node.update_neighbors(grid)
                    for b in buttons: b.active = False
                    bfs_btn.active = True
                    algo_name = "BFS"
                    status = ("running", "BFS running…")
                    draw_fn()
                    t0 = pygame.time.get_ticks()
                    path_length = bfs(draw_fn, start, end)
                    elapsed_ms  = pygame.time.get_ticks() - t0
                    nv = sum(1 for row in grid for n in row
                             if n.color in (C_CLOSED, C_PATH))
                    nodes_visited = nv
                    status = ("done", f"Done! Path = {path_length} steps") \
                             if path_length else ("none", "No path found!")

                elif event.key == pygame.K_d and start and end:
                    for row in grid:
                        for node in row: node.update_neighbors(grid)
                    for b in buttons: b.active = False
                    dijk_btn.active = True
                    algo_name = "Dijkstra"
                    status = ("running", "Dijkstra running…")
                    draw_fn()
                    t0 = pygame.time.get_ticks()
                    path_length = dijkstra(draw_fn, grid, start, end)
                    elapsed_ms  = pygame.time.get_ticks() - t0
                    nv = sum(1 for row in grid for n in row
                             if n.color in (C_CLOSED, C_PATH))
                    nodes_visited = nv
                    status = ("done", f"Done! Path = {path_length} steps") \
                             if path_length else ("none", "No path found!")

                elif event.key == pygame.K_c:
                    start = end = None
                    path_length = nodes_visited = 0
                    algo_name = ""; elapsed_ms = 0.0
                    grid = make_grid(ROWS)
                    for b in buttons: b.active = False
                    status = ("idle", "Grid cleared")

    pygame.quit()


main()