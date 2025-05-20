import pygame  # 게임용 라이브러리
import sys     # 시스템 종료 등을 위한 라이브러리

# ▶ Pygame 초기화
pygame.init()

# ▶ 화면 크기 설정
WIDTH, HEIGHT = 800, 400  # 가로 800, 세로 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 게임 화면 생성

# ▶ 색상 정의 (RGB)
WHITE = (255, 255, 255)
clock = pygame.time.Clock()    

# ▶ 게임 루프 시작
running = True
while running:
    screen.fill(WHITE)  # 화면을 하얀색으로 지움 (매 프레임 초기화)

    # 1. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # [7] 화면 업데이트
    pygame.display.update()
    clock.tick(60)  # 초당 60 프레임 유지

pygame.quit()
sys.exit()