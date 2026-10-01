import random
import pygame

def spawnEnemy():
    x = random.randrange(25, 775)
    y = random.randrange(25, 575)
    return x, y

def enemyAttack(player_pos, enemy_pos):
    player_position = pygame.math.Vector2(player_pos)
    enemy_position = pygame.math.Vector2(enemy_pos)
    return player_position.distance_to(enemy_position) <= 40