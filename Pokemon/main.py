import math
import random
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))
font = pygame.font.SysFont("Arial", 40)

#music and sounds
BGMusic = pygame.mixer.music.load("Assets/BGMusic.mp3")
pygame.mixer.music.play(-1)#pics

collect = pygame.mixer.Sound("Assets/Collect.wav")

BG = pygame.image.load("Assets/BG.jpg")
BG = pygame.transform.scale(BG, (800, 800))
#we create 2 background to give a scrolling effect
pika0 = pygame.image.load("Assets/0.png")
pika1 = pygame.image.load("Assets/1.png")
pika2 = pygame.image.load("Assets/2.png")
pika3 = pygame.image.load("Assets/3.png")
pika4 = pygame.image.load("Assets/4.png")
pika5 = pygame.image.load("Assets/5.png")
run = [pika0, pika1, pika2, pika3, pika4, pika5]

pokeball = pygame.image.load("Assets/pokeball.png")

#list of all pokemon that can spawn
#automation of this shouldnt be hard. Just do:
pokemonList = []
numPokemonPics = 15#number of pokemon sprites in folder
for i in range(numPokemonPics):
    pokemonList.append(pygame.image.load("Assets/Pokemon/" + str(i) + ".png"))
#alternatively you could do this manually

#variables
running = True

#player variables
runIndex = 0
playerX = 100
playerY = 600
playerY_change = 0
playerX_change = 0
jumpSpeed = 40
speed = 32
isJump = False
isFall = False
health = 5
#background variables
BGX = 0
BG2X = 800
scrollspeed = 10

#PokemonVariables
pokeX1 = 1200
pokeX2 = 600
pokeimage1 = pygame.transform.scale(random.choice(pokemonList), (100, 100))
pokeimage2 = pygame.transform.scale(random.choice(pokemonList), (100, 100))

#pokeball variables
score = 0
pokeballX = 1000
pokeballY = random.randint(300, 600)

def display_screen():
    #background

    screen.blit(BG, (BGX, 0))
    screen.blit(BG, (BG2X, 0))
    #player
    player_sprite = pygame.transform.scale(run[runIndex], (75, 50))
    player_sprite = pygame.transform.flip(player_sprite, True, False)
    screen.blit(player_sprite, (playerX, playerY))

    #enemies
    screen.blit(pokeimage1, (pokeX1, 550))
    screen.blit(pokeimage2, (pokeX2, 550))
    #pokeball
    pokeball_item = pygame.transform.scale(pokeball, (50, 50))
    screen.blit(pokeball_item, (pokeballX, pokeballY))
    #UI
    score_display = font.render(str(score), True, (0,0,0))
    screen.blit(score_display, (5,0))
    pokeball_icon = pygame.transform.scale(pokeball, (50, 50))
    screen.blit(pokeball_icon, (50,0))

    #healthbar
    pygame.draw.rect(screen, [120, 120, 120], [590, 0, 210, 70], False)#creates grey rectangle
    pygame.draw.rect(screen, [100, 200, 20], [600, 50, 200 / 5 * health, 10], False)#creates green rectangle and auto
    #resizes based off health
    health_display = font.render("Health:", True, (0,0,0))
    screen.blit(health_display, (650, 10))
    if health < 1:
        screen.blit(BG, (0,0))
        final_display = font.render("Final Score: " + str(score), True, (0,0,0))
        screen.blit(final_display, (280, 350))



def isCol (x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))
    if distance < 80:
        return True
    else:
        return False

clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not isJump:
                    isJump = True
            if event.key == pygame.K_RIGHT:
                playerX_change = speed
            if event.key == pygame.K_LEFT:
                playerX_change = -speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 700:
        playerX = 700

    #animation:
    if runIndex < len(run) - 1:
        runIndex += 1
    else:
        runIndex = 0

    if isJump:
        if playerY < 300:
            isFall = True
        if isFall:
            playerY_change = jumpSpeed
        else:
            playerY_change = - jumpSpeed
    else:
        playerY_change = 0
    playerY += playerY_change
    if playerY > 600:
        playerY = 600
        isJump = False
        isFall = False

    #background code
    BGX -= scrollspeed
    BG2X = BGX + 800
    if BGX < -800:
        BGX = 0

    #enemy code
    pokeX1 -= scrollspeed
    pokeX2 -= scrollspeed
    if pokeX1 < -200:
        pokeX1 = random.randint(800, 1000)
        pokeimage1 = pygame.transform.scale(random.choice(pokemonList), (100, 100))
    elif pokeX2 < -200:
        pokeX2 = random.randint(800, 1000)
        pokeimage2 = pygame.transform.scale(random.choice(pokemonList), (100, 100))

    #enemy collision

    if isCol(pokeX1, 550, playerX, playerY):
        pokeX1 = random.randint(800, 1200)
        pokeimage1 = pygame.transform.scale(random.choice(pokemonList), (100, 100))
        health -= 1
    elif isCol(pokeX2, 550, playerX, playerY):
        pokeX2 = random.randint(800, 1200)
        pokeimage2 = pygame.transform.scale(random.choice(pokemonList), (100, 100))
        health -= 1

    if abs(pokeX1 - pokeX2) < 200:
        if pokeX1 < pokeX2:
            pokeX2 += 200
        else:
            pokeX1 += 200


    #pokeball code
    if health > 1:
        pokeballX -= scrollspeed
        if pokeballX < -200:
            pokeballX = random.randint(800, 1000)
            pokeballY = random.randint(300, 600)

        if isCol(pokeballX, pokeballY, playerX, playerY):
            pokeballX = random.randint(800, 1000)
            pokeballY = random.randint(300, 600)
            collect.play()
            score += 1

    #pokeball collision

    #difficulty
    if score == 5:
        scrollspeed = 15
    elif score == 15:
        scrollspeed = 20

    display_screen()
    pygame.display.update()
    clock.tick(20)