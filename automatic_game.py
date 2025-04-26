import pygame
import time
import random
from collections import defaultdict

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 25
ROWS, COLS = 24, 24
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BASE_MAX_LIFESPAN = 9  # Base lifespan in seconds
LIFESPAN_BONUS_PER_NEIGHBOR = 1  # Small bonus per neighbor

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Simulation with Community Lifespan")

# Initialize the grid, birth times, and history
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
birth_times = [[None for _ in range(COLS)] for _ in range(ROWS)]
history = defaultdict(list)  # Tracks lifespans of dead cells

# Function to count alive neighbors
def count_neighbors(grid, i, j):
    count = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:  # Skip the cell itself
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < ROWS and 0 <= nj < COLS and grid[ni][nj] == 1:
                count += 1
    return count

# Main simulation loop
running = True
clock = pygame.time.Clock()
start_time = time.time()
next_spawn_time = start_time + 0.2  # Spawn a cell every 0.2 seconds

while running:
    current_time = time.time()

    # Handle window close event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn a new cell every 2 seconds at a random empty position
    if current_time >= next_spawn_time:
        dead_cells = [(i, j) for i in range(ROWS) for j in range(COLS) if grid[i][j] == 0]
        if dead_cells:
            i, j = random.choice(dead_cells)
            grid[i][j] = 1
            birth_times[i][j] = current_time
        next_spawn_time += 0.2

    # Update alive cells based on dynamic lifespan
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i][j] == 1:
                neighbors = count_neighbors(grid, i, j)
                age = current_time - birth_times[i][j]

                # Calculate effective max lifespan with small weight from neighbors
                effective_max_lifespan = BASE_MAX_LIFESPAN + (neighbors * LIFESPAN_BONUS_PER_NEIGHBOR)

                # Check if the cell exceeds its effective max lifespan
                if age > effective_max_lifespan:
                    lifespan = age
                    history[(i, j)].append(lifespan)  # Record lifespan for history
                    grid[i][j] = 0
                    birth_times[i][j] = None

    # Draw the grid
    screen.fill(BLACK)
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i][j] == 1:
                pygame.draw.rect(screen, WHITE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()
    clock.tick(30)

# Clean up
pygame.quit()
