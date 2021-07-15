import random
import math
from unicodedata import numeric

import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

background = pygame.image.load("background.png")

mixer.music.load("background.wav")
mixer.music.play(-1)

player_img = pygame.image.load("player.png")
player_x = 370
player_y = 480
player_x_change = 0

enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_stage = "ready"

score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score_object = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_object, (x, y))

def game_over():
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_stage
    bullet_stage = "fire"
    screen.blit(bullet_img, (x+16, y+10))

def is_collision(ex, ey, bx, by):
    d = math.sqrt((ex - bx)**2 + (ey - by)**2)
    return d < 27;

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_stage == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(number_of_enemies):
        if enemy_y[i] > 440:
            for j in range(number_of_enemies):
                enemy_y[j] = 2000
            game_over()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion = mixer.Sound("explosion.wav")
            explosion.play()
            bullet_y = 480
            bullet_stage = "ready"
            score += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        enemy(enemy_x[i], enemy_y[i], i)

        
    if bullet_y <= 0:
        bullet_y = 480
        bullet_stage = "ready"

    if bullet_stage == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
