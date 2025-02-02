import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Hexagon parameters
hexagon_center = (width // 2, height // 2)
hexagon_radius = 150
hexagon_angle = 0  # Rotation angle

# Ball parameters
ball_radius = 10
ball_x = width // 2
ball_y = height // 4
ball_dx = 5  # Initial x velocity
ball_dy = 0  # Initial y velocity
gravity = 0.5
friction = 0.98

clock = pygame.time.Clock()

def draw_hexagon(center, radius, angle):
    points = []
    for i in range(6):
        angle_rad = math.radians(angle + i * 60)  # 60 degrees per side
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        points.append((x, y))
    pygame.draw.polygon(screen, white, points, 2) # Draw the hexagon outline

def ball_collision(ball_x, ball_y, ball_dx, ball_dy, center, radius, angle):
    for i in range(6):
        angle_rad = math.radians(angle + i * 60)
        x1 = center[0] + radius * math.cos(angle_rad)
        y1 = center[1] + radius * math.sin(angle_rad)

        angle_rad_next = math.radians(angle + (i+1) * 60)
        x2 = center[0] + radius * math.cos(angle_rad_next)
        y2 = center[1] + radius * math.sin(angle_rad_next)

        #Check if the ball's next position will be inside the hexagon
        #Slightly more accurate collision detection

        next_ball_x = ball_x + ball_dx
        next_ball_y = ball_y + ball_dy

        #Using the point in triangle method for collision detection
        #https://stackoverflow.com/questions/20495962/check-if-a-point-is-in-a-triangle
        def point_in_triangle(px, py, x1, y1, x2, y2, x3, y3):
            d1 = (px - x1) * (y2 - y1) - (px - x2) * (y1 - x1)
            d2 = (px - x2) * (y3 - y2) - (px - x3) * (y2 - y2)
            d3 = (px - x3) * (y1 - y3) - (px - x1) * (y3 - y1)
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            return not (has_neg and has_pos)

        triangle_center_x = center[0]
        triangle_center_y = center[1]

        if point_in_triangle(next_ball_x, next_ball_y, x1, y1, x2, y2, triangle_center_x, triangle_center_y):

            # Calculate normal vector to the wall
            nx = y2 - y1
            ny = -(x2 - x1)
            norm_length = math.sqrt(nx**2 + ny**2)
            nx /= norm_length
            ny /= norm_length

            # Calculate dot product of velocity and normal
            dot_product = ball_dx * nx + ball_dy * ny

            # Reflect the velocity
            ball_dx -= 2 * dot_product * nx
            ball_dy -= 2 * dot_product * ny
            
            #Add a small amount to avoid getting stuck
            ball_x += ball_dx * 0.1
            ball_y += ball_dy * 0.1
            break #Only collide with one wall per frame


    return ball_x, ball_y, ball_dx, ball_dy


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    hexagon_angle = (hexagon_angle + 1) % 360  # Rotate slowly

    # Update ball position and velocity
    ball_x += ball_dx
    ball_y += ball_dy
    ball_dy += gravity

    # Apply friction
    ball_dx *= friction
    ball_dy *= friction

    # Ball collision with walls
    ball_x, ball_y, ball_dx, ball_dy = ball_collision(ball_x, ball_y, ball_dx, ball_dy, hexagon_center, hexagon_radius, hexagon_angle)


    # Ball collision with screen edges (optional)
    if ball_x + ball_radius > width or ball_x - ball_radius < 0:
        ball_dx *= -1
    if ball_y + ball_radius > height or ball_y - ball_radius < 0:
        ball_dy *= -1


    # Draw everything
    screen.fill(black)
    draw_hexagon(hexagon_center, hexagon_radius, hexagon_angle)
    pygame.draw.circle(screen, red, (int(ball_x), int(ball_y)), ball_radius)  # Draw the ball

    pygame.display.flip()
    clock.tick(60)  # Control frame rate

pygame.quit()