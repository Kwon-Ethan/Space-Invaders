import pygame
import os
import random
import math
from pygame import mixer

#Initialise pygame
pygame.init()

#Centre the game window to the middle of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'
#Set the window's size to 800 by 600
window = pygame.display.set_mode((800,600))
#Set the display caption to "Space Invaders"
pygame.display.set_caption("Space Invaders")
#Set the variable windowIcon to the picture of the ufo
windowIcon = pygame.image.load('ufo.png')
#Display the icon as windowIcon
pygame.display.set_icon(windowIcon)

#Background
backgroundImg = pygame.image.load('background.jpg')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

gameIsOver = False

#Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerXChange = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for index in range (num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = -10
bullet_state = True

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)
over_textX = 200
over_textY = 250

restart_textX = 200
restart_textY = 350

def player(x,y):
    window.blit(playerImg, (x, y))

def enemy(x,y,i):
    window.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = False
    window.blit(bulletImg, (x + 16,y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def showScore(x,y):
    score = font.render("Score:" + str(score_value), True, (255,255,255))
    window.blit(score, (x, y))

def game_over_text(x, y, rx, ry):
    gameIsOver = True
    restart_text = font.render("Press R to Restart", True, (255,255,255))
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    window.blit(restart_text, (rx, ry))
    window.blit(over_text, (x, y))

    

run = True

while run:
    window.fill((0,0,0))
    window.blit(backgroundImg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and gameIsOver:
                gameIsOver = False
                bullet_state = True
                restart_textY = 2000
                playerY = 480
                over_textY = 2000
                score_value = 0
                for i in range(num_of_enemies):
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(0, 150)
            if event.key == pygame.K_LEFT:
                playerXChange = -4
            if event.key == pygame.K_RIGHT:
                playerXChange = 4
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                if bullet_state and not gameIsOver:
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0

    #Player movement
    playerX += playerXChange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy movement
    for i in range(num_of_enemies):
        
        #Game Over
        if enemyY[i] > 440:
            over_textY = 250
            restart_textY = 350
            gameIsOver = True
            playerY = 2000
            bullet_state = True
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(over_textX, over_textY, restart_textX, restart_textY)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        
        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = True
            score_value += 100
            collision = False
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 150)
        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= -32:
        bulletY = 480
        bullet_state = True

    #Bullet movement
    if not bullet_state and not gameIsOver:
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change
    
    if gameIsOver:
        game_over_text(over_textX, over_textY, restart_textX, restart_textY)

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
