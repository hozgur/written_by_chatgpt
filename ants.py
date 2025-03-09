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
        self.sensor_angle = math.pi / 3  # Increased from pi/4 to pi/3 for wider sensing
        self.sensor_distance = 30  # Increased from 20 to 30 for longer range sensing
        self.wander_strength = 0.5  # Increased from 0.3 to 0.5 for more randomness
        self.previous_directions = []  # Store previous directions to detect loops
        self.direction_memory = 5  # Number of previous directions to remember
        
        # Time tracking
        self.time_since_home = 0
        self.time_since_food = 0
        self.stuck_time = 0  # Track how long ant might be stuck
        
    def update(self):
        # Store previous position to detect if stuck
        prev_x, prev_y = self.x, self.y
        
        # Check for reaching food or home BEFORE movement and direction changes
        if not self.carrying_food and self.simulation.is_food_at(self.x, self.y):
            self.carrying_food = True
            self.angle = math.atan2(self.simulation.home_position[1] - self.y, 
                                  self.simulation.home_position[0] - self.x)
            self.time_since_food = 0
            self.previous_directions.clear()
            return  # End update here to ensure clean state transition
        elif self.carrying_food and self.simulation.is_home_at(self.x, self.y):
            # Drop off food and reset state
            self.carrying_food = False
            self.time_since_home = 0
            self.previous_directions.clear()
            # Pick a new random direction for food search
            self.angle = random.uniform(0, 2 * math.pi)
            # Move slightly away from home to prevent immediate return
            self.x += math.cos(self.angle) * (self.speed * 2)
            self.y += math.sin(self.angle) * (self.speed * 2)
            return  # End update here to ensure clean state transition
        
        # Regular update logic
        if self.carrying_food:
            self.return_to_home()
            self.time_since_food += 1
        else:
            self.search_for_food()
            self.time_since_home += 1
        
        # Move ant according to its direction and speed
        self.move()
        
        # Check if ant is stuck (barely moving)
        if abs(self.x - prev_x) < 0.1 and abs(self.y - prev_y) < 0.1:
            self.stuck_time += 1
            if self.stuck_time > 10:  # If stuck for too long
                self.angle += random.uniform(math.pi/2, math.pi)  # Make a significant turn
                self.stuck_time = 0
        else:
            self.stuck_time = 0
        
        # Store direction history
        self.previous_directions.append(self.angle)
        if len(self.previous_directions) > self.direction_memory:
            self.previous_directions.pop(0)
        
        # Check for loops and break them
        if self.detect_loop():
            self.break_loop()
        
        # Deposit pheromones with time-based decay
        max_time = 1000
        if not self.carrying_food:
            strength = max(0, 1.0 - self.time_since_home / max_time)
            self.simulation.add_pheromone("home", self.x, self.y, strength * 0.8)
        else:
            strength = max(0, 1.0 - self.time_since_food / max_time)
            self.simulation.add_pheromone("food", self.x, self.y, strength * 0.8)
    
    def detect_loop(self) -> bool:
        if len(self.previous_directions) < self.direction_memory:
            return False
        
        # Calculate average angular change
        total_change = 0
        for i in range(1, len(self.previous_directions)):
            change = (self.previous_directions[i] - self.previous_directions[i-1]) % (2 * math.pi)
            if change > math.pi:
                change -= 2 * math.pi
            total_change += abs(change)
        
        avg_change = total_change / (len(self.previous_directions) - 1)
        return avg_change > 0.5  # Detect if making consistent turns
    
    def break_loop(self):
        # Make a random significant direction change to break the loop
        self.angle += random.uniform(-math.pi, math.pi)
        self.previous_directions.clear()
        self.wander_strength = 0.8  # Temporarily increase randomness
    
    def search_for_food(self):
        left_angle = self.angle - self.sensor_angle
        right_angle = self.angle + self.sensor_angle
        
        # Add a forward-biased center sensor
        center_left_angle = self.angle - self.sensor_angle/3
        center_right_angle = self.angle + self.sensor_angle/3
        
        # Calculate sensor positions with multiple forward points
        sensors = [
            (left_angle, self.sensor_distance),
            (center_left_angle, self.sensor_distance * 1.2),
            (self.angle, self.sensor_distance * 1.5),
            (center_right_angle, self.sensor_distance * 1.2),
            (right_angle, self.sensor_distance)
        ]
        
        # Sample pheromones at all sensor positions
        max_pheromone = 0
        best_angle = self.angle
        
        for angle, distance in sensors:
            x = self.x + math.cos(angle) * distance
            y = self.y + math.sin(angle) * distance
            
            # Skip this direction if there's an obstacle
            if self.simulation.is_obstacle_at(x, y):
                continue
                
            pheromone = self.simulation.get_pheromone("food", int(x), int(y))
            
            if pheromone > max_pheromone:
                max_pheromone = pheromone
                best_angle = angle
        
        # Adjust direction with more randomness when no pheromones are found
        if max_pheromone > 0:
            # Smoother turning when following pheromones
            angle_diff = (best_angle - self.angle + 3 * math.pi) % (2 * math.pi) - math.pi
            self.angle += angle_diff * 0.3
        else:
            # More random movement when exploring
            self.angle += random.uniform(-self.wander_strength, self.wander_strength)
            
        # Gradually return wander_strength to normal if it was increased
        if self.wander_strength > 0.5:
            self.wander_strength = max(0.5, self.wander_strength * 0.95)
    
    def return_to_home(self):
        # Calculate direct vector to home
        home_x, home_y = self.simulation.home_position
        dx = home_x - self.x
        dy = home_y - self.y
        distance_to_home = math.sqrt(dx*dx + dy*dy)
        direct_home_angle = math.atan2(dy, dx)
        
        # If close to home, head directly there with high precision
        if distance_to_home < 200:  # Increased direct navigation range
            # Strong direct navigation when close
            angle_diff = (direct_home_angle - self.angle + 3 * math.pi) % (2 * math.pi) - math.pi
            self.angle += angle_diff * 0.5  # Stronger correction
            # Minimal randomness when close to home
            self.angle += random.uniform(-0.1, 0.1)
            return
            
        # Calculate sensor positions with wider spread when far from home
        left_angle = self.angle - self.sensor_angle
        right_angle = self.angle + self.sensor_angle
        
        # Sample pheromone concentrations at multiple points
        sensors = [
            (left_angle, self.sensor_distance),
            (self.angle - self.sensor_angle/2, self.sensor_distance * 1.2),
            (self.angle, self.sensor_distance * 1.5),
            (self.angle + self.sensor_angle/2, self.sensor_distance * 1.2),
            (right_angle, self.sensor_distance)
        ]
        
        max_pheromone = 0
        best_angle = direct_home_angle  # Default to direct home direction
        
        for angle, distance in sensors:
            x = self.x + math.cos(angle) * distance
            y = self.y + math.sin(angle) * distance
            
            if self.simulation.is_obstacle_at(x, y):
                continue
                
            pheromone = self.simulation.get_pheromone("home", int(x), int(y))
            if pheromone > max_pheromone:
                max_pheromone = pheromone
                best_angle = angle
        
        # Combine pheromone direction with direct home direction
        if max_pheromone > 0:
            # Weight between pheromone direction and direct home direction
            pheromone_weight = min(0.7, max_pheromone)  # Cap pheromone influence
            direct_weight = 1 - pheromone_weight
            
            # Calculate weighted angle
            pheromone_angle_diff = (best_angle - self.angle + 3 * math.pi) % (2 * math.pi) - math.pi
            direct_angle_diff = (direct_home_angle - self.angle + 3 * math.pi) % (2 * math.pi) - math.pi
            
            total_adjustment = (pheromone_angle_diff * pheromone_weight + 
                              direct_angle_diff * direct_weight)
            
            self.angle += total_adjustment * 0.3
        else:
            # No pheromones - use direct navigation with moderate precision
            angle_diff = (direct_home_angle - self.angle + 3 * math.pi) % (2 * math.pi) - math.pi
            self.angle += angle_diff * 0.3
        
        # Reduced randomness when returning home
        self.angle += random.uniform(-self.wander_strength/4, self.wander_strength/4)
    
    def move(self):
        # Calculate new position based on angle and speed
        new_x = self.x + math.cos(self.angle) * self.speed
        new_y = self.y + math.sin(self.angle) * self.speed
        
        # Check for collisions with obstacles
        if self.simulation.is_obstacle_at(new_x, new_y):
            # Try to find a clear direction
            clear_angle = self.find_clear_path()
            if clear_angle is not None:
                self.angle = clear_angle
                new_x = self.x + math.cos(self.angle) * self.speed
                new_y = self.y + math.sin(self.angle) * self.speed
            else:
                # If no clear path, reverse direction
                self.angle += math.pi + random.uniform(-0.5, 0.5)
                return
        
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

    def find_clear_path(self) -> float:
        # Try 8 different directions to find a clear path
        for i in range(8):
            test_angle = self.angle + (i * math.pi / 4)
            test_x = self.x + math.cos(test_angle) * (self.speed * 2)
            test_y = self.y + math.sin(test_angle) * (self.speed * 2)
            
            if not self.simulation.is_obstacle_at(test_x, test_y):
                return test_angle
        return None


class AntSimulation:
    def __init__(self, 
                 width: int = 1920, 
                 height: int = 1080, 
                 grid_scale: int = 10, 
                 num_ants: int = 2000,
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
        
        # Initialize obstacles grid
        self.obstacles = np.zeros((self.grid_width, self.grid_height), dtype=bool)
        
        # Pheromone decay rate
        self.decay_rate = 0.995
        
        # Home position (default to center)
        if home_position is None:
            self.home_position = (width // 2, height // 2)
        else:
            self.home_position = home_position
        
        # Food positions
        if food_positions is None:
            self.food_positions = []
            for _ in range(3):
                x = random.randint(100, self.width - 100)
                y = random.randint(100, self.height - 100)
                self.food_positions.append((x, y))
        else:
            self.food_positions = food_positions
        
        # Create the ants
        self.ants = [Ant(self, self.home_position) for _ in range(num_ants)]
        
        # Obstacle drawing state
        self.drawing_obstacle = False
        self.erasing_obstacle = False
        self.obstacle_size = 2  # Size in grid cells
    
    def update(self):
        # Update all ants
        for ant in self.ants:
            ant.update()
        
        # Apply pheromone decay
        # Only subtract decay_rate from values greater than decay_rate
        self.food_pheromones *= self.decay_rate
        self.home_pheromones *= self.decay_rate
        #self.food_pheromones[self.food_pheromones > self.decay_rate] -= self.decay_rate
        #self.home_pheromones[self.home_pheromones > self.decay_rate] -= self.decay_rate
        #self.food_pheromones[self.food_pheromones <= self.decay_rate] = 0
        #self.home_pheromones[self.home_pheromones <= self.decay_rate] = 0
    
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
    
    def add_obstacle(self, grid_x: int, grid_y: int, size: int = 2):
        for dx in range(-size, size + 1):
            for dy in range(-size, size + 1):
                x, y = grid_x + dx, grid_y + dy
                if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                    self.obstacles[x, y] = True
    
    def remove_obstacle(self, grid_x: int, grid_y: int, size: int = 2):
        for dx in range(-size, size + 1):
            for dy in range(-size, size + 1):
                x, y = grid_x + dx, grid_y + dy
                if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                    self.obstacles[x, y] = False
    
    def is_obstacle_at(self, x: int, y: int) -> bool:
        grid_x, grid_y = int(x // self.grid_scale), int(y // self.grid_scale)
        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
            return self.obstacles[grid_x, grid_y]
        return False


def main():
    pygame.init()
    width, height = 1920, 1080
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ant Colony Simulation")
    
    grid_scale = 20
    
    # Set home and food positions
    home_position = (width-150, 150)
    food_positions = [(width // 2 + 300, height // 2 + 200)]
    
    # Create simulation
    simulation = AntSimulation(width, height, grid_scale, num_ants=1000, 
                              home_position=home_position, 
                              food_positions=food_positions)
    
    clock = pygame.time.Clock()
    
    # UI elements
    show_food_pheromones = True
    show_home_pheromones = True
    food_checkbox_rect = pygame.Rect(20, 20, 20, 20)
    home_checkbox_rect = pygame.Rect(20, 50, 20, 20)
    font = pygame.font.SysFont(None, 24)
    
    # Obstacle controls
    obstacle_text = font.render("Left click: Draw obstacles | Right click: Erase | Mouse wheel: Size", True, (255, 255, 255))
    
    # Main loop
    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x, grid_y = mouse_x // grid_scale, mouse_y // grid_scale
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if food_checkbox_rect.collidepoint(event.pos):
                        show_food_pheromones = not show_food_pheromones
                    elif home_checkbox_rect.collidepoint(event.pos):
                        show_home_pheromones = not show_home_pheromones
                    else:
                        simulation.drawing_obstacle = True
                elif event.button == 3:  # Right click
                    simulation.erasing_obstacle = True
                elif event.button == 4:  # Mouse wheel up
                    simulation.obstacle_size = min(5, simulation.obstacle_size + 1)
                elif event.button == 5:  # Mouse wheel down
                    simulation.obstacle_size = max(1, simulation.obstacle_size - 1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    simulation.drawing_obstacle = False
                elif event.button == 3:
                    simulation.erasing_obstacle = False
            elif event.type == pygame.MOUSEMOTION:
                if simulation.drawing_obstacle:
                    simulation.add_obstacle(grid_x, grid_y, simulation.obstacle_size)
                elif simulation.erasing_obstacle:
                    simulation.remove_obstacle(grid_x, grid_y, simulation.obstacle_size)
        
        # Update simulation
        simulation.update()
        
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw the pheromone grid and obstacles
        for x in range(simulation.grid_width):
            for y in range(simulation.grid_height):
                # Draw obstacles
                if simulation.obstacles[x, y]:
                    pygame.draw.rect(screen, (128, 128, 128), 
                                   (x * grid_scale, y * grid_scale, grid_scale, grid_scale))
                else:
                    # Draw pheromones
                    food_intensity = min(255, simulation.food_pheromones[x, y] * 255)
                    home_intensity = min(255, simulation.home_pheromones[x, y] * 255)
                    
                    if (show_food_pheromones and food_intensity > 0) or (show_home_pheromones and home_intensity > 0):
                        food_display = int(food_intensity) if show_food_pheromones else 0
                        home_display = int(home_intensity) if show_home_pheromones else 0
                        color = (0, food_display, home_display)
                        pygame.draw.rect(screen, color, 
                                       (x * grid_scale, y * grid_scale, grid_scale, grid_scale))
        
        # Draw the food sources
        for food_x, food_y in simulation.food_positions:
            # Draw outer glow
            for r in range(5):
                alpha = 100 - r * 20
                radius = 50 - r * 2
                glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (0, 255, 0, alpha), (radius, radius), radius)
                screen.blit(glow_surface, (int(food_x) - radius, int(food_y) - radius))
            # Draw main food circle
            pygame.draw.circle(screen, (0, 255, 0), (int(food_x), int(food_y)), 20)
            # Draw center
            pygame.draw.circle(screen, (200, 255, 200), (int(food_x), int(food_y)), 10)
        
        # Draw the home
        home_x, home_y = simulation.home_position
        # Draw outer glow
        for r in range(5):
            alpha = 100 - r * 20
            radius = 50 - r * 2
            glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (0, 0, 255, alpha), (radius, radius), radius)
            screen.blit(glow_surface, (int(home_x) - radius, int(home_y) - radius))
        # Draw main home circle
        pygame.draw.circle(screen, (0, 0, 255), (int(home_x), int(home_y)), 25)
        # Draw center
        pygame.draw.circle(screen, (150, 150, 255), (int(home_x), int(home_y)), 15)
        
        # Draw the ants
        for ant in simulation.ants:
            color = (255, 0, 0) if ant.carrying_food else (255, 255, 255)
            pygame.draw.circle(screen, color, (int(ant.x), int(ant.y)), 2)
        
        # Draw UI elements
        pygame.draw.rect(screen, (255, 255, 255), food_checkbox_rect, 2)
        if show_food_pheromones:
            pygame.draw.rect(screen, (255, 255, 255), food_checkbox_rect.inflate(-8, -8))
        food_text = font.render("Show Food Pheromones (Green)", True, (0, 255, 0))
        screen.blit(food_text, (food_checkbox_rect.right + 10, food_checkbox_rect.top))
        
        pygame.draw.rect(screen, (255, 255, 255), home_checkbox_rect, 2)
        if show_home_pheromones:
            pygame.draw.rect(screen, (255, 255, 255), home_checkbox_rect.inflate(-8, -8))
        home_text = font.render("Show Home Pheromones (Blue)", True, (0, 0, 255))
        screen.blit(home_text, (home_checkbox_rect.right + 10, home_checkbox_rect.top))
        
        # Draw obstacle controls text
        screen.blit(obstacle_text, (20, height - 30))
        size_text = font.render(f"Obstacle size: {simulation.obstacle_size}", True, (255, 255, 255))
        screen.blit(size_text, (20, height - 60))
        
        # Display pheromone values at mouse position
        if 0 <= grid_x < simulation.grid_width and 0 <= grid_y < simulation.grid_height:
            food_value = simulation.food_pheromones[grid_x, grid_y]
            home_value = simulation.home_pheromones[grid_x, grid_y]
            is_obstacle = simulation.obstacles[grid_x, grid_y]
            
            info_surface = pygame.Surface((200, 100))  # Increased height for obstacle info
            info_surface.fill((0, 0, 0))
            info_surface.set_alpha(200)
            screen.blit(info_surface, (width - 220, 20))
            
            pos_text = font.render(f"Grid: ({grid_x}, {grid_y})", True, (255, 255, 255))
            screen.blit(pos_text, (width - 200, 30))
            
            food_info = font.render(f"Food: {food_value:.3f}", True, (0, 255, 0))
            home_info = font.render(f"Home: {home_value:.3f}", True, (0, 0, 255))
            obstacle_info = font.render(f"Obstacle: {is_obstacle}", True, (128, 128, 128))
            screen.blit(food_info, (width - 200, 50))
            screen.blit(home_info, (width - 200, 70))
            screen.blit(obstacle_info, (width - 200, 90))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()