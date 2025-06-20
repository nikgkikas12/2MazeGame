import pygame
import sys
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 20
COLS, ROWS = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE

best_time = 10000  # υψηλό σκορ σε δευτερόλεπτα

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Duel Test")

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 24)

# Πλέγμα (maze): 0 = κενό, 1 = τοίχος
maze = [[0 if x % 2 == 1 or y % 2 == 1 else 1 for x in range(COLS)] for y in range(ROWS)]
for x in range(10, 30):
    maze[15][x] = 1
for y in range(10, 25):
    maze[y][20] = 1

# Αρχικές θέσεις
p1 = [0, 0]              # WASD
p2 = [COLS - 1, 0]       # Arrows
goal = [COLS // 2, ROWS - 1]

start_time = time.time()
winner = None

def move(pos, dx, dy):
    new_x = pos[0] + dx
    new_y = pos[1] + dy
    if 0 <= new_x < COLS and 0 <= new_y < ROWS:
        if maze[new_y][new_x] == 0:
            pos[0], pos[1] = new_x, new_y

clock = pygame.time.Clock()
run = True

while run:
    clock.tick(60)
    screen.fill(BLACK)

    # Σχεδίαση πλέγματος
    for y in range(ROWS):
        for x in range(COLS):
            color = WHITE if maze[y][x] == 1 else BLACK
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Σχεδίαση παικτών και τερματισμού
    pygame.draw.rect(screen, GREEN, (goal[0]*TILE_SIZE, goal[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, RED, (p1[0]*TILE_SIZE, p1[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, BLUE, (p2[0]*TILE_SIZE, p2[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Έλεγχος για νικητή
    if not winner:
        if p1 == goal:
            winner = "Player 1 (Red)"
        elif p2 == goal:
            winner = "Player 2 (Blue)"
        if winner:
            elapsed_time = round(time.time() - start_time, 2)
            if elapsed_time < best_time:
                best_time = elapsed_time
                print("🎉 New High Score!")

    # Εμφάνιση αποτελέσματος
    if winner:
        text = font.render(f"Winner: {winner}, Time: {best_time} sec", True, BLACK)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and not winner:
            # Παίκτης 1 (WASD)
            if event.key == pygame.K_w: move(p1, 0, -1)
            elif event.key == pygame.K_s: move(p1, 0, 1)
            elif event.key == pygame.K_a: move(p1, -1, 0)
            elif event.key == pygame.K_d: move(p1, 1, 0)
            # Παίκτης 2 (Arrow keys)
            elif event.key == pygame.K_UP: move(p2, 0, -1)
            elif event.key == pygame.K_DOWN: move(p2, 0, 1)
            elif event.key == pygame.K_LEFT: move(p2, -1, 0)
            elif event.key == pygame.K_RIGHT: move(p2, 1, 0)

pygame.quit()
sys.exit()
