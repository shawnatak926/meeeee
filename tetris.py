import pygame
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BLOCK_WIDTH, BLOCK_HEIGHT = 50, 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Ball:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.dx = 4 * random.choice([-1, 1])
        self.dy = -4
        self.rect = pygame.Rect(self.x, self.y, BALL_SIZE, BALL_SIZE)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x, self.y)

    def bounce(self):
        if self.x <= 0 or self.x >= WINDOW_WIDTH - BALL_SIZE:
            self.dx *= -1
        if self.y <= 0:
            self.dy *= -1


class Paddle:
    def __init__(self):
        self.x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2
        self.y = WINDOW_HEIGHT - 40
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dx):
        self.x += dx
        self.x = max(0, min(WINDOW_WIDTH - PADDLE_WIDTH, self.x))
        self.rect.topleft = (self.x, self.y)


class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


def create_blocks():
    blocks = []
    for i in range(5):
        for j in range(8):
            blocks.append(Block(j * (BLOCK_WIDTH + 5) + 10, i * (BLOCK_HEIGHT + 5) + 10))
    return blocks


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    ball = Ball()
    paddle = Paddle()
    blocks = create_blocks()
    running = True
    score = 0
    font = pygame.font.Font(None, 36)

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-6)
        if keys[pygame.K_RIGHT]:
            paddle.move(6)

        ball.move()
        ball.bounce()

        if ball.rect.colliderect(paddle.rect):
            ball.dy *= -1
            score += 1

        for block in blocks[:]:
            if ball.rect.colliderect(block.rect):
                blocks.remove(block)
                ball.dy *= -1
                score += 5

        if not blocks:
            blocks = create_blocks()

        if ball.y >= WINDOW_HEIGHT:
            ball = Ball()
            score = 0
            blocks = create_blocks()

        pygame.draw.rect(screen, WHITE, paddle.rect)
        pygame.draw.ellipse(screen, WHITE, ball.rect)

        for block in blocks:
            block.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main() 