import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireworks with Particle Physics")

# Colors
BLACK = (0, 0, 0)

# Particle class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 4)
        self.angle = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(2, 6)
        self.gravity = 0.1
        self.lifetime = random.randint(20, 60)
        self.age = 0
    
    def update(self):
        # Move the particle
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        # Apply gravity
        self.speed *= 0.98  # Simulate air resistance
        self.y += self.gravity
        # Age the particle
        self.age += 1
    
    def draw(self, screen):
        if self.age < self.lifetime:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Firework class
class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 300)
        self.color = [random.randint(50, 255) for _ in range(3)]
        self.particles = [Particle(self.x, self.y, self.color) for _ in range(100)]
    
    def update(self):
        for particle in self.particles:
            particle.update()
    
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

# Main loop
def main():
    clock = pygame.time.Clock()
    fireworks = []
    running = True
    
    while running:
        screen.fill(BLACK)
        
        # Create a new firework at random intervals
        if random.randint(0, 20) == 0:
            fireworks.append(Firework())
        
        # Update and draw all fireworks
        for firework in fireworks:
            firework.update()
            firework.draw(screen)
        
        # Remove finished fireworks
        fireworks = [f for f in fireworks if any(p.age < p.lifetime for p in f.particles)]
        
        pygame.display.flip()
        clock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()

# Run the simulation
if __name__ == "__main__":
    main()
