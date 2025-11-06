import pygame, sys, random, os, json

# ========== CONFIGURATION ==========
WIDTH, HEIGHT, CELL_SIZE = 600, 400, 20
FPS = 10
DATA_FILE = "scores.json"

BLACK, GREEN, DARK_GREEN, RED, GRAY, WHITE = (
    (0, 0, 0),
    (0, 255, 0),
    (0, 180, 0),
    (255, 0, 0),
    (40, 40, 40),
    (255, 255, 255)
)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game App")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)
small_font = pygame.font.SysFont("consolas", 16)
big_font = pygame.font.SysFont("consolas", 48, bold=True)

# ========== DATA MANAGEMENT ==========
def load_scores():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_score(score):
    scores = load_scores()
    scores.append(score)
    scores = sorted(scores, reverse=True)[:10]
    with open(DATA_FILE, "w") as f:
        json.dump(scores, f)

# ========== DRAW GRID ==========
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

# ========== LEADERBOARD SCREEN ==========
def show_leaderboard():
    scores = load_scores()
    running = True
    while running:
        screen.fill(BLACK)
        title = big_font.render("LEADERBOARD", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        for i, s in enumerate(scores):
            text = font.render(f"{i+1}. {s}", True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 150 + i*30))
        info = small_font.render("Press ESC to return to menu", True, WHITE)
        screen.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT-50))

        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

# ========== GAME OVER SCREEN ==========
def game_over_screen(score):
    save_score(score)
    scores = load_scores()
    running = True
    while running:
        screen.fill(BLACK)
        text1 = big_font.render("GAME OVER", True, WHITE)
        text2 = font.render(f"Your Score: {score}", True, WHITE)
        text3 = small_font.render("Press ENTER to play again or ESC to menu", True, WHITE)
        screen.blit(text1, (WIDTH//2 - text1.get_width()//2, 100))
        screen.blit(text2, (WIDTH//2 - text2.get_width()//2, 180))
        screen.blit(text3, (WIDTH//2 - text3.get_width()//2, 260))
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play_game()
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

# ========== MAIN MENU ==========
def main_menu():
    running = True
    while running:
        screen.fill(BLACK)
        title = big_font.render("SNAKE GAME", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        play_text = font.render("1. Play Game", True, WHITE)
        board_text = font.render("2. Leaderboard", True, WHITE)
        exit_text = font.render("3. Exit", True, WHITE)
        screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, 180))
        screen.blit(board_text, (WIDTH//2 - board_text.get_width()//2, 220))
        screen.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, 260))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_game()
                elif event.key == pygame.K_2:
                    show_leaderboard()
                elif event.key == pygame.K_3 or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# ========== GAMEPLAY ==========
def play_game():
    snake = [(100, 100), (80, 100), (60, 100)]
    snake_dir = (CELL_SIZE, 0)
    food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
    score = 0
    highscore = max(load_scores()) if load_scores() else 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                    snake_dir = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                    snake_dir = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                    snake_dir = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                    snake_dir = (CELL_SIZE, 0)

        # Move snake with wrap
        new_head = ((snake[0][0] + snake_dir[0]) % WIDTH, (snake[0][1] + snake_dir[1]) % HEIGHT)
        snake.insert(0, new_head)

        # Check food collision
        if new_head == food:
            score += 10
            food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            if score > highscore:
                highscore = score
        else:
            snake.pop()

        # Self collision
        if new_head in snake[1:]:
            game_over_screen(score)
            return

        # Draw everything
        screen.fill(BLACK)
        draw_grid()

        for i, block in enumerate(snake):
            color = DARK_GREEN if i % 2 == 0 else GREEN
            pygame.draw.rect(screen, color, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

        # Draw scores
        score_text = font.render(f"Score: {score}", True, WHITE)
        highscore_text = small_font.render(f"High Score: {highscore}", True, WHITE)
        screen.blit(score_text, (10, 5))
        screen.blit(highscore_text, (10, 35))

        pygame.display.flip()
        clock.tick(FPS)

# ========== RUN ==========
if __name__ == "__main__":
    main_menu()
