import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("River Raid")

# Load sprites
sprite_sheet = pygame.image.load("riverraid.png").convert_alpha()

# Function to get sprite from sheet
def get_sprite(x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sprite_sheet, (0, 0), (x, y, width, height))
    return sprite

# Player sprite
player_sprite = get_sprite(0, 0, 50, 30)
player = player_sprite.get_rect()
player.centerx = width // 2
player.bottom = height - 10
player_speed = 5

# Enemy sprite
enemy_sprite = get_sprite(50, 0, 30, 30)

# Bullet sprite
bullet_sprite = get_sprite(80, 0, 4, 10)

# Fuel sprite
fuel_sprite = get_sprite(84, 0, 30, 30)

# River
river_width = 300
river_x = (width - river_width) // 2

# Enemies
enemies = []
enemy_speed = 3
enemy_spawn_timer = 0

# Bullets
bullets = []
bullet_speed = 7

# Game loop
clock = pygame.time.Clock()
running = True

def spawn_enemy():
    x = random.randint(river_x, river_x + river_width - enemy_sprite.get_width())
    enemy = enemy_sprite.get_rect(topleft=(x, -enemy_sprite.get_height()))
    enemies.append(enemy)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player.centerx - 2, player.top, 4, 10)
                bullets.append(bullet)

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > river_x:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < river_x + river_width:
        player.x += player_speed

    # Move and remove bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Spawn and move enemies
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= 60:
        spawn_enemy()
        enemy_spawn_timer = 0

    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.top > height:
            enemies.remove(enemy)

    # Check for collisions
    for enemy in enemies[:]:
        if player.colliderect(enemy):
            running = False
        for bullet in bullets[:]:
            if bullet.colliderect(enemy):
                enemies.remove(enemy)
                bullets.remove(bullet)
                break

    # Draw everything
    screen.fill((0, 255, 0))  # Green background
    pygame.draw.rect(screen, (0, 0, 255), (river_x, 0, river_width, height))  # Blue river
    screen.blit(player_sprite, player)
    for enemy in enemies:
        screen.blit(enemy_sprite, enemy)
    for bullet in bullets:
        screen.blit(bullet_sprite, bullet)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()