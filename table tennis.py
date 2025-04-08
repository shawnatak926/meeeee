import pygame
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Ball:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.dx = 6 * random.choice([-1, 1])
        self.dy = 6 * random.choice([-1, 1])
        self.rect = pygame.Rect(self.x, self.y, BALL_SIZE, BALL_SIZE)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x, self.y)

    def bounce(self):
        if self.y <= 0 or self.y >= WINDOW_HEIGHT - BALL_SIZE:
            self.dy *= -1

    def reset(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.dx *= -1
        self.dy *= random.choice([-1, 1])
        self.rect.topleft = (self.x, self.y)


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dy):
        self.y += dy
        self.y = max(0, min(WINDOW_HEIGHT - PADDLE_HEIGHT, self.y))
        self.rect.topleft = (self.x, self.y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    ball = Ball()
    left_paddle = Paddle(10, (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2)
    right_paddle = Paddle(WINDOW_WIDTH - 20, (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2)
    left_score = 0
    right_score = 0
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move(-6)
        if keys[pygame.K_s]:
            left_paddle.move(6)
        if keys[pygame.K_UP]:
            right_paddle.move(-6)
        if keys[pygame.K_DOWN]:
            right_paddle.move(6)

        ball.move()
        ball.bounce()

        if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
            ball.dx *= -1.1  # Increase speed slightly on paddle hit

        if ball.x <= 0:
            right_score += 1
            ball.reset()
        elif ball.x >= WINDOW_WIDTH:
            left_score += 1
            ball.reset()

        pygame.draw.rect(screen, WHITE, left_paddle.rect)
        pygame.draw.rect(screen, WHITE, right_paddle.rect)
        pygame.draw.ellipse(screen, WHITE, ball.rect)
        pygame.draw.aaline(screen, WHITE, (WINDOW_WIDTH // 2, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT))

        score_text = font.render(f"{left_score} - {right_score}", True, WHITE)
        screen.blit(score_text, (WINDOW_WIDTH // 2 - 30, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
