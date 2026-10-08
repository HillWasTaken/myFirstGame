import pygame
import random
from food import spawnFood
from enemy import enemyAttack, spawnEnemy

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My first game")
clock = pygame.time.Clock()

x, y = 400, 300
speed = 150
stamina = 100
max_stamina = 100
sprint_multiplier = 2
stamina_drain = 35
stamina_regen = 20
player_radius = 20
enemy_speed = 150
enemy_radius = 20
player_health = 100
enemy_damage = 10
enemy_attack_interval = 1.0
enemy_attack_timer = 0
line_length = 35
bullet_speed = 600
bullet_radius = 5
bullets = []

food_x, food_y = spawnFood()
enemy_x, enemy_y = spawnEnemy()

running = True
counter = 0
font = pygame.font.Font(None, 32)

paused = False

while running:
    dt = clock.tick(60) / 1000  # seconds sinds last frame, max 60 FPS

    # 1. Input / events
    keys = pygame.key.get_pressed()
    fire_bullet = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            fire_bullet = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused = not paused

    if not paused:

        shift_held = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        sprinting = shift_held and stamina > 0
        if sprinting:
            current_speed = speed * sprint_multiplier
            stamina = max(0, stamina - stamina_drain * dt)
        else:
            current_speed = speed
            if not shift_held:
                stamina = min(max_stamina, stamina + stamina_regen * dt)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  x -= current_speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: x += current_speed * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:    y -= current_speed * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  y += current_speed * dt

        x = max(player_radius, min(x, screen.get_width() - player_radius))
        y = max(player_radius, min(y, screen.get_height() - player_radius))

        enemy_direction = pygame.math.Vector2(x - enemy_x, y - enemy_y)
        enemy_pos = pygame.math.Vector2(enemy_x, enemy_y)
        player_pos = pygame.math.Vector2(x, y)
        distance = enemy_pos.distance_to(player_pos)
        if distance > enemy_radius + player_radius:
            if enemy_direction.length_squared() > 0:
                enemy_direction.normalize_ip()
                enemy_x += enemy_direction.x * enemy_speed * dt
                enemy_y += enemy_direction.y * enemy_speed * dt

        enemy_attack_timer = max(0, enemy_attack_timer - dt)
        if enemy_attack_timer == 0 and enemyAttack((x, y), (enemy_x, enemy_y)):
            player_health = max(0, player_health - enemy_damage)
            enemy_attack_timer = enemy_attack_interval

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
                counter += 1
            elif (0 <= bullet["position"].x <= screen.get_width() and 0 <= bullet["position"].y <= screen.get_height()):
                remaining_bullets.append(bullet)
                
        bullets = remaining_bullets

        if pygame.math.Vector2(x,y).distance_to((food_x, food_y)) < 30:
            food_x, food_y = spawnFood()

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

    if not paused:
        text = font.render(
            f"Score: {counter}   Stamina: {int(stamina)}   Health: {player_health}",
            True,
            (255, 255, 255),
        )
        screen.blit(text, (10,10))
    else:
        pygame.draw.rect(screen, (217, 155, 141), pygame.Rect(30,30, (screen.get_width() - 60), (screen.get_height() - 60)), 1)
        text = font.render(
            f"Paused\nScore: {counter}   Stamina: {int(stamina)}   Health: {player_health}",
            True,
            (255,255,255)
        )
        screen.blit(text, ((screen.get_width() / 2.2), 50))

    pygame.display.flip()

pygame.quit()