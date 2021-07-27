#This game was made for a 4 day camp so it lacks some complexity

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))

font = pygame.font.SysFont("Arial", 40)

#images
air_animation = []

for i in range (10):
    air_animation.append(pygame.image.load(f"Air/darkness3_{i+1}.png"))

earth_animation = []

for i in range (5):
    earth_animation.append(pygame.image.load(f"Earth/earth5_{i+2}.png"))

fire_animation = []

for i in range (4):
    fire_animation.append(pygame.image.load(f"Fire/fire1_{i+1}.png"))

walk_animation = []
for i in range(3):
    walk_animation.append(pygame.image.load(f"Player/{i}.png"))

bg = pygame.image.load("Background.png")
bg = pygame.transform.scale(bg, (800, 800))
fg = pygame.image.load("Foreground.png")
fg = pygame.transform.scale(fg, (800, 800))

#variables
game_over = False
running = True
answer = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]#decides our answer key
default = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
fire_chosen = default[0]
earth_chosen = default[1]
airChosen = default[2]
#makes sure the game doesn't end as it begins
while default == answer:
    default = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
#player variables
playerX = 0
playerY = 260
playerX_change = 0
playerIndex = 0
speed = 20
isLeft = False
#pillar variables
earthIndex = 0
fireIndex = 0
airIndex = 0
earthX = 600
earthY = 130
fireX = 350
fireY = 130
airX = 100
airY = 150
#interact key icon
interact_icon = font.render("Spacebar", True, (255, 255 ,255))
#answer locations
location1 = (random.randint(20, 200), random.randint(80, 100))
location2 = (random.randint(300, 400), random.randint(80, 100))
location3 = (random.randint(500, 700), random.randint(80, 100))
#game over
increment = 10
#functions

def display_key(x1, x2, y2):#x1 is playerX, x2 is the x for each pillar
    if abs(x2 - x1) < 50:
        screen.blit(interact_icon, (x2 - 20, y2))



def draw_screen():
    screen.blit(fg, (0, 0))
    screen.blit(bg, (0, 0))

    #player
    player_image = pygame.transform.scale(walk_animation[playerIndex], (100, 80))
    if isLeft:
        player_image = pygame.transform.flip(player_image, True, False)
    screen.blit(player_image, (playerX, playerY))
    #pillars

    if airChosen:
        air_icon = pygame.transform.scale(air_animation[airIndex], (100, 100))
        screen.blit(air_icon, (airX, airY))
    if fire_chosen:
        fire_icon = pygame.transform.scale(fire_animation[fireIndex], (100, 100))
        screen.blit(fire_icon, (fireX, fireY))
    if earth_chosen:
        earth_icon = pygame.transform.scale(earth_animation[earthIndex], (100, 100))
        screen.blit(earth_icon, (earthX, earthY))

    display_key(playerX, airX, airY)
    display_key(playerX, fireX, fireY)
    display_key(playerX, earthX, earthY)

    #display answer
    answer1 = font.render(str(answer[0]), True, (100, 100, 100))
    screen.blit(answer1, location1)
    answer2 = font.render(str(answer[1]), True, (100, 100, 100))
    screen.blit(answer2, location2)
    answer3 = font.render(str(answer[2]), True, (100, 100, 100))
    screen.blit(answer3, location3)

    if game_over:
        pygame.draw.rect(screen, [120, 60, 0], [0, 0, 800, increment], False)
        if increment > 800:
            end_message = font.render("You escaped!", True, (200, 200, 200))
            screen.blit(end_message, (300, 300))



clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 20
                isLeft = False
            if event.key == pygame.K_LEFT:
                playerX_change = -20
                isLeft = True
            if event.key == pygame.K_SPACE:
                if abs(playerX - fireX) < 50:
                    fire_chosen = not fire_chosen
                if abs(playerX - airX) < 50:
                    airChosen = not airChosen
                if abs(playerX - earthX) < 50:
                    earth_chosen = not earth_chosen


    playerX += playerX_change

    #animate player
    if playerX_change != 0:
        if playerIndex < len(walk_animation) - 1:
            playerIndex += 1
        else:
            playerIndex = 0




    #animate elements
    if airIndex < len(air_animation) - 1:
        airIndex += 1
    else:
        airIndex = 0
    if fireIndex < len(fire_animation) - 1:
        fireIndex += 1
    else:
        fireIndex = 0
    if earthIndex < len(earth_animation) - 1:
        earthIndex += 1
    else:
        earthIndex = 0

    if answer == [airChosen, fire_chosen, earth_chosen]:
        game_over = True
        if increment < 810:
            increment += 10


    draw_screen()
    pygame.display.update()
    clock.tick(20)

