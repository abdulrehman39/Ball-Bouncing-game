import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
HEX_RADIUS = 200
BALL_RADIUS = 10
BALL_COLOR = (255, 0, 0)
HEX_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (255, 255, 255)
OMEGA = 3  # Angular velocity in radians per second
GRAVITY = 0.8  # Pixels per second squared
FRICTION = 0.995  # Velocity retention factor per frame
COR = 0.8  # Coefficient of restitution

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
clock = pygame.time.Clock()

class Ball:
    def __init__(self, x: float, y: float, vx: float = 0.0, vy: float = 0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

# Initialize ball near the top of the hexagon
ball = Ball(CENTER[0], CENTER[1] - HEX_RADIUS + BALL_RADIUS + 5, 3, 0)
rotation_angle = 0  # Current rotation angle in radians

def get_hex_vertices(center, radius, angle):
    """Generate hexagon vertices with given rotation angle"""
    vertices = []
    for i in range(6):
        theta = angle + math.radians(i * 60)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        vertices.append((x, y))
    return vertices

def closest_point_on_segment(A, B, P):
    """Find closest point on segment AB to point P"""
    ax, ay = A
    bx, by = B
    px, py = P
    
    # Vector AB
    abx = bx - ax
    aby = by - ay
    # Vector AP
    apx = px - ax
    apy = py - ay
    
    # Project AP onto AB
    t = (apx * abx + apy * aby) / (abx**2 + aby**2 + 1e-8)
    t = max(0, min(1, t))
    
    return (ax + t * abx, ay + t * aby)

running = True
dt = 0  # Delta time in seconds

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    rotation_angle += OMEGA * dt
    rotation_angle %= 2 * math.pi
    
    # Get current hexagon vertices
    vertices = get_hex_vertices(CENTER, HEX_RADIUS, rotation_angle)
    
    # Apply physics
    ball.vy += GRAVITY * dt
    ball.vx *= FRICTION
    ball.vy *= FRICTION
    
    # Update position
    ball.x += ball.vx * dt
    ball.y += ball.vy * dt
    
    # Collision detection and response
    for i in range(6):
        A = vertices[i]
        B = vertices[(i+1)%6]
        P = (ball.x, ball.y)
        closest = closest_point_on_segment(A, B, P)
        
        # Calculate distance to closest point
        dx = ball.x - closest[0]
        dy = ball.y - closest[1]
        distance_sq = dx**2 + dy**2
        
        if distance_sq < BALL_RADIUS**2:
            # Calculate normal vector (pointing inward)
            midpoint = ((A[0] + B[0])/2, (A[1] + B[1])/2)
            normal = (CENTER[0] - midpoint[0], CENTER[1] - midpoint[1])
            norm_length = math.hypot(*normal)
            if norm_length == 0:
                continue
            normal = (normal[0]/norm_length, normal[1]/norm_length)
            
            # Calculate wall point velocity due to rotation
            px, py = closest
            vp_x = -OMEGA * (py - CENTER[1])
            vp_y = OMEGA * (px - CENTER[0])
            
            # Calculate relative velocity
            rel_vx = ball.vx - vp_x
            rel_vy = ball.vy - vp_y
            
            # Calculate normal component
            rel_norm = rel_vx * normal[0] + rel_vy * normal[1]
            
            if rel_norm < 0:  # Only process if moving towards wall
                # Apply collision response
                new_rel_vx = rel_vx - (1 + COR) * rel_norm * normal[0]
                new_rel_vy = rel_vy - (1 + COR) * rel_norm * normal[1]
                
                # Update ball velocity
                ball.vx = new_rel_vx + vp_x
                ball.vy = new_rel_vy + vp_y
                
                # Reposition ball outside collision point
                overlap = BALL_RADIUS - math.sqrt(distance_sq)
                ball.x += normal[0] * overlap
                ball.y += normal[1] * overlap
                break

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.polygon(screen, HEX_COLOR, vertices, 2)
    pygame.draw.circle(screen, BALL_COLOR, (int(ball.x), int(ball.y)), BALL_RADIUS)
    pygame.display.flip()
    
    dt = clock.tick(60) / 1000  # Limit to 60 FPS and convert to seconds

pygame.quit()