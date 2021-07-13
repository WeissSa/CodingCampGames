#Full code. Students may not get this far. that's okay
#dodge the obstacles and collect fuel cans
#Aim for high score
#arrow keys to control
import pygame
import random
import math

#setup
pygame.init()
screen = pygame.display.set_mode((800,800))
font = pygame.font.SysFont("Arial", 35)

#sounds
music = pygame.mixer.music.load("Assets/JDB - Old School Run.wav")
pygame.mixer.music.play(-1)
itemSound = pygame.mixer.Sound("Assets/Coin.wav")

#images
bg = pygame.image.load("Assets/bgImage.jpg")
bg = pygame.transform.scale(bg, (800,800))
playerImage = pygame.image.load("Assets/ship.png")
playerImage = pygame.transform.scale(playerImage, (100, 150))
BH = pygame.image.load("Assets/blackhole.png")
BH = pygame.transform.scale(BH, (100, 100))
Asteroid = pygame.image.load("Assets/asteroid.png")
Asteroid.set_colorkey((255, 255, 255))
Asteroid = pygame.transform.scale(Asteroid, (100, 100))
gas = pygame.image.load("Assets/gas.png")
gas = pygame.transform.scale(gas, (100, 100))

#variables
    #game
running = True
lanes = [200, 350, 500]
laneIndex = 1
FPS = 20
cooldown = 5
score = 0
    #player
playerX = lanes[laneIndex]
playerY = 600
health = 3
    #objects
objectSpeed = 30
BHoff = True #represents if BH is offscreen
BHY = -100
BHX = random.choice(lanes)
Aoff = True #represents if Asteroid is offscreen
AY = -100
AX = random.choice(lanes)
Goff = True #represents if Gas is offscreen
GY = -100
GX = random.choice(lanes)
#functions
def draw_screen():
    #bg
    screen.fill((0,0,0))
    screen.blit(bg, (0,0))
    #player
    screen.blit(playerImage, (playerX, playerY))

    if BHY < 800:
        screen.blit(BH, (BHX, BHY))

    if AX < 800:
        screen.blit(Asteroid, (AX, AY))

    if GX < 800:
        screen.blit(gas, (GX, GY))


    #score
    score_display = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_display, (30, 20))

def isColliding(x1, x2, y1, y2):
    distance = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))
    if distance < 50:
        return True
    return False

def checkHealth(health):
    if health < 1:
        pygame.quit()

clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if laneIndex < 2:
                    laneIndex += 1
            if event.key == pygame.K_LEFT:
                if laneIndex > 0:
                    laneIndex -= 1

    playerX = lanes[laneIndex]


    #cooldown/respawn
    if cooldown == 0:
        if BHoff:
            BHY = -100
            BHX = random.choice(lanes)
            BHoff = False
        elif Goff:
            GY = -100
            GX = random.choice(lanes)
            Goff = False
        elif Aoff:
            AY = -100
            AX = random.choice(lanes)
            Aoff = False
        cooldown = random.randint(5, 10)
    else:
        cooldown -= 1

    #movement
    if BHY < 800:
        BHY += objectSpeed
    else:
        BHoff = True
    if AY < 800:
        AY += objectSpeed
    else:
        Aoff = True
    if GY < 800:
        GY += objectSpeed
    else:
        Goff = True


    #collision
    if isColliding(playerX, AX, playerY, AY):
        AY = 801
        health -= 1
        Aoff = True
        checkHealth(health)
    if isColliding(playerX, BHX, playerY, BHY):
        BHY = 801
        health -= 1
        BHoff = True
        checkHealth(health)
    if isColliding(playerX, GX, playerY, GY):
        GY = 801
        score += 10
        Goff = True

    #difficulty
    if score == 100:
        objectSpeed = 50
    elif score == 300:
        objectSpeed = 60

    draw_screen()
    pygame.display.update()
    clock.tick(FPS)