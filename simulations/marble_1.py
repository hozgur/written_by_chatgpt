import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Particle Simulation with Gravity and Reduced Bounce Collision")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Gravity constant
GRAVITY = 0.5  # Increased gravity strength

# Damping factor for collisions (0 < DAMPING <= 1)
DAMPING = 0.8  # Lower values reduce bounce more

# Particle class
class Particle:
    def __init__(self, x, y, radius=5):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = WHITE
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.mass = self.radius * 0.1  # mass proportional to radius
    
    def move(self):
        self.speed_y += GRAVITY * self.mass  # Apply gravity to vertical speed
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off the walls
        if self.x <= self.radius or self.x >= width - self.radius:
            self.speed_x = -self.speed_x * DAMPING
        if self.y <= self.radius or self.y >= height - self.radius:
            self.speed_y = -self.speed_y * DAMPING
            self.y = max(self.radius, min(self.y, height - self.radius))  # Prevent sticking to edges
    
    def attract(self, target_x, target_y):
        distance_x = target_x - self.x
        distance_y = target_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if distance > 1:  # Prevent division by zero
            self.speed_x += (distance_x / distance) * self.mass
            self.speed_y += (distance_y / distance) * self.mass
    
    def collide(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if distance < self.radius + other.radius:  # Collision detected
            # Calculate new velocities based on elastic collision formulas
            angle = math.atan2(distance_y, distance_x)
            speed_self = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)
            speed_other = math.sqrt(other.speed_x ** 2 + other.speed_y ** 2)
            
            direction_self = math.atan2(self.speed_y, self.speed_x)
            direction_other = math.atan2(other.speed_y, other.speed_x)
            
            new_speed_x_self = speed_other * math.cos(direction_other - angle)
            new_speed_y_self = speed_self * math.sin(direction_self - angle)
            new_speed_x_other = speed_self * math.cos(direction_self - angle)
            new_speed_y_other = speed_other * math.sin(direction_other - angle)
            
            # Apply damping to reduce bounce
            self.speed_x = (new_speed_x_self * math.cos(angle) + new_speed_y_self * math.cos(angle + math.pi / 2)) * DAMPING
            self.speed_y = (new_speed_x_self * math.sin(angle) + new_speed_y_self * math.sin(angle + math.pi / 2)) * DAMPING
            other.speed_x = (new_speed_x_other * math.cos(angle) + new_speed_y_other * math.cos(angle + math.pi / 2)) * DAMPING
            other.speed_y = (new_speed_x_other * math.sin(angle) + new_speed_y_other * math.sin(angle + math.pi / 2)) * DAMPING
            
            # Adjust positions to prevent particles from sticking together
            overlap = 0.5 * (self.radius + other.radius - distance + 1)
            self.x -= overlap * math.cos(angle)
            self.y -= overlap * math.sin(angle)
            other.x += overlap * math.cos(angle)
            other.y += overlap * math.sin(angle)
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Main loop
def main():
    particles = [Particle(random.randint(0, width), random.randint(0, height)) for _ in range(300)]
    running = True
    attracting = False
    
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                attracting = True
            elif event.type == pygame.MOUSEBUTTONUP:
                attracting = False
        
        if attracting:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for particle in particles:
                particle.attract(mouse_x, mouse_y)
        
        for i, particle in enumerate(particles):
            for other in particles[i+1:]:
                particle.collide(other)
            particle.move()
            particle.draw()
        
        pygame.display.flip()
        pygame.time.delay(30)

    pygame.quit()

if __name__ == "__main__":
    main()
