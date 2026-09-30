import pygame
import random
from spawnFood import spawnFood
from enemy import spawnEnemy

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My first game")
clock = pygame.time.Clock()

x, y = 400, 300
speed = 300
player_radius = 20
enemy_speed = 150
enemy_radius = 20
line_length = 35
bullet_speed = 600
bullet_radius = 5
bullets = []

food_x, food_y = spawnFood()
enemy_x, enemy_y = spawnEnemy()

running = True
counter = 0
font = pygame.font.Font(None, 32)

while running:
    dt = clock.tick(60) / 1000  # seconds sinds last frame, max 60 FPS

    # 1. Input / events
    fire_bullet = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            fire_bullet = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:  x -= speed * dt
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: x += speed * dt
    if keys[pygame.K_UP] or keys[pygame.K_w]:    y -= speed * dt
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:  y += speed * dt

    x = max(player_radius, min(x, screen.get_width() - player_radius))
    y = max(player_radius, min(y, screen.get_height() - player_radius))

    enemy_direction = pygame.math.Vector2(x - enemy_x, y - enemy_y)
    if enemy_direction.length_squared() > 0:
        enemy_direction.normalize_ip()
        enemy_x += enemy_direction.x * enemy_speed * dt
        enemy_y += enemy_direction.y * enemy_speed * dt

    mouse_x, mouse_y = pygame.mouse.get_pos()
    direction = pygame.math.Vector2(mouse_x - x, mouse_y - y)
    if direction.length_squared() > 0:
        direction.normalize_ip()

        if fire_bullet:
            bullet_position = pygame.math.Vector2(x, y) + direction * line_length
            bullets.append({
                "position": bullet_position,
                "velocity": direction * bullet_speed,
            })

    remaining_bullets = []

    for bullet in bullets:
        bullet["position"] += bullet["velocity"] * dt

        if bullet["position"].distance_to((food_x, food_y)) < bullet_radius + 10:
            food_x, food_y = spawnFood()
            counter -= 1
        elif bullet["position"].distance_to((enemy_x, enemy_y)) < bullet_radius + enemy_radius:
            enemy_x, enemy_y = spawnEnemy()
        elif (0 <= bullet["position"].x <= screen.get_width() and 0 <= bullet["position"].y <= screen.get_height()):
            remaining_bullets.append(bullet)
            
    bullets = remaining_bullets

    if pygame.math.Vector2(x,y).distance_to((food_x, food_y)) < 30:
        food_x, food_y = spawnFood()
        counter += 1

    # Draw
    screen.fill((20, 20, 30))

    # Food
    pygame.draw.circle(screen, (80, 220, 100), (food_x, food_y), 10)

    # Player
    pygame.draw.circle(screen, (255, 80, 80), (int(x), int(y)), player_radius)
    line_end = (int(x + direction.x * line_length), int(y + direction.y * line_length))
    pygame.draw.line(screen, (255, 80, 80), (int(x), int(y)), line_end, 5)
    pygame.draw.circle(screen, (255, 80, 80), line_end, 2)

    #Enemy
    pygame.draw.circle(screen, (100, 0, 0), (int(enemy_x), int(enemy_y)), enemy_radius)

    # Bullet
    for bullet in bullets:
        bullet_center = (int(bullet["position"].x), int(bullet["position"].y))
        pygame.draw.circle(screen, (255, 230, 80), bullet_center, bullet_radius)

    text = font.render(f"Score: {counter}", True, (255,255,255))
    screen.blit(text, (10,10))

    pygame.display.flip()

pygame.quit()