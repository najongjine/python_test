import pygame
import sys
import os

# 현재 스크립트 파일의 디렉토리로 변경
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

DINO_SPRITE_SIZE = (64, 64)
OBASTACLE_SPRITE_SIZE = (60, 50)

def get_resource_path(relative_path):
    """리소스 파일의 절대 경로를 반환합니다."""
    try:
        # PyInstaller로 빌드된 실행 파일의 경우
        base_path = sys._MEIPASS
    except AttributeError:
        # 개발 환경의 경우
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ▶ Dino 클래스 정의
class Dino(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.walk_images = [
    pygame.transform.scale(
        pygame.image.load(get_resource_path(f'dino_walk_{i}.png')).convert_alpha(),
        DINO_SPRITE_SIZE
    )
    for i in range(1, 3)
]
        self.jump_images = [
    pygame.transform.scale(
        pygame.image.load(get_resource_path(f'dino_jump_{i}.png')).convert_alpha(),
        DINO_SPRITE_SIZE
    )
    for i in range(1, 3)
]
        self.image = self.walk_images[0]
        """
        self.image는 공룡의 현재 이미지를 나타냅니다.
self.rect는 해당 이미지의 사각형 영역을 나타내며, 이 영역이 충돌 감지에 사용됩니다.
즉, 공룡의 충돌 영역은 현재 이미지의 크기와 위치에 따라 자동으로 설정됩니다.
        """
        self.rect = self.image.get_rect(topleft=pos)
        self.index = 0
        self.is_jumping = False
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -12

    def update(self):
        if self.is_jumping:
            self.velocity += self.gravity
            self.rect.y += self.velocity
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.is_jumping = False
                self.velocity = 0
            self.index = (self.index + 1) % len(self.jump_images)
            self.image = self.jump_images[self.index]
        else:
            self.index = (self.index + 1) % len(self.walk_images)
            self.image = self.walk_images[self.index]

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = self.jump_strength


# ▶ Obstacle 클래스 정의
class Obstacle(pygame.sprite.Sprite):      
    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.transform.scale(
    pygame.image.load(get_resource_path('obstacle.png')).convert_alpha(),
    OBASTACLE_SPRITE_SIZE
)
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = WIDTH


# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# 공룡과 장애물 인스턴스 생성
dino = Dino(pos=(50, HEIGHT - 90))
obstacle = Obstacle(pos=(WIDTH, HEIGHT - 60), speed=5)

# 스프라이트 그룹에 추가
all_sprites.add(dino)
all_sprites.add(obstacle)
obstacles.add(obstacle)

# 게임 루프
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        dino.jump()

    # 스프라이트 업데이트
    all_sprites.update()

    # 충돌 검사
    if pygame.sprite.spritecollide(dino, obstacles, False):
        print("충돌! 게임 오버")
        running = False

    # 스프라이트 그리기
    all_sprites.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

pygame.quit()
sys.exit()

