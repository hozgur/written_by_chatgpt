import numpy as np
import random
import pygame
import math
from typing import Tuple, List

class Ant:
    def __init__(self, simulation, position: Tuple[int, int]):
        self.simulation = simulation
        self.x, self.y = position
        self.angle = random.uniform(0, 2 * math.pi)  # Random initial direction
        self.speed = 2.0
        self.carrying_food = False
        self.sensor_angle = math.pi / 4  # 45 degrees
        self.sensor_distance = 20
        self.wander_strength = 0.3
        
        # Time tracking
        self.time_since_home = 0
        self.time_since_food = 0
        
    def update(self):
        # Determine behavior based on whether ant is carrying food
        if self.carrying_food:
            self.return_to_home()
            self.time_since_food += 1
        else:
            self.search_for_food()
            self.time_since_home += 1
            
        # Check for reaching food or home
        if not self.carrying_food and self.simulation.is_food_at(self.x, self.y):
            self.carrying_food = True
            # Turn around when finding food
            self.angle += math.pi
            # Reset food timer
            self.time_since_food = 0
        elif self.carrying_food and self.simulation.is_home_at(self.x, self.y):
            self.carrying_food = False
            # Turn around when reaching home
            self.angle += math.pi
            # Reset home timer
            self.time_since_home = 0
            
        # Move ant according to its direction and speed
        self.move()
        
        # Deposit pheromones with time-based decay
        max_time = 800  # Time constant for pheromone strength reduction
        if not self.carrying_food:
            # Home pheromone strength decreases with time since leaving home
            strength = max(0, 1.0 - self.time_since_home / max_time)
            self.simulation.add_pheromone("home", self.x, self.y, strength)
        else:
            # Food pheromone strength decreases with time since finding food
            strength = max(0, 1.0 - self.time_since_food / max_time)
            self.simulation.add_pheromone("food", self.x, self.y, strength)
    
    def search_for_food(self):
        # Use sensors to detect food pheromones
        left_angle = self.angle - self.sensor_angle
        right_angle = self.angle + self.sensor_angle
        
        # Calculate sensor positions
        left_x = self.x + math.cos(left_angle) * self.sensor_distance
        left_y = self.y + math.sin(left_angle) * self.sensor_distance
        
        forward_x = self.x + math.cos(self.angle) * self.sensor_distance
        forward_y = self.y + math.sin(self.angle) * self.sensor_distance
        
        right_x = self.x + math.cos(right_angle) * self.sensor_distance
        right_y = self.y + math.sin(right_angle) * self.sensor_distance
        
        # Sample pheromone concentrations at sensor positions
        left_pheromone = self.simulation.get_pheromone("food", int(left_x), int(left_y))
        forward_pheromone = self.simulation.get_pheromone("food", int(forward_x), int(forward_y))
        right_pheromone = self.simulation.get_pheromone("food", int(right_x), int(right_y))
        
        # Adjust direction based on pheromone concentrations
        if max(left_pheromone, forward_pheromone, right_pheromone) > 0:
            if left_pheromone > forward_pheromone and left_pheromone > right_pheromone:
                self.angle -= 0.1  # Turn left
            elif right_pheromone > forward_pheromone and right_pheromone > left_pheromone:
                self.angle += 0.1  # Turn right
        else:
            # Random wandering
            self.angle += random.uniform(-self.wander_strength, self.wander_strength)
    
    def return_to_home(self):
        # Calculate sensor positions to detect home pheromone gradient
        left_angle = self.angle - self.sensor_angle
        right_angle = self.angle + self.sensor_angle
        
        # Calculate sensor positions
        left_x = self.x + math.cos(left_angle) * self.sensor_distance
        left_y = self.y + math.sin(left_angle) * self.sensor_distance
        
        forward_x = self.x + math.cos(self.angle) * self.sensor_distance
        forward_y = self.y + math.sin(self.angle) * self.sensor_distance
        
        right_x = self.x + math.cos(right_angle) * self.sensor_distance
        right_y = self.y + math.sin(right_angle) * self.sensor_distance
        
        # Sample pheromone concentrations at sensor positions
        left_pheromone = self.simulation.get_pheromone("home", int(left_x), int(left_y))
        forward_pheromone = self.simulation.get_pheromone("home", int(forward_x), int(forward_y))
        right_pheromone = self.simulation.get_pheromone("home", int(right_x), int(right_y))
        
        # Adjust direction based on pheromone concentrations
        if max(left_pheromone, forward_pheromone, right_pheromone) > 0:
            # Make direction changes more significant for better gradient following
            if left_pheromone > forward_pheromone and left_pheromone > right_pheromone:
                self.angle -= 0.2  # Turn left more decisively
            elif right_pheromone > forward_pheromone and right_pheromone > left_pheromone:
                self.angle += 0.2  # Turn right more decisively
            # If forward is strongest, keep going that direction
        else:
            # Direct navigation toward home when no pheromones detected
            home_x, home_y = self.simulation.home_position
            home_direction = math.atan2(home_y - self.y, home_x - self.x)
            
            # More directly adjust toward home - increased strength
            angle_diff = (home_direction - self.angle + 3 * math.pi) % (2 * math.pi) - math.pi
            self.angle += min(0.1, max(-0.1, angle_diff * 0.2))  # Increased adjustment
            
            # Reduced randomness to prevent wandering away from home direction
            self.angle += random.uniform(-self.wander_strength/2, self.wander_strength/2)
    
    def move(self):
        # Calculate new position based on angle and speed
        new_x = self.x + math.cos(self.angle) * self.speed
        new_y = self.y + math.sin(self.angle) * self.speed
        
        # Check for collisions with screen edges and bounce
        bounce = False
        
        # Horizontal boundaries
        if new_x < 0:
            new_x = 0
            bounce = True
        elif new_x >= self.simulation.width:
            new_x = self.simulation.width - 1
            bounce = True
        
        # Vertical boundaries
        if new_y < 0:
            new_y = 0
            bounce = True
        elif new_y >= self.simulation.height:
            new_y = self.simulation.height - 1
            bounce = True
        
        # If the ant hit a wall, bounce it (reflect its direction)
        if bounce:
            # Add some randomness to the bounce to prevent ants getting stuck
            self.angle = (self.angle + math.pi + random.uniform(-0.5, 0.5)) % (2 * math.pi)
        
        # Update the ant's position
        self.x, self.y = new_x, new_y


class AntSimulation:
    def __init__(self, 
                 width: int = 1920, 
                 height: int = 1080, 
                 grid_scale: int = 10, 
                 num_ants: int = 1000,
                 home_position: Tuple[int, int] = None,
                 food_positions: List[Tuple[int, int]] = None):
        # Simulation area dimensions
        self.width = width
        self.height = height
        
        # Grid dimensions (lower resolution)
        self.grid_scale = grid_scale
        self.grid_width = width // grid_scale
        self.grid_height = height // grid_scale
        
        # Initialize pheromone grids (one for food, one for home)
        self.food_pheromones = np.zeros((self.grid_width, self.grid_height))
        self.home_pheromones = np.zeros((self.grid_width, self.grid_height))
        
        # Pheromone decay rate - increased to make pheromones last longer
        self.decay_rate = 0.005  # Changed from 0.95 to 0.99
        
        # Home position (default to center)
        if home_position is None:
            self.home_position = (width // 2, height // 2)
        else:
            self.home_position = home_position
        
        # Food positions
        if food_positions is None:
            # Create some random food sources
            self.food_positions = []
            for _ in range(3):
                x = random.randint(100, self.width - 100)
                y = random.randint(100, self.height - 100)
                self.food_positions.append((x, y))
        else:
            self.food_positions = food_positions
        
        # Create the ants
        self.ants = [Ant(self, self.home_position) for _ in range(num_ants)]
        
    def update(self):
        # Update all ants
        for ant in self.ants:
            ant.update()
        
        # Apply pheromone decay
        # Only subtract decay_rate from values greater than decay_rate
        self.food_pheromones[self.food_pheromones > self.decay_rate] -= self.decay_rate/2
        self.home_pheromones[self.home_pheromones > self.decay_rate] -= self.decay_rate
        self.food_pheromones[self.food_pheromones <= self.decay_rate] = 0
        self.home_pheromones[self.home_pheromones <= self.decay_rate] = 0
    
    def add_pheromone(self, pheromone_type: str, x: int, y: int, amount: float = 1.0):
        # Convert coordinates to grid coordinates
        grid_x = int(x // self.grid_scale)
        grid_y = int(y // self.grid_scale)
        
        # Ensure coordinates are within grid bounds
        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
            if pheromone_type == "food":
                self.food_pheromones[grid_x, grid_y] += amount
            elif pheromone_type == "home":
                self.home_pheromones[grid_x, grid_y] += amount
    
    def get_pheromone(self, pheromone_type: str, x: int, y: int) -> float:
        # Convert coordinates to grid coordinates
        grid_x = x // self.grid_scale
        grid_y = y // self.grid_scale
        
        # Ensure coordinates are within grid bounds
        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
            if pheromone_type == "food":
                return self.food_pheromones[grid_x, grid_y]
            elif pheromone_type == "home":
                return self.home_pheromones[grid_x, grid_y]
        return 0.0
    
    def is_food_at(self, x: int, y: int, radius: int = 50) -> bool:
        # Check if position is near any food source
        for food_x, food_y in self.food_positions:
            dist = math.sqrt((x - food_x) ** 2 + (y - food_y) ** 2)
            if dist < radius:
                return True
        return False
    
    def is_home_at(self, x: int, y: int, radius: int = 50) -> bool:
        # Check if position is near home
        home_x, home_y = self.home_position
        dist = math.sqrt((x - home_x) ** 2 + (y - home_y) ** 2)
        return dist < radius


def main():
    pygame.init()
    width, height = 1920, 1080
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ant Colony Simulation")
    
    grid_scale = 20  # Grid resolution is 1/10 of screen resolution
    
    # Set home and food positions as requested
    home_position = (50, 50)  # Top-left
    
    # Food position closer to center (about 2/3 of the way toward center from bottom-right)
    food_positions = [(width // 2 + 300, height // 2 + 200)]
    
    # Create simulation
    simulation = AntSimulation(width, height, grid_scale, num_ants=1000, 
                              home_position=home_position, 
                              food_positions=food_positions)
    
    # Create a clock object to control frame rate
    clock = pygame.time.Clock()
    
    # Checkboxes for pheromone visibility
    show_food_pheromones = True
    show_home_pheromones = True
    food_checkbox_rect = pygame.Rect(20, 20, 20, 20)
    home_checkbox_rect = pygame.Rect(20, 50, 20, 20)
    font = pygame.font.SysFont(None, 24)
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle checkboxes when clicked
                if food_checkbox_rect.collidepoint(event.pos):
                    show_food_pheromones = not show_food_pheromones
                elif home_checkbox_rect.collidepoint(event.pos):
                    show_home_pheromones = not show_home_pheromones
        
        # Update simulation
        simulation.update()
        
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw the pheromone grid with separate visibility toggles
        for x in range(simulation.grid_width):
            for y in range(simulation.grid_height):
                # Get pheromone intensities
                food_intensity = min(255, simulation.food_pheromones[x, y] * 255)
                home_intensity = min(255, simulation.home_pheromones[x, y] * 255)
                
                # Only draw visible pheromones with non-zero intensity
                if (show_food_pheromones and food_intensity > 0) or (show_home_pheromones and home_intensity > 0):
                    # Apply visibility settings to intensities
                    food_display = int(food_intensity) if show_food_pheromones else 0
                    home_display = int(home_intensity) if show_home_pheromones else 0
                    
                    # Create a blended color based on visible pheromones
                    color = (0, food_display, home_display)
                    
                    pygame.draw.rect(screen, color, 
                                   (x * grid_scale, y * grid_scale, grid_scale, grid_scale))
        
        # Draw the food sources
        for food_x, food_y in simulation.food_positions:
            pygame.draw.circle(screen, (0, 255, 0), (int(food_x), int(food_y)), 10)
        
        # Draw the home
        home_x, home_y = simulation.home_position
        pygame.draw.circle(screen, (0, 0, 255), (int(home_x), int(home_y)), 15)
        
        # Draw the ants
        for ant in simulation.ants:
            color = (255, 0, 0) if ant.carrying_food else (255, 255, 255)
            pygame.draw.circle(screen, color, (int(ant.x), int(ant.y)), 2)
        
        # Draw the checkboxes and labels
        # Food pheromone checkbox
        pygame.draw.rect(screen, (255, 255, 255), food_checkbox_rect, 2)
        if show_food_pheromones:
            pygame.draw.rect(screen, (255, 255, 255), food_checkbox_rect.inflate(-8, -8))
        food_text = font.render("Show Food Pheromones (Green)", True, (0, 255, 0))
        screen.blit(food_text, (food_checkbox_rect.right + 10, food_checkbox_rect.top))
        
        # Home pheromone checkbox
        pygame.draw.rect(screen, (255, 255, 255), home_checkbox_rect, 2)
        if show_home_pheromones:
            pygame.draw.rect(screen, (255, 255, 255), home_checkbox_rect.inflate(-8, -8))
        home_text = font.render("Show Home Pheromones (Blue)", True, (0, 0, 255))
        screen.blit(home_text, (home_checkbox_rect.right + 10, home_checkbox_rect.top))
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()