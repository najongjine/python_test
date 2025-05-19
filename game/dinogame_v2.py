import pygame
import sys

# ▶ Pygame 초기화
pygame.init()

# ▶ 화면 설정
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumping Dino")
clock = pygame.time.Clock()

# ▶ 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ▶ Dino 클래스 정의
class Dino:
    def __init__(self, x, y, width, height, gravity=0.5, jump_strength=-10):
        # 위치와 크기
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # 점프 관련 속성
        self.gravity = gravity
        self.jump_strength = jump_strength
        self.velocity = 0
        self.is_jumping = False

    def handle_input(self):
        # 스페이스바를 누르면 점프
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity = self.jump_strength
            self.is_jumping = True

    def update(self):
        # 점프 및 낙하 처리
        self.velocity += self.gravity
        self.y += self.velocity

        # 땅에 닿으면 다시 점프 가능하게 처리
        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.is_jumping = False

    def draw(self, surface):
        # 화면에 공룡 그리기
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# ▶ Obstacle 클래스 정의
class Obstacle:
    def __init__(self, x, y, width, height, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def update(self):
        # 왼쪽으로 계속 이동
        self.x -= self.speed
        if self.x < 0:
            self.x = WIDTH  # 다시 오른쪽으로 돌아감

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# ▶ 인스턴스 생성
dino = Dino(x=50, y=HEIGHT - 50, width=50, height=50)
obstacle = Obstacle(x=WIDTH, y=HEIGHT - 50, width=20, height=50)

# ▶ 메인 게임 루프
running = True
while running:
    screen.fill(WHITE)

    # 1. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. 공룡 입력 및 움직임 처리
    dino.handle_input()
    dino.update()

    # 3. 장애물 이동
    obstacle.update()

    # 4. 충돌 검사
    if dino.get_rect().colliderect(obstacle.get_rect()):
        print("충돌! 게임 오버")
        running = False

    # 5. 화면에 오브젝트 그리기
    dino.draw(screen)
    obstacle.draw(screen)

    # 6. 화면 갱신
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
