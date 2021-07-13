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


#classes
class fallingObject:
    x = 0
    y = 900
    offscreen = True
    speed = 30
    damaging = True

    def __init__(self, damaging):
        self.x = random.choice(lanes)
        self.y = 900
        self.offscreen = True
        self.damaging = damaging

    def spawn(self):
        self.x = random.choice(lanes)
        self.y = -100
        self.offscreen = False

    def isCol(self, x, y):
        distance = math.sqrt(math.pow(self.x - x, 2) + math.pow(self.y - y, 2))
        if distance < 50:
            self.y = 801
            self.offscreen = True
            return True
        return False

    def checkOff(self):
        if self.y < 800:
            self.y += fallingObject.speed
        else:
            self.offscreen = True



#sounds
music = pygame.mixer.music.load("Assets/JDB - Old School Run.wav")
pygame.mixer.music.play(-1)
itemSound = pygame.mixer.Sound("Assets/Coin.wav")

#images
bg = pygame.image.load("Assets/bgImage.jpg")
bg = pygame.transform.scale(bg, (800,800))
playerImage = pygame.image.load("Assets/ship.png")
playerImage = pygame.transform.scale(playerImage, (100, 150))
Blackhole = pygame.image.load("Assets/blackhole.png")
Blackhole = pygame.transform.scale(Blackhole, (100, 100))
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
BH = fallingObject(True)#blackhole
A = fallingObject(True)#Asteroid
G = fallingObject(False)#gas

#functions
def draw_screen():
    #bg
    screen.fill((0,0,0))
    screen.blit(bg, (0,0))
    #player
    screen.blit(playerImage, (playerX, playerY))

    if BH.y < 800:
        screen.blit(Blackhole, (BH.x, BH.y))

    if A.x < 800:
        screen.blit(Asteroid, (A.x, A.y))

    if G.x < 800:
        screen.blit(gas, (G.x, G.y))


    #score
    pygame.draw.rect(screen, [255, 255, 255], [25, 15, 150, 50], False)
    score_display = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_display, (30, 20))

    #Health
    pygame.draw.rect(screen, [100, 20, 20], [600, 15, 200/3 * health, 50], False)#Displays a rectangle that updates
    #with the health.
    score_display = font.render("Health", True, (0, 0, 0))
    screen.blit(score_display, (650, 20))


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
        if BH.offscreen:
            BH.spawn()
        elif G.offscreen:
            G.spawn()
        elif A.offscreen:
            A.spawn()
        cooldown = random.randint(5, 10)
    else:
        cooldown -= 1

    #movement
    A.checkOff()
    BH.checkOff()
    G.checkOff()


    #collision
    if health > 0:
        if A.isCol(playerX, playerY) or BH.isCol(playerX, playerY):
            health -= 1
        elif G.isCol(playerX, playerY):
            score += 10

    checkHealth(health)

    #difficulty
    if score == 100:
        fallingObject.speed = 50
    elif score == 300:
        fallingObject.speed = 60
    if not game_over:
        draw_screen()
    pygame.display.update()
    clock.tick(FPS)