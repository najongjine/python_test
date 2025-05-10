import pygame
import random
import time

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up display
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Set up game clock
CLOCK = pygame.time.Clock()
FPS = 10

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Starting direction: right
        self.length = 1
        self.score = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self, food_position):
        current = self.get_head_position()
        x, y = self.direction
        new = ((current[0] + x) % GRID_WIDTH, (current[1] + y) % GRID_HEIGHT)
        
        # Game over if snake collides with itself
        if new in self.positions[1:]:
            return False
        
        self.positions.insert(0, new)
        
        # Check if the snake ate food
        if new == food_position:
            self.score += 1
            return True
        else:
            if len(self.positions) > self.length:
                self.positions.pop()
            return None
    
    def change_direction(self, direction):
        # Prevent 180-degree turns
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def draw(self, surface):
        for p in self.positions:
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                         random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), 
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

def main():
    snake = Snake()
    food = Food()
    
    game_over = False
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))
        
        # Update the snake
        result = snake.update(food.position)
        
        if result is False:  # Game over
            game_over = True
        elif result is True:  # Snake ate food
            snake.length += 1
            food.randomize_position()
            # Ensure food doesn't appear on snake
            while food.position in snake.positions:
                food.randomize_position()
        
        # Draw everything
        DISPLAY.fill(WHITE)
        snake.draw(DISPLAY)
        food.draw(DISPLAY)
        
        # Display score
        font = pygame.font.SysFont('arial', 20)
        score_text = font.render(f"Score: {snake.score}", True, BLACK)
        DISPLAY.blit(score_text, (5, 5))
        
        pygame.display.update()
        CLOCK.tick(FPS)
    
    # Show game over message
    font = pygame.font.SysFont('arial', 40)
    game_over_text = font.render("Game Over", True, BLACK)
    DISPLAY.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 
                                  HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()

if __name__ == "__main__":
    main()
