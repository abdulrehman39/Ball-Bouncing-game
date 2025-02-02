import pygame
import math

# Initialize Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in a Spinning Hexagon")
clock = pygame.time.Clock()

# Ball properties
ball_radius = 10
ball_pos = pygame.math.Vector2(width / 2, height / 2)
# Initial velocity in pixels per second
ball_vel = pygame.math.Vector2(200, -150)
gravity = pygame.math.Vector2(0, 300)   # pixels per second²
friction = 0.999  # slight damping each frame
restitution = 0.9  # bounciness coefficient

# Hexagon properties
hex_center = pygame.math.Vector2(width / 2, height / 2)
hex_radius = 250
hex_angle = 0  # initial rotation angle (radians)
spin_speed = math.radians(45)  # 45° per second in radians

def compute_hexagon_vertices(center, radius, angle_offset):
    """Returns a list of 6 vertices for a hexagon rotated by angle_offset."""
    vertices = []
    for i in range(6):
        angle = angle_offset + math.radians(60 * i)
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        vertices.append(pygame.math.Vector2(x, y))
    return vertices

def line_collision_response(ball_pos, ball_vel, A, B):
    """
    Check collision of a circle (ball) with a line segment AB.
    Returns updated ball_pos and ball_vel if collision occurs.
    """
    # Find closest point on segment AB to ball center.
    AB = B - A
    t = (ball_pos - A).dot(AB) / AB.length_squared()
    t = max(0, min(1, t))
    closest = A + AB * t
    distance = (ball_pos - closest).length()

    if distance < ball_radius:
        # Determine collision normal (pointing from wall to ball)
        if distance == 0:
            n = pygame.math.Vector2(0, 1)
        else:
            n = (ball_pos - closest).normalize()

        # Compute the wall’s linear velocity due to hexagon rotation.
        # The wall rotates about hex_center so the point's velocity is:
        # v_wall = omega x r, where r = (closest - hex_center)
        r = closest - hex_center
        # The perpendicular to r is (-r.y, r.x)
        wall_vel = pygame.math.Vector2(-r.y, r.x) * spin_speed

        # Get the ball’s velocity relative to the moving wall.
        v_rel = ball_vel - wall_vel

        # Only reflect if the ball is moving into the wall.
        if v_rel.dot(n) < 0:
            # Reflect the relative velocity about the normal.
            v_rel = v_rel - (1 + restitution) * v_rel.dot(n) * n
            ball_vel = v_rel + wall_vel

            # Move the ball so it’s no longer penetrating the wall.
            overlap = ball_radius - distance
            ball_pos += n * overlap

    return ball_pos, ball_vel

running = True
while running:
    dt = clock.tick(60) / 1000.0  # seconds elapsed since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the hexagon’s rotation.
    hex_angle += spin_speed * dt
    hex_vertices = compute_hexagon_vertices(hex_center, hex_radius, hex_angle)

    # Update ball physics.
    ball_vel += gravity * dt
    ball_pos += ball_vel * dt

    # Check collision with each of the hexagon's edges.
    for i in range(6):
        A = hex_vertices[i]
        B = hex_vertices[(i + 1) % 6]
        ball_pos, ball_vel = line_collision_response(ball_pos, ball_vel, A, B)

    # Apply friction (damping)
    ball_vel *= friction

    # Drawing
    screen.fill((30, 30, 30))  # dark background
    # Draw hexagon outline
    hex_points = [(int(v.x), int(v.y)) for v in hex_vertices]
    pygame.draw.polygon(screen, (200, 200, 200), hex_points, 3)
    # Draw the ball
    pygame.draw.circle(screen, (255, 0, 0), (int(ball_pos.x), int(ball_pos.y)), ball_radius)

    pygame.display.flip()

pygame.quit()
