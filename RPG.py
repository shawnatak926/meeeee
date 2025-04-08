import pygame
import sys
import heapq

# 초기화
pygame.init()

# 화면 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("MOBA Game")

# 색상
green = (0, 255, 0)
gray = (169, 169, 169)  # 벽 색상
black = (0, 0, 0)  # 배경 색상
white = (255, 255, 255)  # 경로 색상

# 캐릭터 설정
character_pos = [width // 2, height // 2]
character_radius = 10
speed = 0.2

target_pos = character_pos[:]

# 벽 설정 (2개의 벽)
walls = [
    pygame.Rect(200, 150, 400, 50),  # 가로 벽
    pygame.Rect(200, 400, 400, 50)   # 가로 벽
]

clock = pygame.time.Clock()

# A* 알고리즘을 위한 유틸리티 함수들
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def is_valid_pos(pos, walls, width, height):
    if pos[0] < 0 or pos[0] >= width or pos[1] < 0 or pos[1] >= height:
        return False
    for wall in walls:
        if wall.collidepoint(pos):
            return False
    return True

def a_star(start, goal, walls, width, height):
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, goal), 0, start, None))  # (f, g, current_pos, parent)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_list:
        _, g, current, parent = heapq.heappop(open_list)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 상, 하, 좌, 우
            neighbor = (current[0] + dx, current[1] + dy)
            if is_valid_pos(neighbor, walls, width, height):
                tentative_g_score = g + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], tentative_g_score, neighbor, current))
    return []

# 경로 계산
path = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            target_pos = list(event.pos)
            path = a_star((int(character_pos[0]), int(character_pos[1])), target_pos, walls, width, height)

    # 경로를 따라 이동
    if path:
        next_point = path[0]
        dx = next_point[0] - character_pos[0]
        dy = next_point[1] - character_pos[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 1:
            character_pos[0] += dx / distance * speed * clock.get_time()
            character_pos[1] += dy / distance * speed * clock.get_time()
        else:
            path.pop(0)

    # 화면 그리기
    screen.fill(black)  # 배경 색상 설정

    # 벽 그리기
    for wall in walls:
        pygame.draw.rect(screen, gray, wall)

    # 경로 그리기
    for point in path:
        pygame.draw.circle(screen, white, point, 5)

    # 캐릭터 그리기
    pygame.draw.circle(screen, green, (int(character_pos[0]), int(character_pos[1])), character_radius)

    pygame.display.flip()
    clock.tick(60)
