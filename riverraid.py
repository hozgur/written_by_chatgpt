import pygame
import random
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # River color
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("River Raid with Obstacles")

# Game clock
clock = pygame.time.Clock()

# Speed
player_speed = 5
enemy_speed = 5
bullet_speed = 10
obstacle_speed = 4

# Game variables
score = 0
lives = 3
fuel = 100
MAX_FUEL = 100
FUEL_CONSUMPTION = 0.2
level = 1

# Font for score display
font = pygame.font.Font(None, 36)

# Load sounds
class DummySound:
    def play(self):
        pass

try:
    shoot_sound = pygame.mixer.Sound('shoot.wav')
    explosion_sound = pygame.mixer.Sound('explosion.wav')
    refuel_sound = pygame.mixer.Sound('refuel.wav')
except:
    # If sound files are missing, create silent dummy sounds
    shoot_sound = DummySound()
    explosion_sound = DummySound()
    refuel_sound = DummySound()

# Load the sprite sheet
sprite_sheet = pygame.image.load('riverraid.png').convert_alpha()

# Extract the individual sprites using the coordinates
player_image = pygame.transform.scale(sprite_sheet.subsurface((60, 10, 28, 28)), (40, 40))
enemy_image = pygame.transform.scale(sprite_sheet.subsurface((10, 45, 28, 28)), (40, 40))
boat_image = pygame.transform.scale(sprite_sheet.subsurface((90, 90, 48, 30)), (40, 25))
bullet_image = pygame.Surface((10, 10))
bullet_image.fill((255, 255, 0))  # Simple yellow bullet

# Create fuel tank image
fuel_tank_image = pygame.Surface((30, 40))
fuel_tank_image.fill((0, 0, 0))  # Fill with black for transparency
fuel_tank_image.set_colorkey((0, 0, 0))  # Make black transparent

# Main tank body (silver/metallic)
pygame.draw.rect(fuel_tank_image, (192, 192, 192), (5, 10, 20, 25))  # Main body
pygame.draw.rect(fuel_tank_image, (128, 128, 128), (5, 10, 20, 5))   # Top shadow
pygame.draw.rect(fuel_tank_image, (160, 160, 160), (5, 30, 20, 5))   # Bottom shadow

# Tank cap (darker metal)
pygame.draw.rect(fuel_tank_image, (100, 100, 100), (10, 5, 10, 5))   # Cap

# Warning stripes (yellow and black)
pygame.draw.rect(fuel_tank_image, (255, 215, 0), (5, 15, 20, 5))     # Yellow stripe
pygame.draw.rect(fuel_tank_image, (255, 0, 0), (5, 20, 20, 5))       # Red stripe

# Fuel symbol (F)
font_small = pygame.font.Font(None, 20)
fuel_text = font_small.render("F", True, (0, 0, 0))
fuel_tank_image.blit(fuel_text, (12, 25))

# Sprite Groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
fuel_tanks = pygame.sprite.Group()

# Player Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += player_speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= player_speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += player_speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Enemy Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

    def update(self):
        self.rect.y += enemy_speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Obstacle Sprite
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = boat_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint((SCREEN_WIDTH - SCREEN_WIDTH // 2) // 2, SCREEN_WIDTH - (SCREEN_WIDTH // 2) // 2 - self.rect.width)
        self.rect.y = random.randint(-200, -100)

    def update(self):
        self.rect.y += obstacle_speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Bullet Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

    def update(self):
        self.rect.y -= bullet_speed
        if self.rect.bottom < 0:
            self.kill()

# Add FuelTank class after the Bullet class
class FuelTank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = fuel_tank_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint((SCREEN_WIDTH - SCREEN_WIDTH // 2) // 2, 
                                   SCREEN_WIDTH - (SCREEN_WIDTH // 2) // 2 - self.rect.width)
        self.rect.y = random.randint(-200, -100)

    def update(self):
        self.rect.y += obstacle_speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Create player
player = Player()
all_sprites.add(player)

# Game loop
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()
                shoot_sound.play()
            if event.key == pygame.K_r and game_over:
                # Reset game
                game_over = False
                score = 0
                lives = 3
                fuel = MAX_FUEL
                level = 1
                # Clear all sprites
                for sprite in all_sprites:
                    sprite.kill()
                # Create new player
                player = Player()
                all_sprites.add(player)

    if not game_over:
        # Decrease fuel
        fuel -= FUEL_CONSUMPTION * (level * 0.5)
        if fuel <= 0:
            lives -= 1
            if lives > 0:
                fuel = MAX_FUEL
            else:
                game_over = True

        # Add new enemy
        if random.randint(1, max(20 - level, 5)) == 1:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Add new obstacle
        if random.randint(1, max(50 - level, 20)) == 1:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

        # Add new fuel tank
        if random.randint(1, 100) == 1:
            fuel_tank = FuelTank()
            all_sprites.add(fuel_tank)
            fuel_tanks.add(fuel_tank)

        # Update sprites
        all_sprites.update()

        # Check for bullet-enemy collisions
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 100
            explosion_sound.play()

        # Check for player-fuel tank collisions (refueling by flying over)
        fuel_collisions = pygame.sprite.spritecollide(player, fuel_tanks, True)
        if fuel_collisions:
            old_fuel = fuel
            fuel = min(fuel + 30, MAX_FUEL)
            if fuel > old_fuel:  # Only play sound and add score if fuel was actually added
                score += 50
                refuel_sound.play()

        # Check for player-enemy or player-obstacle collisions
        if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, obstacles):
            lives -= 1
            explosion_sound.play()
            if lives <= 0:
                game_over = True
            else:
                # Reset player position
                player.rect.centerx = SCREEN_WIDTH // 2
                player.rect.bottom = SCREEN_HEIGHT - 10
                # Clear enemies and obstacles
                for sprite in enemies:
                    sprite.kill()
                for sprite in obstacles:
                    sprite.kill()

        # Increase level every 1000 points
        level = max(1, score // 1000 + 1)

    # Fill screen with black
    screen.fill(BLACK)

    # Draw the river
    river_width = SCREEN_WIDTH // 2
    river_rect = pygame.Rect((SCREEN_WIDTH - river_width) // 2, 0, river_width, SCREEN_HEIGHT)
    pygame.draw.rect(screen, BLUE, river_rect)

    # Draw all sprites
    all_sprites.draw(screen)

    # Draw HUD
    score_text = font.render(f'Score: {score}', True, WHITE)
    lives_text = font.render(f'Lives: {lives}', True, WHITE)
    fuel_text = font.render(f'Fuel: {int(fuel)}', True, WHITE if fuel > 30 else RED)
    level_text = font.render(f'Level: {level}', True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(fuel_text, (10, 70))
    screen.blit(level_text, (10, 100))

    if game_over:
        game_over_text = font.render('GAME OVER - Press R to Restart', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(game_over_text, text_rect)

    # Refresh the screen
    pygame.display.flip()

    # Control game speed
    clock.tick(30)

# Quit pygame
pygame.quit()
