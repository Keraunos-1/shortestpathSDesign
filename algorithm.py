import tkinter as tk
import heapq
import math
import random

root = tk.Tk()
root.title("A* Pathfinding Visualizer")

root.configure(bg='white')

width, height = 30, 25
cell_size = 30
root.geometry('+520+100')

start_color = (255, 221, 0)
end_color = (235, 10, 30)

start = None
goal = None

is_setting_start = False
is_setting_goal = False
is_setting_wall = False
# This code defines a heuristic function that calculates the Euclidean distance
# between the given cell and a goal cell. If the goal is not provided, the function returns 0.
def heuristic(cell, goal):
    if goal is not None:
        return math.sqrt((cell[0] - goal[0])**2 + (cell[1] - goal[1])**2)
    else:
        return 0
#   This is an implementation of the A* search algorithm in Python. 
#   It finds the shortest path between a start and a goal on a grid by considering the cost to reach the current cell and an estimate of the cost to get from the current cell to the goal. 
#   The algorithm uses a priority queue to efficiently explore the grid and find the optimal path. The function returns the optimal path and a list of changes made during the search.
def a_star(grid, start, goal):
    open_set = [(0, start)]
    closed_set = set()
    paths = {start: (None, 0)}
    changes = []
    
    while open_set:
        _, current_cell = heapq.heappop(open_set)

        if current_cell == goal:
            path = []
            
            while current_cell:
                path.append(current_cell)
                current_cell, _ = paths[current_cell]
            return path[::-1], changes

        if current_cell in closed_set:
            continue

        closed_set.add(current_cell)

        changes.append((current_cell, 'closed_set'))
        
        for neighbor in get_neighbors(grid, current_cell):
            tentative_g = paths[current_cell][1] + 1

            if neighbor not in paths or tentative_g < paths[neighbor][1]:
                paths[neighbor] = (current_cell, tentative_g)
                f_value = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_value, neighbor))

                changes.append((neighbor, 'open_set'))

    return [], []
# This code snippet defines a function to get the neighbors of a cell in a grid. 
# It calculates the adjacent cells to the given cell and returns a list of valid neighboring cells that are not walls.
def get_neighbors(grid, cell):
    row, col = cell
    neighbors = [(row + 1, col),
                 (row - 1, col),
                 (row, col + 1),
                 (row, col - 1)]
    
    return [(r, c) for r, c in neighbors if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != 'wall']
# This code snippet defines a function draw_changes that takes a list of changes as input. 
# It iterates through the list and for each cell and cell_type pair in the changes
# it calculates the coordinates for a rectangle based on the cell's position and type
# and then draws the rectangle on a canvas with a fill color determined by the cell type.
def draw_changes(changes):
    
    for cell, cell_type in changes:
        x1, y1 = cell[1] * cell_size, cell[0] * cell_size
        x2, y2 = (cell[1] + 1) * cell_size, (cell[0] + 1) * cell_size
        
        if cell_type == 'open_set':
            color = '#fbaab1'
        elif cell_type == 'closed_set':
            color = '#fdd0d4'

        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#fbaab1')  #, activefill='#006b4e', activeoutline='#006b4e'
# This code defines a function draw_grid() that clears the canvas and then iterates over a grid
# drawing rectangles based on the cell type. After that, it runs the A* algorithm on the grid
# and draws the changes on the canvas
# and then draws a path on the canvas with gradient colors.        
def draw_grid():
    canvas.delete("all")
    for i in range(width):
        for j in range(height):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = (i + 1) * cell_size, (j + 1) * cell_size

            cell_type = grid[j][i]

            color = '#0066FF'
            if cell_type == 'start':
                color = '#FFDD00'
            elif cell_type == 'goal':
                color = '#eb0a1e'
            elif cell_type == 'wall':
                color = '#0c4da2'

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#0c4da2')
            
    path, changes = a_star(grid, start, goal)
    draw_changes(changes)  # Draw changes after A* is complete

    num_steps = len(path)

    for step, cell in enumerate(path):
        x1, y1 = cell[1] * cell_size + cell_size // 16, cell[0] * cell_size + cell_size // 16
        x2, y2 = (cell[1] + 1) * cell_size - cell_size // 16, (cell[0] + 1) * cell_size - cell_size // 16

        gradient_factor = step / (num_steps - 1)
        current_color = calculate_gradient_color(start_color,
                                                 end_color,
                                                 gradient_factor)
        print(current_color)
        hex_color = "#{:02X}{:02X}{:02X}".format(*current_color)

        canvas.create_rectangle(x1, y1, x2, y2, fill=hex_color, outline=hex_color)  
#, activefill='#006b4e', activeoutline='#006b4e'
# This code snippet defines a function that calculates a gradient color between two given colors based on a factor.
# It uses the start and end colors, and the factor to determine the intermediate color.       
def calculate_gradient_color(start_color, end_color, factor):
    return tuple(int(start + (end - start) * factor)
                 for start, end in zip(start_color, end_color))
# This code defines a function handle_mouse_click that takes an event as input.
# It determines the row and column of the clicked cell, and based on the state variables is_setting_start,
# is_setting_goal, and is_setting_wall, it performs different actions such as setting the start or goal cell,
# toggling a wall, or redrawing the grid.
def handle_mouse_click(event):
    global is_setting_start, is_setting_goal, is_setting_wall

    col = event.x // cell_size
    row = event.y // cell_size

    if 0 <= row < height and 0 <= col < width:
        if is_setting_start:
            if grid[row][col] == 'wall':
                return
            set_start(row, col)
        elif is_setting_goal:
            if grid[row][col] == 'wall':
                return
            set_goal(row, col)
            draw_grid()
        elif is_setting_wall:
            toggle_wall(row, col)

        if not is_setting_wall:
            draw_grid()
# This code defines a function set_start that updates the start position on a grid and redraws the grid.
# It uses a global variable start to keep track of the current start position and updates the grid accordingly.
def set_start(row, col):
    global start
    if start:
        grid[start[0]][start[1]] = 'empty'
    start = (row, col)
    grid[row][col] = 'start'
    draw_grid()
# This code snippet defines a function called set_goal which updates the global variable goal with the given row and col values.
# It also updates the grid to mark the new goal position and redraws the grid.
def set_goal(row, col):
    global goal
    if goal and 0 <= goal[0] < height and 0 <= goal[1] < width:
        grid[goal[0]][goal[1]] = 'empty'
    goal = (row, col)
    if grid and 0 <= row < height and 0 <= col < width:
        grid[row][col] = 'goal'
    draw_grid()
# This code defines a function toggle_wall that toggles the wall state of a cell in the grid and redraws the grid.
# It uses a global variable grid to keep track of the current grid state and updates the grid accordingly.
def toggle_wall(row, col):
    if grid[row][col] == 'wall':
        grid[row][col] = 'empty'
    else:
        grid[row][col] = 'wall'
    draw_grid()
# This code defines a function restart that clears the grid and redraws the grid.
# It also resets the global variables start and goal to None.
def restart():
    global start, goal
    start = None
    goal = None
    for i in range(height):
        for j in range(width):
            grid[i][j] = 'empty'
    draw_grid()
# This code defines a function set_mode that sets the mode to either 'start', 'goal', or 'wall' based on the given mode value.
# It also updates the global variables is_setting_start, is_setting_goal, and is_setting_wall.
def set_mode(mode):
    global is_setting_start, is_setting_goal, is_setting_wall
    is_setting_start = mode == 'start'
    is_setting_goal = mode == 'goal'
    is_setting_wall = mode == 'wall'
# This code defines a function generate_random_maze that generates a random maze on the grid and redraws the grid.
# It uses a global variable grid to keep track of the current grid state and updates the grid accordingly.
# It also resets the global variables start and goal to None.
def generate_random_maze():
    global start, goal
    start = None
    goal = None
    for i in range(height):
        for j in range(width):
            if random.random() < 0.2:
                grid[i][j] = 'wall'
            else:
                grid[i][j] = 'empty'
                
    draw_grid()
#write a description for all of this functions 
grid = [['empty' for _ in range(width)] for _ in range(height)]
canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size, bg='white')
canvas.pack()

draw_grid()

canvas.bind('<ButtonRelease-1>', handle_mouse_click)
canvas.bind('<B1-Motion>', handle_mouse_click)

button_font = ('Helvetica', 12, "bold")
start_button = tk.Button(root, text="Set Start",
                        font=button_font, bg='#9eb8da',
                        fg='#0c4da2', activebackground= '#3d71b5',
                        activeforeground='#eb0a1e',
                        command=lambda: set_mode('start'))
start_button.pack(side=tk.LEFT, padx=5)
goal_button = tk.Button(root, text="Set Goal",
                        font=button_font, bg='#9eb8da',
                        fg='#0c4da2', activebackground= '#3d71b5',
                        activeforeground='#eb0a1e',
                        command=lambda: set_mode('goal'))
goal_button.pack(side=tk.LEFT, padx=5)
wall_button = tk.Button(root, text="Toggle Wall",
                        font=button_font, bg='#9eb8da',
                        fg='#0c4da2', activebackground= '#3d71b5',
                        activeforeground='#eb0a1e',
                        command=lambda: set_mode('wall'))
wall_button.pack(side=tk.LEFT, padx=5)
random_maze_button = tk.Button(root, text="Random Maze",
                        font=button_font, bg='#9eb8da',
                        fg='#0c4da2', activebackground= '#3d71b5',
                        activeforeground='#eb0a1e',
                        command=generate_random_maze)
random_maze_button.pack(side=tk.LEFT, padx=5)
restart_button = tk.Button(root, text="Restart",
                        font=button_font, bg='#9eb8da',
                        fg='#0c4da2', activebackground= '#3d71b5',
                        activeforeground='#eb0a1e', command=restart)
restart_button.pack(side=tk.RIGHT, padx=5)

root.mainloop()