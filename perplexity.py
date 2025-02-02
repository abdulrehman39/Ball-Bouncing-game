import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.99

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball class
class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 5  # Initial velocity in x direction
        self.vy = 0  # Initial velocity in y direction

    def update(self):
        # Apply gravity
        self.vy += GRAVITY
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

# Hexagon class
class Hexagon:
    def __init__(self, center_x, center_y, size):
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.angle = 0

    def update(self):
        # Rotate the hexagon over time
        self.angle += 1

    def draw(self, screen):
        points = []
        for i in range(6):
            theta = math.radians(60 * i + self.angle)
            x = self.center_x + self.size * math.cos(theta)
            y = self.center_y + self.size * math.sin(theta)
            points.append((x, y))
        
        pygame.draw.polygon(screen, WHITE, points)

def check_collision(ball, hexagon):
    # Check collision with hexagon walls (simplified)
    for i in range(6):
        angle1 = math.radians(60 * i + hexagon.angle)
        angle2 = math.radians(60 * (i + 1) + hexagon.angle)

        x1 = hexagon.center_x + hexagon.size * math.cos(angle1)
        y1 = hexagon.center_y + hexagon.size * math.sin(angle1)
        
        x2 = hexagon.center_x + hexagon.size * math.cos(angle2)
        y2 = hexagon.center_y + hexagon.size * math.sin(angle2)

        # Line segment from (x1,y1) to (x2,y2)
        if line_circle_collision((x1, y1), (x2, y2), (ball.x, ball.y), ball.radius):
            ball.vy *= -1  # Reverse vertical velocity on collision

def line_circle_collision(p1, p2, circle_center, radius):
    # Check if the circle collides with the line segment p1 to p2
    line_vec = (p2[0] - p1[0], p2[1] - p1[1])
    circle_vec = (circle_center[0] - p1[0], circle_center[1] - p1[1])
    
    line_len_sq = line_vec[0] ** 2 + line_vec[1] ** 2
    if line_len_sq == 0:
        return False
    
    t = max(0, min(1, (circle_vec[0] * line_vec[0] + circle_vec[1] * line_vec[1]) / line_len_sq))
    
    closest_point = (p1[0] + t * line_vec[0], p1[1] + t * line_vec[1])
    
    dist_sq = (closest_point[0] - circle_center[0]) ** 2 + (closest_point[1] - circle_center[1]) ** 2
    
    return dist_sq <= radius ** 2

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball = Ball(WIDTH // 2, HEIGHT // 2, 15)
    hexagon = Hexagon(WIDTH // 2, HEIGHT // 2, 200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ball.update()
        hexagon.update()

        check_collision(ball, hexagon)

        screen.fill(BLACK)
        
        hexagon.draw(screen)
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
