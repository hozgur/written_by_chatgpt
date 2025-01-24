import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 3
FUEL_CONSUMPTION = 0.1
HIGH_SCORE_FILE = "highscore.txt"

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
    surf = pygame.Surface((40, 30), pygame.SRCALPHA)
    pygame.draw.polygon(surf, WHITE, [(20, 0), (40, 30), (0, 30)])
    pygame.draw.line(surf, RED, (15, 15), (25, 15), 2)
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
    surf = pygame.Surface((50, 10), pygame.SRCALPHA)
    pygame.draw.polygon(surf, DARK_GREEN, [(0, 10), (50, 10), (40, 0), (10, 0)])
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
        self.width = river_bank_img.get_width()
        self.left_image = pygame.transform.flip(river_bank_img, True, False)
        self.right_image = river_bank_img

    def draw(self, surface, banks):
        for y, (left, right) in enumerate(banks):
            surface.blit(self.left_image, (left - self.width, y * 10))
            surface.blit(self.right_image, (right, y * 10))

def generate_river_banks():
    return [[WIDTH//2 - 100, WIDTH//2 + 100] for _ in range(HEIGHT//10)]

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