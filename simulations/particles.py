# This is created by claude-sonnet-3.5 on Cursor

import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Optimized Particle Simulation with NumPy and Mouse Interaction")

# Particle settings
num_particles = 1000
particle_radius = np.random.uniform(1, 5, num_particles)  # Varying particle sizes
push_radius = 100  # Radius within which particles are affected by the cursor

# Initialize particle positions, velocities, and colors
positions = np.random.rand(num_particles, 2) * np.array([width, height])
velocities = np.random.randn(num_particles, 2) * 2
colors = np.random.randint(0, 255, (num_particles, 3))

# Trail settings
max_trail_length = 20
trails = [[] for _ in range(num_particles)]

# Glow surface
glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get mouse position
    mouse_pos = np.array(pygame.mouse.get_pos())

    # Update particle positions
    positions += velocities

    # Bounce off walls
    positions = np.clip(positions, [0, 0], [width, height])
    hit_wall = (positions <= 0) | (positions >= [width, height])
    velocities[hit_wall] *= -1

    # Apply mouse repulsion
    direction = positions - mouse_pos
    distance = np.linalg.norm(direction, axis=1).reshape(-1, 1)
    repulsion = np.where(distance < push_radius, direction / (distance + 1), 0)
    velocities += repulsion * 0.5

    # Limit particle speed
    speed = np.linalg.norm(velocities, axis=1).reshape(-1, 1)
    max_speed = 5
    velocities = np.where(speed > max_speed, velocities / speed * max_speed, velocities)

    # Clear the screen and glow surface
    screen.fill((0, 0, 0))
    glow_surface.fill((0, 0, 0, 0))

    # Update trails and draw particles
    for i, (pos, color) in enumerate(zip(positions, colors)):
        trails[i].append(pos.copy())
        if len(trails[i]) > max_trail_length:
            trails[i].pop(0)
        
        # Draw trail
        if len(trails[i]) > 1:
            pygame.draw.lines(screen, color, False, trails[i], 1)
        
        # Draw particle
        pygame.draw.circle(screen, color, pos.astype(int), particle_radius[i])
        
        # Add glow effect
        pygame.draw.circle(glow_surface, (*color, 100), pos.astype(int), particle_radius[i] * 2)

    # Apply glow effect
    screen.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    # Draw mouse position
    pygame.draw.circle(screen, (255, 255, 255), mouse_pos.astype(int), 10)

    # Gradually change particle colors
    colors += np.random.randint(-5, 6, (num_particles, 3))
    colors = np.clip(colors, 0, 255)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
