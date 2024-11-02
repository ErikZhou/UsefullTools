import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置游戏窗口
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (128, 128, 128)
]

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# 游戏参数
cell_size = 30
board_width = 10
board_height = 20
board = [[0] * board_width for _ in range(board_height)]

# 当前方块
current_shape = None
current_x = 0
current_y = 0
current_color = None

# 游戏循环
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5
game_over = False

def new_shape():
    global current_shape, current_x, current_y, current_color
    current_shape = random.choice(SHAPES)
    current_x = board_width // 2 - len(current_shape[0]) // 2
    current_y = 0
    current_color = random.choice(COLORS)

def check_collision(shape, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                if (y + i >= board_height or
                    x + j < 0 or x + j >= board_width or
                    board[y + i][x + j]):
                    return True
    return False

def merge_shape():
    for i, row in enumerate(current_shape):
        for j, cell in enumerate(row):
            if cell:
                board[current_y + i][current_x + j] = current_color

def rotate_shape():
    global current_shape
    rotated = list(zip(*current_shape[::-1]))
    if not check_collision(rotated, current_x, current_y):
        current_shape = rotated

def clear_lines():
    global board
    full_lines = [i for i, row in enumerate(board) if all(row)]
    for line in full_lines:
        del board[line]
        board.insert(0, [0] * board_width)

def draw_board():
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (x * cell_size, y * cell_size, cell_size - 1, cell_size - 1))

def draw_shape():
    for i, row in enumerate(current_shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_color,
                                 ((current_x + j) * cell_size,
                                  (current_y + i) * cell_size,
                                  cell_size - 1, cell_size - 1))

new_shape()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not check_collision(current_shape, current_x - 1, current_y):
                current_x -= 1
            if event.key == pygame.K_RIGHT and not check_collision(current_shape, current_x + 1, current_y):
                current_x += 1
            if event.key == pygame.K_DOWN and not check_collision(current_shape, current_x, current_y + 1):
                current_y += 1
            if event.key == pygame.K_UP:
                rotate_shape()

    fall_time += clock.get_rawtime()
    clock.tick()

    if fall_time / 1000 > fall_speed:
        if not check_collision(current_shape, current_x, current_y + 1):
            current_y += 1
        else:
            merge_shape()
            clear_lines()
            new_shape()
            if check_collision(current_shape, current_x, current_y):
                game_over = True
        fall_time = 0

    screen.fill(BLACK)
    draw_board()
    draw_shape()
    pygame.display.flip()

pygame.quit()
