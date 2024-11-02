import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Shapes of the Tetriminos
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1],
     [1, 1]],
    [[0, 1, 0],
     [1, 1, 1]],
    [[1, 0, 0],
     [1, 1, 1]],
    [[0, 0, 1],
     [1, 1, 1]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 1],
     [1, 1, 0]]
]

# Colors for each shape
SHAPE_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

# Game variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# The Grid
grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]

# Tetrimino class
class Tetrimino:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(SHAPE_COLORS)
        self.x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, pygame.Rect((self.x + j) * BLOCK_SIZE, (self.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Check if position is valid
def valid_space(tetrimino, offset_x, offset_y):
    for i, row in enumerate(tetrimino.shape):
        for j, cell in enumerate(row):
            if cell:
                new_x = tetrimino.x + j + offset_x
                new_y = tetrimino.y + i + offset_y
                if new_x < 0 or new_x >= SCREEN_WIDTH // BLOCK_SIZE or new_y >= SCREEN_HEIGHT // BLOCK_SIZE:
                    return False
                if new_y >= 0 and grid[new_y][new_x] != BLACK:
                    return False
    return True

# Add Tetrimino to the grid
def merge_tetrimino(tetrimino):
    for i, row in enumerate(tetrimino.shape):
        for j, cell in enumerate(row):
            if cell:
                grid[tetrimino.y + i][tetrimino.x + j] = tetrimino.color

# Remove completed lines
def clear_lines():
    global grid
    grid = [row for row in grid if any(cell == BLACK for cell in row)]
    while len(grid) < SCREEN_HEIGHT // BLOCK_SIZE:
        grid.insert(0, [BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])

def main():
    current_tetrimino = Tetrimino(random.choice(SHAPES))
    running = True
    fall_time = 0
    fall_speed = 500  # milliseconds per block fall

    while running:
        screen.fill(BLACK)
        fall_time += clock.get_time()

        # Falling mechanism
        if fall_time >= fall_speed:
            if valid_space(current_tetrimino, 0, 1):
                current_tetrimino.y += 1
            else:
                merge_tetrimino(current_tetrimino)
                clear_lines()
                current_tetrimino = Tetrimino(random.choice(SHAPES))
                if not valid_space(current_tetrimino, 0, 0):
                    running = False  # Game Over
            fall_time = 0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and valid_space(current_tetrimino, -1, 0):
                    current_tetrimino.x -= 1
                if event.key == pygame.K_RIGHT and valid_space(current_tetrimino, 1, 0):
                    current_tetrimino.x += 1
                if event.key == pygame.K_DOWN and valid_space(current_tetrimino, 0, 1):
                    current_tetrimino.y += 1
                if event.key == pygame.K_UP:
                    current_tetrimino.rotate()
                    if not valid_space(current_tetrimino, 0, 0):
                        current_tetrimino.rotate()  # Rotate back if not valid

        # Draw grid
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell != BLACK:
                    pygame.draw.rect(screen, cell, pygame.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Draw current Tetrimino
        current_tetrimino.draw()

        # Update the screen
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
