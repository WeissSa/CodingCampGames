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
explo1 = pygame.image.load("Assets/explosion/explosion2_1.png")
explo2 = pygame.image.load("Assets/explosion/explosion2_2.png")
explo3 = pygame.image.load("Assets/explosion/explosion2_3.png")
explo4 = pygame.image.load("Assets/explosion/explosion2_4.png")
explo5 = pygame.image.load("Assets/explosion/explosion2_5.png")
explo6 = pygame.image.load("Assets/explosion/explosion2_6.png")
explo7 = pygame.image.load("Assets/explosion/explosion2_7.png")
explo8 = pygame.image.load("Assets/explosion/explosion2_8.png")

explosion = [explo1, explo2, explo3, explo4, explo5, explo6, explo7, explo8]

#variables
    #game
running = True
lanes = [200, 350, 500]
laneIndex = 1
FPS = 20
cooldown = 5
score = 0
game_over = False
    #player
playerX = lanes[laneIndex]
playerY = 600
health = 3
explosionFrame = 0
    #objects
objectSpeed = 30
BHoff = True #represents if BH is offscreen
BHY = 900
BHX = random.choice(lanes)
Aoff = True #represents if Asteroid is offscreen
AY = 900
AX = random.choice(lanes)
Goff = True #represents if Gas is offscreen
GY = 900
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
    pygame.draw.rect(screen, [255, 255, 255], [25, 15, 150, 50], False)
    score_display = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_display, (30, 20))

    #Health
    pygame.draw.rect(screen, [100, 20, 20], [600, 15, 200/3 * health, 50], False)#Displays a rectangle that updates
    #with the health.
    score_display = font.render("Health", True, (0, 0, 0))
    screen.blit(score_display, (650, 20))

def isColliding(x1, x2, y1, y2):
    distance = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))
    if distance < 50:
        return True
    return False

def checkHealth(health):
    #global variables make it messy, but I want to use more functions and I dont think it makes sense to introduce
    #classes
    global game_over
    global explosionFrame
    if health < 1:
        game_over = True
        if explosionFrame < 8:#handles one time explosion
            explode = pygame.transform.scale(explosion[int(explosionFrame)], (1200, 1200))
            screen.blit(explode, (-200, -200))
            explosionFrame += 0.5
        else:#handles end screen
            screen.fill((65, 90, 180))
            end_display1 = font.render("Game over!", True, (0, 0, 0))
            end_display2 = font.render("Your score was: " + str(score), True, (0, 0, 0))
            screen.blit(end_display1, (300, 320))
            screen.blit(end_display2, (270, 380))

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
    #could simplify with classes/functions, but classes feel like a bad idea to introduce
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
    if health > 0:
        if isColliding(playerX, AX, playerY, AY):
            AY = 801
            health -= 1
            Aoff = True
        if isColliding(playerX, BHX, playerY, BHY):
            BHY = 801
            health -= 1
            BHoff = True
        if isColliding(playerX, GX, playerY, GY):
            GY = 801
            score += 10
            Goff = True
            itemSound.play()

    checkHealth(health)

    #difficulty
    if score == 100:
        objectSpeed = 50
    elif score == 300:
        objectSpeed = 60
    if not game_over:
        draw_screen()
    pygame.display.update()
    clock.tick(FPS)