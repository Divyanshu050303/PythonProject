import pygame
import random
import math
from pygame import mixer
# intialize
pygame.init()
clock=pygame.time.  Clock()
# create the screen
screen=pygame.display.set_mode((800, 600))
# background
background=pygame.image.load('2799006.jpg')
mixer.music.load("background.wav")
mixer.music.play(-1)
# Title and caption
pygame.display.set_caption("space invaders ")
icon=pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
# Player
playerimg=pygame.image.load("spaceship (4).png")
playerx=370
playery=400
player_change=0
# enemy
enemyimg=[]
enemyx=[]
enemyy=[]
enemyx_change=[]
enemyy_change=[]
num_enemy=6
for i in range(6):

    enemyimg.append(pygame.image.load("ufo.png"))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(2)
    enemyy_change.append(40)
# bullet
bulletimg=pygame.image.load("bullet.png")
bulletx=0
bullety=400
bulletx_change=0
bullety_change=10
bullet_state="ready"


score_value=0
font = pygame.font.Font('freesansbold.ttf', 32)

textx = 10
testy = 10
# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)
def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))
def bullet_fire(x, y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg, (x+10, y+8))
def incollision(bulletx, bullety, enemyy, enemyx):
    distance=math.sqrt(math.pow(enemyx-bulletx,2)+ math.pow(enemyy-bullety,2))
    if distance<27:
        return True
    else:
        return False
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
running=True
while running:
    # RED GREEN AND BLUE
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        # key stroke
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                player_change=-4
            if event.key==pygame.K_RIGHT:
                player_change=4
            if event.key == pygame.K_SPACE:
                if bullet_state=="ready":
                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletx=playerx
                    bullet_fire(bulletx, bullety)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT :
                player_change = 0


    playerx+=player_change
    if playerx<=0:
        playerx=0
    elif playerx>=736:
        playerx=736
        # enemy movement
    for i in range(num_enemy):
        # Game over
        if enemyy[i] > 440:
            for j in range(num_enemy):
                enemyy[j] = 2000
            game_over_text()
            break
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i]=1
            enemyy[i]+=enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i]=-1
            enemyy[i]+=enemyy_change[i]
        # collision
        collision = incollision(bulletx, bullety, enemyy[i], enemyx[i])
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bullety = 480
            bullet_stat = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i], i)
    # bullet
    if bullety<=0:
        bullety=400
        bullet_state="ready"
    if bullet_state is "fire":
        bullet_fire(bulletx, bullety)
        bullety-=bullety_change

    player(playerx, playery)
    show_score(textx, testy)
    pygame.display.update()