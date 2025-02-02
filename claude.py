import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Physics constants
GRAVITY = 0.5
FRICTION = 0.8
BALL_RADIUS = 10
HEXAGON_RADIUS = 200
ROTATION_SPEED = 0.5  # degrees per frame

class Ball:
    def __init__(self, x, y):
        self.pos = np.array([float(x), float(y)])
        self.vel = np.array([0.0, 0.0])
    
    def update(self):
        # Apply gravity
        self.vel[1] += GRAVITY
        
        # Update position
        self.pos += self.vel

class Hexagon:
    def __init__(self, center_x, center_y, radius):
        self.center = np.array([center_x, center_y])
        self.radius = radius
        self.angle = 0
        
    def get_vertices(self):
        vertices = []
        for i in range(6):
            angle = math.radians(self.angle + i * 60)
            x = self.center[0] + self.radius * math.cos(angle)
            y = self.center[1] + self.radius * math.sin(angle)
            vertices.append(np.array([x, y]))
        return vertices
    
    def rotate(self):
        self.angle += ROTATION_SPEED
        
def get_line_normal(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    # Return normalized normal vector
    length = math.sqrt(dx*dx + dy*dy)
    return np.array([-dy/length, dx/length])

def check_collision(ball, vertices):
    for i in range(len(vertices)):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % len(vertices)]
        
        # Get normal vector of the line
        normal = get_line_normal(p1, p2)
        
        # Calculate distance from point to line
        line_vec = p2 - p1
        ball_vec = ball.pos - p1
        projection = np.dot(ball_vec, line_vec) / np.dot(line_vec, line_vec)
        closest_point = p1 + projection * line_vec
        
        # Check if the ball is colliding with the line segment
        if (0 <= projection <= 1 and 
            np.linalg.norm(closest_point - ball.pos) < BALL_RADIUS):
            
            # Calculate reflection vector
            ball.pos = closest_point + normal * BALL_RADIUS
            reflection = ball.vel - 2 * np.dot(ball.vel, normal) * normal
            ball.vel = reflection * FRICTION

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")
    clock = pygame.time.Clock()
    
    ball = Ball(WIDTH/2, HEIGHT/2)
    hexagon = Hexagon(WIDTH/2, HEIGHT/2, HEXAGON_RADIUS)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Reset ball position and give it random velocity
                ball.pos = np.array([float(WIDTH/2), float(HEIGHT/2)])
                ball.vel = np.array([np.random.uniform(-10, 10), np.random.uniform(-10, 10)])
        
        # Update
        hexagon.rotate()
        ball.update()
        
        # Check collisions
        vertices = hexagon.get_vertices()
        check_collision(ball, vertices)
        
        # Draw
        screen.fill(BLACK)
        
        # Draw hexagon
        pygame.draw.polygon(screen, WHITE, vertices, 2)
        
        # Draw ball
        pygame.draw.circle(screen, RED, tuple(ball.pos.astype(int)), BALL_RADIUS)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()