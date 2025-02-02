import pygame
import math

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vx = 5
        self.vy = -10
        self.radius = 10
        self.friction = 0.98
        self.gravity = 0.1

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        self.vx *= self.friction
        self.vy *= self.friction

        # Boundary check
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx = -self.vx
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy = -self.vy * 0.9  # Energy loss on bounce

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

class Hexagon:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 200
        self.angle = 0
        self.speed = 1

    def update(self):
        self.angle += self.speed

    def draw(self, screen):
        points = []
        for i in range(6):
            a = math.radians(self.angle + i * 60)
            px = self.x + math.cos(a) * self.size
            py = self.y + math.sin(a) * self.size
            points.append((px, py))
        pygame.draw.polygon(screen, WHITE, points, 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball = Ball()
    hexagon = Hexagon()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        hexagon.update()
        hexagon.draw(screen)

        ball.update()
        ball.draw(screen)

        # Simple collision detection with hexagon
        # This is a very basic implementation and doesn't account for the hexagon's rotation
        dx = ball.x - hexagon.x
        dy = ball.y - hexagon.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < hexagon.size + ball.radius:
            # Basic bounce logic, doesn't account for angle of incidence
            ball.vx = -ball.vx
            ball.vy = -ball.vy

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()