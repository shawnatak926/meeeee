import pygame
import time
import random

# 초기화
pygame.init()

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# 화면 크기 설정
width = 1600
height = 900

# 화면 생성
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# 스네이크 블록 크기 및 속도
block_size = 10
speed = 15

# 폰트 설정
font = pygame.font.SysFont("bahnschrift", 20)

# 점수 표시 함수
def display_score(score):
    value = font.render("Score: " + str(score), True, white)
    win.blit(value, [10, 10])

# 뱀을 그리는 함수
def draw_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(win, green, [block[0], block[1], block_size, block_size])

# 게임 루프
def game_loop():
    game_over = False
    game_close = False
    
    x = width / 2
    y = height / 2
    dx = 0
    dy = 0
    
    snake_list = []
    snake_length = 1
    
    food_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
    
    clock = pygame.time.Clock()
    
    while not game_over:
        while game_close:
            win.fill(black)
            message = font.render("Game Over! Press C-Play Again or Q-Quit", True, red)
            win.blit(message, [width / 6, height / 3])
            display_score(snake_length - 1)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -block_size
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = block_size
                    dy = 0
                elif event.key == pygame.K_UP:
                    dy = -block_size
                    dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = block_size
                    dx = 0
        
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True
        
        x += dx
        y += dy
        win.fill(black)
        pygame.draw.rect(win, red, [food_x, food_y, block_size, block_size])
        
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]
        
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True
        
        draw_snake(block_size, snake_list)
        display_score(snake_length - 1)
        pygame.display.update()
        
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
            snake_length += 1
        
        clock.tick(speed)
    
    pygame.quit()
    quit()

# 게임 시작
game_loop()