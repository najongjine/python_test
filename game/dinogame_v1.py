import pygame  # 게임용 라이브러리
import sys     # 시스템 종료 등을 위한 라이브러리

# ▶ Pygame 초기화
pygame.init()

# ▶ 화면 크기 설정
WIDTH, HEIGHT = 800, 400  # 가로 800, 세로 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 게임 화면 생성
pygame.display.set_caption("Jumping Dino")         # 윈도우 상단 타이틀 설정
clock = pygame.time.Clock()                        # 프레임 속도 제어용 시계 객체

# ▶ 색상 정의 (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ▶ 공룡 (플레이어) 설정
dino_width, dino_height = 50, 50           # 크기
dino_x = 50                                 # x좌표 (고정됨, 왼쪽에서 시작)
dino_y = HEIGHT - dino_height               # y좌표 (땅에 붙은 위치)
dino_velocity = 0                           # 점프 속도
gravity = 0.5                               # 중력 값
jump_strength = -10                         # 점프 시 위로 올라갈 힘 (음수)
is_jumping = False                          # 점프 중인지 여부

# ▶ 장애물 설정
obstacle_width, obstacle_height = 20, 50   # 장애물 크기
obstacle_x = WIDTH                         # 시작 위치 (오른쪽 끝)
obstacle_y = HEIGHT - obstacle_height      # 땅에 붙인 y 위치
obstacle_speed = 5                         # 장애물이 왼쪽으로 움직이는 속도

# ▶ 게임 루프 시작
running = True
while running:
    screen.fill(WHITE)  # 화면을 하얀색으로 지움 (매 프레임 초기화)

    # [1] 이벤트 처리 (종료 감지)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # 창을 닫으면 게임 종료

    # [2] 키 입력 처리 (스페이스바로 점프)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        dino_velocity = jump_strength  # 위로 튀게 만듬
        is_jumping = True              # 점프 중이라고 표시

    # [3] 공룡의 y 위치 계산 (중력 적용)
    dino_velocity += gravity          # 중력을 매 프레임마다 추가
    dino_y += dino_velocity           # y 좌표 갱신
    if dino_y >= HEIGHT - dino_height:
        dino_y = HEIGHT - dino_height  # 땅에 닿으면 멈춤
        is_jumping = False             # 다시 점프 가능

    # [4] 장애물 왼쪽으로 이동시키기
    obstacle_x -= obstacle_speed
    if obstacle_x < 0:
        obstacle_x = WIDTH  # 왼쪽 끝까지 가면 다시 오른쪽에서 등장

    # [5] 충돌 검사 (사각형 기준)
    dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    if dino_rect.colliderect(obstacle_rect):
        print("충돌! 게임 오버")
        running = False  # 게임 루프 종료

    # [6] 캐릭터와 장애물 화면에 그리기
    pygame.draw.rect(screen, BLACK, dino_rect)       # 공룡
    pygame.draw.rect(screen, BLACK, obstacle_rect)   # 장애물

    # [7] 화면 업데이트
    pygame.display.update()
    clock.tick(60)  # 초당 60 프레임 유지
