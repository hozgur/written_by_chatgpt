import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Water Surface Wave Simulation with Reflections")

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
DEEP_BLUE = (0, 0, 139)

# Grid dimensions
cols, rows = 200, 150
spacing_x = WIDTH // cols
spacing_y = HEIGHT // rows

# Wave grids
current = np.zeros((rows, cols))
previous = np.zeros((rows, cols))
velocity = np.zeros((rows, cols))

def apply_wave(current, x, y, strength):
    if 0 <= x < cols and 0 <= y < rows:
        current[y, x] += strength

def update_wave(current, previous, velocity):
    damping = 0.99
    tension = 0.025
    
    # Wave propagation based on the wave equation
    new_current = (
        (previous[:-2, 1:-1] + previous[2:, 1:-1] + 
         previous[1:-1, :-2] + previous[1:-1, 2:] - 
         4 * previous[1:-1, 1:-1])
        * tension
    ) + 2 * current[1:-1, 1:-1] - previous[1:-1, 1:-1]
    
    # Apply damping
    new_current *= damping
    
    # Update grids
    previous[1:-1, 1:-1] = current[1:-1, 1:-1]
    current[1:-1, 1:-1] = new_current

def draw_wave(surface, current):
    surface.fill(WHITE)
    for y in range(rows):
        for x in range(cols):
            height = current[y, x]
            wave_color_value = max(0, min(255, 127 + int(height * 100)))
            wave_color = (wave_color_value, wave_color_value, 255)
            
            # Reflection effect
            reflection_offset = int(height * 10)
            reflection_y = min(rows - 1, y + reflection_offset)
            sky_color_ratio = y / rows
            sky_color = (
                int(SKY_BLUE[0] * sky_color_ratio + DEEP_BLUE[0] * (1 - sky_color_ratio)),
                int(SKY_BLUE[1] * sky_color_ratio + DEEP_BLUE[1] * (1 - sky_color_ratio)),
                int(SKY_BLUE[2] * sky_color_ratio + DEEP_BLUE[2] * (1 - sky_color_ratio))
            )
            
            # Blend the wave color with the reflection
            blended_color = (
                (wave_color[0] + sky_color[0]) // 2,
                (wave_color[1] + sky_color[1]) // 2,
                (wave_color[2] + sky_color[2]) // 2
            )

            rect = pygame.Rect(x * spacing_x, y * spacing_y, spacing_x, spacing_y)
            pygame.draw.rect(surface, blended_color, rect)

# Simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // spacing_x
            grid_y = mouse_y // spacing_y
            apply_wave(current, grid_x, grid_y, -10)

    update_wave(current, previous, velocity)
    draw_wave(screen, current)

    pygame.display.flip()
    pygame.time.delay(30)

# Quit Pygame
pygame.quit()
