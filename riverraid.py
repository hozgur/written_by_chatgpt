import pygame
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # River color

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

# Load the sprite sheet
sprite_sheet = pygame.image.load('riverraid.png').convert_alpha()

# Extract the individual sprites using the coordinates
player_image = pygame.transform.scale(sprite_sheet.subsurface((60, 10, 28, 28)), (40, 40))
enemy_image = pygame.transform.scale(sprite_sheet.subsurface((10, 45, 28, 28)), (40, 40))
boat_image = pygame.transform.scale(sprite_sheet.subsurface((90, 90, 48, 30)), (40, 25))
bullet_image = pygame.Surface((10, 10))
bullet_image.fill((255, 255, 0))  # Simple yellow bullet

# Sprite Groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

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

# Create player
player = Player()
all_sprites.add(player)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Add new enemy
    if random.randint(1, 20) == 1:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Add new obstacle
    if random.randint(1, 50) == 1:  # Less frequent than enemies
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    # Update sprites
    all_sprites.update()

    # Check for bullet-enemy collisions
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)

    # Check for player-enemy or player-obstacle collisions
    if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, obstacles):
        running = False

    # Fill screen with black
    screen.fill(BLACK)

    # Draw the river (a blue rectangle in the background)
    river_width = SCREEN_WIDTH // 2
    river_rect = pygame.Rect((SCREEN_WIDTH - river_width) // 2, 0, river_width, SCREEN_HEIGHT)
    pygame.draw.rect(screen, BLUE, river_rect)

    # Draw all sprites
    all_sprites.draw(screen)

    # Refresh the screen
    pygame.display.flip()

    # Control game speed
    clock.tick(30)

# Quit pygame
pygame.quit()
