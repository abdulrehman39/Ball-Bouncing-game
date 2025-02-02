import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.98

# Colors
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Ball properties
ball_radius = 10
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4]
ball_velocity = [2.0, 0.0]

# Hexagon properties
hexagon_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
hexagon_radius = 200
hexagon_angle = 0  # Angle in degrees
rotation_speed = 1  # Degrees per frame

# Helper function to get hexagon points
def get_hexagon_points(center, radius, angle):
    points = []
    for i in range(6):
        theta = math.radians(angle + i * 60)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        points.append((x, y))
    return points

# Helper function to reflect the ball off a line segment
def reflect_ball(ball_pos, ball_velocity, point1, point2):
    # Line segment vector
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return

    # Normalize the line vector
    dx /= length
    dy /= length

    # Normal vector to the line
    normal = [-dy, dx]

    # Vector from the point on the line to the ball
    ball_to_line = [ball_pos[0] - point1[0], ball_pos[1] - point1[1]]

    # Projection of ball_to_line onto the normal
    dot_product = ball_to_line[0] * normal[0] + ball_to_line[1] * normal[1]

    if dot_product > 0:
        normal = [-normal[0], -normal[1]]

    # Reflect the velocity vector
    dot = ball_velocity[0] * normal[0] + ball_velocity[1] * normal[1]
    ball_velocity[0] -= 2 * dot * normal[0]
    ball_velocity[1] -= 2 * dot * normal[1]

# Main game loop
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    hexagon_angle += rotation_speed

    # Get hexagon points
    hexagon_points = get_hexagon_points(hexagon_center, hexagon_radius, hexagon_angle)

    # Update ball position
    ball_velocity[1] += GRAVITY  # Apply gravity
    ball_pos[0] = int(ball_pos[0] + ball_velocity[0])
    ball_pos[1] = int(ball_pos[1] + ball_velocity[1])

    # Apply friction
    ball_velocity[0] *= FRICTION
    ball_velocity[1] *= FRICTION

    # Draw the hexagon
    pygame.draw.polygon(screen, BLUE, hexagon_points, 3)

    # Check for collisions with hexagon walls
    for i in range(6):
        point1 = hexagon_points[i]
        point2 = hexagon_points[(i + 1) % 6]

        # Check if the ball is near the wall
        ball_to_point1 = math.hypot(ball_pos[0] - point1[0], ball_pos[1] - point1[1])
        ball_to_point2 = math.hypot(ball_pos[0] - point2[0], ball_pos[1] - point2[1])

        # Reflect the ball if it collides with the wall
        if ball_to_point1 < ball_radius or ball_to_point2 < ball_radius:
            reflect_ball(ball_pos, ball_velocity, point1, point2)

    # Draw the ball
    pygame.draw.circle(screen, BLUE, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
