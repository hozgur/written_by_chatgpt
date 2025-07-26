import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Water Surface Wave Simulation")

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
DEEP_BLUE = (0, 0, 139)

# Grid dimensions
cols, rows = 200, 150  # Reduced resolution for better performance
spacing_x = WIDTH // cols
spacing_y = HEIGHT // rows

# Wave grids
current = np.zeros((rows, cols))
previous = np.zeros((rows, cols))

# Apply wave at specific position
def apply_wave(current, x, y, strength):
    if 0 <= x < cols and 0 <= y < rows:
        current[y, x] = strength

# Update wave propagation
def update_wave(current, previous):
    damping = 0.99
    tension = 0.025

    # Reflect waves at borders
    previous[:, 0] = previous[:, 1]
    previous[:, -1] = previous[:, -2]
    previous[0, :] = previous[1, :]
    previous[-1, :] = previous[-2, :]

    # Perform wave propagation using the wave equation
    new_current = (
        (previous[:-2, 1:-1] + previous[2:, 1:-1] + 
         previous[1:-1, :-2] + previous[1:-1, 2:] - 
         4 * previous[1:-1, 1:-1])
        * tension
    ) + 2 * current[1:-1, 1:-1] - previous[1:-1, 1:-1]

    # Apply damping
    new_current *= damping

    # Update grids in place
    previous[1:-1, 1:-1], current[1:-1, 1:-1] = current[1:-1, 1:-1], new_current

# Draw wave to the screen
def draw_wave(surface, current):
    surface_array = pygame.surfarray.pixels3d(surface)
    
    height_map = (127 + current * 100).clip(0, 255).astype(np.uint8)
    
    gradient = np.linspace(SKY_BLUE, DEEP_BLUE, rows, axis=0)
    reflection = gradient[:, np.newaxis, :]
    
    color_map = np.stack([height_map] * 3, axis=-1)
    blended_color = ((color_map + reflection) // 2).astype(np.uint8)
    
    scaled_color = np.repeat(np.repeat(blended_color, spacing_y, axis=0), spacing_x, axis=1)
    
    surface_array[:scaled_color.shape[0], :scaled_color.shape[1]] = scaled_color[:surface_array.shape[0], :surface_array.shape[1]]

    del surface_array  # Unlock the surface array to apply changes

# Simulation loop
running = True
wave_applied = False  # Track if a wave has been applied
wave_threshold = 0.01  # Threshold to detect if wave has dissipated

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // spacing_x
            grid_y = mouse_y // spacing_y

            if not wave_applied:  # Apply only one wave
                apply_wave(current, grid_y, grid_x, -10)  # Note: swapped x and y
                wave_applied = True

    update_wave(current, previous)
    draw_wave(screen, current)

    pygame.display.flip()
    pygame.time.delay(30)

    # Check if the wave has dissipated (using a small threshold)
    if np.abs(current).max() < wave_threshold:
        wave_applied = False

pygame.quit()
