import random
import pygame

# Constants
SCREEN_WIDTH = 800
PIXEL_WIDTH = 50
SOUND = True

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
clock = pygame.time.Clock()

pygame.display.set_caption("PySnake")
font = pygame.font.Font('font/Minecraft.ttf', 25)
pygame.mixer.music.load('Music/Snake game.wav')


def random_starting_position():
    """Generate a random starting position within the screen."""
    random_range = (PIXEL_WIDTH // 2, SCREEN_WIDTH - PIXEL_WIDTH // 2, PIXEL_WIDTH)
    return [random.randrange(*random_range), random.randrange(*random_range)]


def is_out_of_bound(rect):
    """Check if a rectangle is out of the screen bounds."""
    return rect.bottom > SCREEN_WIDTH or rect.top < 0 or rect.right > SCREEN_WIDTH or rect.left < 0


def display_score(score):
    """Display the current score on the screen."""
    score_text = font.render(f'score: {score}', False, (64, 64, 64))
    screen.blit(score_text, (20, 20))


# Snake setup
snake_bit = pygame.rect.Rect([0, 0, PIXEL_WIDTH - 2, PIXEL_WIDTH - 2])
snake_bit.center = random_starting_position()
snake = [snake_bit.copy()]
snake_direction = (0, 0)
snake_length = 1

# apple setup
apple = pygame.rect.Rect([0, 0, PIXEL_WIDTH - 2, PIXEL_WIDTH - 2])
apple.center = random_starting_position()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Screen
    screen.fill("yellow")
    display_score(snake_length)

    if SOUND:
        pygame.mixer.music.play()
        SOUND = False

    # Game logic
    if is_out_of_bound(snake_bit) or snake_bit.collidelist(snake[:-1]) != -1:
        SOUND = True
        snake_length = 1
        apple.center = random_starting_position()
        snake_bit.center = random_starting_position()
        snake = [snake_bit.copy()]

    if snake_bit.center == apple.center:
        apple.center = random_starting_position()
        snake_length += 1
        snake.append(snake_bit.copy())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        snake_direction = (0, -PIXEL_WIDTH)
    if keys[pygame.K_s]:
        snake_direction = (0, PIXEL_WIDTH)
    if keys[pygame.K_a]:
        snake_direction = (-PIXEL_WIDTH, 0)
    if keys[pygame.K_d]:
        snake_direction = (PIXEL_WIDTH, 0)

    for snake_part in snake:
        pygame.draw.rect(screen, "blue", snake_part)
    pygame.draw.rect(screen, "red", apple)

    # Snake movement
    snake_bit.move_ip(snake_direction)
    snake.append(snake_bit.copy())
    snake = snake[-snake_length:]

    # Display update
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
