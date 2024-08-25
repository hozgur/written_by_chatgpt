import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Water Wave Simulation")

# Colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Water surface points
num_points = 100
spacing = WIDTH // (num_points - 1)
points = [{'x': i * spacing, 'y': HEIGHT // 2, 'dy': 0} for i in range(num_points)]

def apply_wave(points, index, strength):
    if 0 <= index < len(points):
        points[index]['dy'] += strength

def update_wave(points):
    damping = 0.95
    tension = 0.02
    
    # Update positions based on velocity
    for point in points:
        point['y'] += point['dy']
        point['dy'] *= damping
    
    # Apply wave propagation
    for i in range(len(points)):
        if i > 0:
            left_neighbor = points[i - 1]
            force = (points[i]['y'] - left_neighbor['y']) * tension
            points[i - 1]['dy'] += force
        if i < len(points) - 1:
            right_neighbor = points[i + 1]
            force = (points[i]['y'] - right_neighbor['y']) * tension
            points[i + 1]['dy'] += force

def draw_wave(surface, points):
    surface.fill(WHITE)
    for i in range(len(points) - 1):
        pygame.draw.line(surface, BLUE, (points[i]['x'], points[i]['y']), (points[i + 1]['x'], points[i + 1]['y']), 2)

# Simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            closest_point = min(points, key=lambda p: abs(p['x'] - mouse_x))
            apply_wave(points, points.index(closest_point), mouse_y - HEIGHT // 2)

    update_wave(points)
    draw_wave(screen, points)

    pygame.display.flip()
    pygame.time.delay(30)

# Quit Pygame
pygame.quit()
