import pygame
import sys
import random
import math

# 초기 설정
pygame.init()
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# 색상 정의
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 게임 속도
clock = pygame.time.Clock()

# 점수 변수
score = 0
font = pygame.font.SysFont(None, 36)

# 맵 데이터 (1: 벽, 0: 빈 공간)
map_data = {
    (x, y): 1 for x in range(WIDTH // TILE_SIZE) for y in range(HEIGHT // TILE_SIZE) if x == 0 or x == (WIDTH // TILE_SIZE) - 1 or y == 0 or y == (HEIGHT // TILE_SIZE) - 1
}
map_data.update({
    (1, 1): 0, (28, 1): 0, (1, 28): 0, (28, 28): 0,
    (10, 15): 0, (15, 10): 0, (20, 20): 0
})

# 먹이 생성 함수
def spawn_food():
    while True:
        x = random.randint(1, (WIDTH // TILE_SIZE) - 2)
        y = random.randint(1, (HEIGHT // TILE_SIZE) - 2)
        if map_data.get((x, y)) == 0:
            return x * TILE_SIZE, y * TILE_SIZE

food_x, food_y = spawn_food()

# 팩맨 클래스
class Pacman:
    def __init__(self):
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.speed = TILE_SIZE
        self.direction = pygame.K_RIGHT

    def move(self):
        new_x, new_y = self.x, self.y
        if self.direction == pygame.K_UP:
            new_y -= self.speed
        elif self.direction == pygame.K_DOWN:
            new_y += self.speed
        elif self.direction == pygame.K_LEFT:
            new_x -= self.speed
        elif self.direction == pygame.K_RIGHT:
            new_x += self.speed

        # 화면 밖으로 나가는 것 방지
        if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
            return

        # 벽 충돌 검사
        if map_data.get((new_x // TILE_SIZE, new_y // TILE_SIZE), 0) == 0:
            self.x, self.y = new_x, new_y

    def draw(self):
        # 팩맨 몸체
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), TILE_SIZE // 2)
        # 팩맨 입
        mouth_angle = math.pi / 3.5
        if self.direction == pygame.K_RIGHT:
            start_angle = -mouth_angle
        elif self.direction == pygame.K_LEFT:
            start_angle = math.pi - mouth_angle
        elif self.direction == pygame.K_UP:
            start_angle = 1.5 * math.pi - mouth_angle
        elif self.direction == pygame.K_DOWN:
            start_angle = 0.5 * math.pi - mouth_angle
        pygame.draw.polygon(screen, BLACK, [
            (self.x, self.y),
            (self.x + int(TILE_SIZE * math.cos(start_angle)), self.y + int(TILE_SIZE * math.sin(start_angle))),
            (self.x + int(TILE_SIZE * math.cos(start_angle + 2 * mouth_angle)), self.y + int(TILE_SIZE * math.sin(start_angle + 2 * mouth_angle)))
        ])

# 벽 그리기 함수
def draw_walls():
    for (col, row), value in map_data.items():
        if value == 1:
            pygame.draw.rect(screen, WHITE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# 점수 표시 함수
def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# 게임 루프
pacman = Pacman()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pacman.direction = event.key

    pacman.move()

    # 팩맨이 먹이를 먹었는지 확인
    if pacman.x == food_x and pacman.y == food_y:
        score += 10
        food_x, food_y = spawn_food()

    screen.fill(BLACK)
    draw_walls()
    pacman.draw()
    # 먹이 그리기
    pygame.draw.circle(screen, RED, (food_x, food_y), TILE_SIZE // 4)
    draw_score()
    pygame.display.flip()
    clock.tick(10)