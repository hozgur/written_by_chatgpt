import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Game constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 3
FUEL_CONSUMPTION = 0.1
HIGH_SCORE_FILE = os.path.join(script_dir, "highscore.txt")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 100, 0)
GREY = (128, 128, 128)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("River Raid")

clock = pygame.time.Clock()

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0
    except:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write(str(score))

# Generate assets programmatically
def create_player_image():
    surf = pygame.Surface((50, 40), pygame.SRCALPHA)
    # Main body with gradient
    for i in range(40):
        shade = 200 - int(i * 3)
        pygame.draw.line(surf, (shade, shade, shade), (25, i), (25, i), 3)
    # Wings
    pygame.draw.polygon(surf, (180, 180, 180), [
        (15, 25), (35, 25), 
        (40, 35), (10, 35)
    ])
    # Cockpit
    pygame.draw.circle(surf, (0, 0, 150), (25, 15), 5)
    # Afterburner
    for i in range(5):
        pygame.draw.line(surf, (255, 165 - i*30, 0), 
                        (25, 38 - i), (25, 38 - i), 2)
    # Wing details
    pygame.draw.line(surf, (100, 100, 100), (20, 28), (30, 28), 2)
    return surf

def create_bullet_image():
    surf = pygame.Surface((5, 15), pygame.SRCALPHA)
    pygame.draw.rect(surf, YELLOW, (0, 0, 5, 15))
    return surf

def create_helicopter_image():
    surf = pygame.Surface((50, 30), pygame.SRCALPHA)
    pygame.draw.rect(surf, RED, (5, 10, 40, 15))
    pygame.draw.circle(surf, GREY, (25, 5), 10)
    pygame.draw.line(surf, BLACK, (25, 5), (25, 15), 2)
    return surf

def create_tank_image():
    surf = pygame.Surface((40, 20), pygame.SRCALPHA)
    pygame.draw.rect(surf, DARK_GREEN, (0, 5, 40, 15))
    pygame.draw.rect(surf, GREEN, (10, 0, 20, 10))
    pygame.draw.line(surf, BLACK, (30, 5), (35, 0), 3)
    return surf

def create_fuel_image():
    surf = pygame.Surface((20, 30), pygame.SRCALPHA)
    pygame.draw.rect(surf, GREEN, (5, 5, 10, 20))
    pygame.draw.rect(surf, YELLOW, (5, 0, 10, 5))
    return surf

def create_river_bank_image():
    surf = pygame.Surface((80, 25), pygame.SRCALPHA)
    
    # Layered soil profile
    for y in range(25):
        # Base layer (dark soil)
        soil_color = (
            30 + y*2,
            20 + y,
            0,
            255 - int(y * 8)
        )
        pygame.draw.line(surf, soil_color, (0, y), (80, y))
        
        # Top layer texture (sandy soil)
        if y < 15:
            for x in range(0, 80, 3):
                if random.random() < 0.3:
                    shade = random.randint(150, 180)
                    pygame.draw.line(surf, (shade, shade-20, 0, 200), 
                                    (x, y), (x+2, y), 1)

    # Natural vegetation clusters
    for _ in range(8):  # Fewer clusters but more detailed
        cluster_x = random.randint(0, 80)
        cluster_y = random.randint(0, 15)
        plant_type = random.choice(["reed_cluster", "bush_cluster", "mixed_vegetation"])
        
        if plant_type == "reed_cluster":
            # Group of reeds in a natural pattern
            for _ in range(random.randint(3,6)):
                x = cluster_x + random.randint(-5,5)
                y = cluster_y + random.randint(0,3)
                height = random.randint(4,8)
                for i in range(height):
                    shade = (80 + i*2, 90 + i*3, 0, 200 - i*20)
                    pygame.draw.line(surf, shade, (x, y-i), (x, y-i), 2)
                pygame.draw.circle(surf, (100, 110, 0, 220), (x, y-height-1), 2)
                
        elif plant_type == "bush_cluster":
            # Cluster of overlapping bushes
            base_color = (random.randint(0,10), 
                         random.randint(80,100), 
                         0, 
                         200)
            for _ in range(random.randint(2,4)):
                x = cluster_x + random.randint(-8,8)
                y = cluster_y + random.randint(-2,2)
                width = random.randint(6,10)
                height = random.randint(4,6)
                pygame.draw.ellipse(surf, base_color, (x, y, width, height))
                
        elif plant_type == "mixed_vegetation":
            # Combination of grasses and small plants
            for _ in range(random.randint(4,8)):
                x = cluster_x + random.randint(-10,10)
                y = cluster_y + random.randint(-3,3)
                if random.random() < 0.7:
                    # Grass blades
                    length = random.randint(3,6)
                    angle = random.uniform(-0.3, 0.3)
                    end_x = x + math.cos(angle) * length
                    end_y = y - math.sin(angle) * length
                    pygame.draw.line(surf, 
                        (40, 80 + random.randint(0,20), 0, 220), 
                        (x, y), (end_x, end_y), 1)
                else:
                    # Small flowers
                    pygame.draw.circle(surf, 
                        random.choice([(255,215,0,220), (255,0,0,220)]), 
                        (x, y), 1)

    # Water's edge details
    for x in range(0, 80, 4):
        if random.random() < 0.4:
            # Small waves/ripples
            pygame.draw.arc(surf, (50, 80, 150, 150), 
                           (x-2, 22, 4, 2), math.pi, 2*math.pi, 1)
            
            # Rocky texture
            if random.random() < 0.3:
                pygame.draw.polygon(surf, (80, 70, 60, 220),
                    [(x, 23), (x+1, 22), (x+2, 23), (x+1, 24)])

    return surf

def create_background_image():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill((0, 0, 30))
    for _ in range(200):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        pygame.draw.circle(surf, WHITE, (x, y), 1)
    return surf

# Create all assets
player_img = create_player_image()
bullet_img = create_bullet_image()
helicopter_img = create_helicopter_image()
tank_img = create_tank_image()
fuel_img = create_fuel_image()
river_bank_img = create_river_bank_image()
background_img = create_background_image()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-50))
        self.fuel = 100
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dx):
        self.rect.x += dx * PLAYER_SPEED
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.fuel = max(0, self.fuel - FUEL_CONSUMPTION)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        self.image = helicopter_img if enemy_type == "helicopter" else tank_img
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += ENEMY_SPEED
        if self.rect.top > HEIGHT:
            self.kill()

class Fuel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = fuel_img
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += ENEMY_SPEED
        if self.rect.top > HEIGHT:
            self.kill()

class RiverBank:
    def __init__(self):
        self.colors = [
            (20, 40, 0),      # Darkest base
            (30, 55, 0),      # Dark base
            (40, 70, 0),      # Mid dark
            (50, 85, 0),      # Mid tone
            (60, 100, 0),     # Light tone
            (0, 50, 150)      # Water edge
        ]
        # Initialize vegetation tracking
        self.vegetation_left = []
        self.vegetation_right = []
        self.next_plant_y = 0
        
    def draw(self, surface, banks):
        # Create layers surface for blending
        layers = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Generate base points
        left_points = [(0, 0)]
        right_points = [(WIDTH, 0)]
        for y, (left, right) in enumerate(banks):
            y_coord = y * 10
            left_points.append((left, y_coord))
            right_points.append((right, y_coord))
        left_points.append((0, HEIGHT))
        right_points.append((WIDTH, HEIGHT))
        
        # Draw multiple gradient layers
        for i, color in enumerate(self.colors[:-1]):  # Skip water edge color
            # Offset each layer slightly for depth
            offset = i * 4
            
            # Left bank with adjusted points
            left_layer = [(p[0] + offset, p[1]) for p in left_points]
            pygame.draw.polygon(layers, (*color, 255 - i * 20), left_layer)
            
            # Right bank with adjusted points
            right_layer = [(p[0] - offset, p[1]) for p in right_points]
            pygame.draw.polygon(layers, (*color, 255 - i * 20), right_layer)
            
            # Add highlight lines for texture
            if i > 0:
                for y, (left, right) in enumerate(banks):
                    if random.random() < 0.3:
                        y_coord = y * 10
                        # Left bank highlights
                        highlight_x = left + offset + random.randint(0, 8)
                        pygame.draw.line(layers, 
                            (*color, 100),
                            (highlight_x, y_coord),
                            (highlight_x + random.randint(5, 15), y_coord + random.randint(5, 10)),
                            2)
                        # Right bank highlights
                        highlight_x = right - offset - random.randint(0, 8)
                        pygame.draw.line(layers, 
                            (*color, 100),
                            (highlight_x, y_coord),
                            (highlight_x - random.randint(5, 15), y_coord + random.randint(5, 10)),
                            2)
        
        # Draw water edges with glow effect
        water_edge = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y, (left, right) in enumerate(banks):
            y_coord = y * 10
            # Outer glow
            for i in range(3):
                alpha = 60 - i * 20
                pygame.draw.line(water_edge, (*self.colors[-1], alpha),
                               (left - i, y_coord), (left - i, y_coord + 10), 2)
                pygame.draw.line(water_edge, (*self.colors[-1], alpha),
                               (right + i, y_coord), (right + i, y_coord + 10), 2)
            
            # Main edge
            pygame.draw.line(water_edge, (*self.colors[-1], 150),
                           (left, y_coord), (left, y_coord + 10), 2)
            pygame.draw.line(water_edge, (*self.colors[-1], 150),
                           (right, y_coord), (right, y_coord + 10), 2)
            
            # Add water ripples
            if random.random() < 0.2:
                for x_offset in range(-2, 3, 2):
                    pygame.draw.arc(water_edge, (*self.colors[-1], 100),
                                  (left + x_offset, y_coord, 4, 4),
                                  0, math.pi, 1)
                    pygame.draw.arc(water_edge, (*self.colors[-1], 100),
                                  (right + x_offset, y_coord, 4, 4),
                                  0, math.pi, 1)
        
        # Update and draw vegetation
        self.update_vegetation(banks)
        self.draw_vegetation(layers)
        
        # Combine all layers
        surface.blit(layers, (0, 0))
        surface.blit(water_edge, (0, 0))
    
    def update_vegetation(self, banks):
        # Remove vegetation that's moved off screen
        self.vegetation_left = [(x, y+1) for x, y in self.vegetation_left if y < HEIGHT]
        self.vegetation_right = [(x, y+1) for x, y in self.vegetation_right if y < HEIGHT]
        
        # Add new vegetation at the top when needed
        while self.next_plant_y <= 0:
            if len(banks) > 0:
                left, right = banks[0]
                # Add left bank vegetation
                if random.random() < 0.3:
                    x = left - random.randint(5, 15)
                    self.vegetation_left.append((x, self.next_plant_y))
                # Add right bank vegetation
                if random.random() < 0.3:
                    x = right + random.randint(5, 15)
                    self.vegetation_right.append((x, self.next_plant_y))
            self.next_plant_y += random.randint(20, 40)  # Space between plants
        self.next_plant_y -= 1
        
    def draw_vegetation(self, surface):
        for x, y in self.vegetation_left + self.vegetation_right:
            if 0 <= y < HEIGHT:
                self.draw_stylized_plant(surface, x, y)
    
    def draw_stylized_plant(self, surface, x, y):
        # Base plant parameters
        height = random.randint(8, 15)
        width = random.randint(4, 8)
        
        # Draw layered plant shape for depth
        for layer in range(3):
            # Gradient colors for depth
            color = (
                40 + layer * 10,
                80 + layer * 15,
                0,
                200 - layer * 30
            )
            
            # Offset each layer slightly
            offset = layer * 2
            points = [
                (x, y - offset),
                (x - width, y + height - offset),
                (x + width, y + height - offset)
            ]
            
            # Draw base shape
            pygame.draw.polygon(surface, color, points)
            
            # Add detail lines for texture
            if random.random() < 0.5:
                detail_y = y + height//2 - offset
                pygame.draw.line(surface,
                    (120, 150, 0, 100),
                    (x - width//2, detail_y),
                    (x + width//2, detail_y),
                    1)

def generate_river_banks():
    """Generate smoother river banks"""
    banks = []
    # Start with middle positions
    left_pos = WIDTH//2 - 100
    right_pos = WIDTH//2 + 100
    
    # Generate initial control points
    control_points = []
    num_controls = 8
    for i in range(num_controls):
        left = left_pos + random.randint(-30, 30)
        right = right_pos + random.randint(-30, 30)
        control_points.append((left, right))
    
    # Generate smooth bank positions using control points
    for i in range(HEIGHT//10):
        # Find the two nearest control points
        control_idx = (i * (num_controls-1)) // (HEIGHT//10)
        next_idx = min(control_idx + 1, num_controls-1)
        blend = ((i * (num_controls-1)) % (HEIGHT//10)) / (HEIGHT//10)
        
        # Interpolate between control points
        left = int(control_points[control_idx][0] * (1-blend) + 
                  control_points[next_idx][0] * blend)
        right = int(control_points[control_idx][1] * (1-blend) + 
                   control_points[next_idx][1] * blend)
        
        # Ensure minimum width and screen bounds
        if right - left < 150:
            center = (left + right) // 2
            left = center - 75
            right = center + 75
            
        left = max(50, min(left, WIDTH//2 - 50))
        right = max(WIDTH//2 + 50, min(right, WIDTH - 50))
        
        banks.append([left, right])
    
    return banks

def show_game_over_screen(screen, score, high_score):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 64)
    game_over_text = font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))
    
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    restart_text = font.render("Press SPACE to restart or ESC to quit", True, WHITE)
    
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 40))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 100))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE:
                    return True
    return False

def game():
    # Initialize pygame modules and screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("River Raid")
    
    playing = True
    while playing:
        # Load high score at start
        high_score = load_high_score()
        
        player = Player()
        all_sprites = pygame.sprite.Group(player)
        bullets = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        fuels = pygame.sprite.Group()
        
        river_banks = generate_river_banks()
        river = RiverBank()
        
        score = 0
        running = True
        dx = 0

        while running:
            screen.blit(background_img, (0, 0))
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = Bullet(player.rect.centerx, player.rect.top)
                        all_sprites.add(bullet)
                        bullets.add(bullet)

            # Player movement
            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            
            # Spawning
            if random.random() < 0.02:
                x = random.randint(river_banks[-1][0] + 20, river_banks[-1][1] - 20)
                enemies.add(Enemy(x, -20, random.choice(["helicopter", "tank"])))
            if random.random() < 0.01:
                x = random.randint(river_banks[-1][0] + 20, river_banks[-1][1] - 20)
                fuels.add(Fuel(x, -20))
            
            # Update - separate sprite updates by type
            player.update(dx)
            bullets.update()
            enemies.update()
            fuels.update()
            river_banks.pop(0)
            new_left = river_banks[-1][0] + random.randint(-2, 2)
            new_right = river_banks[-1][1] + random.randint(-2, 2)
            river_banks.append([max(50, min(new_left, WIDTH-200)), 
                              min(WIDTH-50, max(new_right, 200))])
            
            # Collision detection
            if (player.rect.left < river_banks[player.rect.centery//10][0] or 
                player.rect.right > river_banks[player.rect.centery//10][1]):
                running = False
                
            if pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask):
                running = False
                
            for bullet in pygame.sprite.groupcollide(bullets, enemies, True, True, pygame.sprite.collide_mask):
                score += 100
                
            if pygame.sprite.spritecollide(player, fuels, True, pygame.sprite.collide_mask):
                player.fuel = min(100, player.fuel + 25)
            
            if player.fuel <= 0:
                running = False
            
            # Drawing
            river.draw(screen, river_banks)
            all_sprites.draw(screen)
            bullets.draw(screen)
            enemies.draw(screen)
            fuels.draw(screen)
            
            # UI
            pygame.draw.rect(screen, (50, 50, 50), (10, 10, 204, 24))
            pygame.draw.rect(screen, (0, 200, 0), (12, 12, player.fuel * 2, 20))
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 40))
            screen.blit(pygame.transform.scale(fuel_img, (30, 30)), (WIDTH-50, 10))
            
            pygame.display.flip()
            clock.tick(60)

        # Save high score if new high score
        if score > high_score:
            save_high_score(score)
            high_score = score

        # Show game over screen and check if player wants to restart
        playing = show_game_over_screen(screen, score, high_score)

    pygame.quit()

if __name__ == "__main__":
    game()