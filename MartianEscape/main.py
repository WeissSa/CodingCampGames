#This is the final game of the summer and I want to try something a bit different
#Click on the spaceships as fast as you can. Avoid clicking on the rocket ship.
#Click on enough spaceships and you escape! If you don't click fast enough the aliens land and you lose :(

import pygame
import random

pygame.init()
font = pygame.font.SysFont("Arial", 40)
screen = pygame.display.set_mode((800, 800))

#images
ship_surface = pygame.image.load("Assets/Creatures/spaceship1.png")
friend_surface = pygame.image.load("Assets/Creatures/HumanShip.png")
friend_surface = pygame.transform.rotozoom(friend_surface, -47, 0.05)

click_animation = []
for i in range(5):
    click_surface = pygame.image.load(f"Assets/Impact/impact4_{i+1}.png")
    click_animation.append(click_surface)

BG = pygame.image.load("Assets/Background/img.png")
BG = pygame.transform.scale(BG, (800, 800))

#variables
running = True
danger = 0
#player
clicks = []
clickIndexes = []

#enemy
spaceships = []
#friendly
isShowing = False

#events
NEWENEMY = pygame.USEREVENT
pygame.time.set_timer(NEWENEMY, 350)

NEWFRIEND = pygame.USEREVENT + 1
pygame.time.set_timer(NEWFRIEND, 1500)


#functions

def create_click(position):
    click_rect = click_animation[0].get_rect(center=position)
    clicks.append(click_rect)
    clickIndexes.append(0)

def draw_clicks(clicks):
    for i in range (len(clicks)):
        surface = click_animation[clickIndexes[i]]
        screen.blit(surface, clicks[i])
        #handles animation
        if clickIndexes[i] < 4:
            clickIndexes[i] += 1
        else:
            clickIndexes.pop(i)
            clicks.pop(i)

def create_enemy():
    position = (random.randint(50, 750), random.randint(50, 750))
    enemy_rect = ship_surface.get_rect(center=position)
    spaceships.append(enemy_rect)

def draw_enemies(ships):
    for ship in ships:
        screen.blit(ship_surface, ship)

def draw_screen():
    screen.blit(BG, (0,0))


    draw_enemies(spaceships)

    #friendly ship
    if isShowing:
        screen.blit(friend_surface, friendly_rect)

    #enemies must be before clicks
    draw_clicks(clicks)

    #User interface
    pygame.draw.rect(screen, [0, 0, 0], [0, 0, 150, 30], False)
    pygame.draw.rect(screen, [255, 0, 0], [0, 0, danger * 5, 30], False)

    if danger > 30:
        screen.fill((255, 0, 0))

clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            create_click(pos)

        if event.type == NEWENEMY:
            create_enemy()

        if event.type == NEWFRIEND:
            print("hi")
            if isShowing:
                isShowing = False
            else:
                pos = (random.randint(50, 750),random.randint(50, 750))
                friendly_rect = friend_surface.get_rect(center = pos)
                isShowing = True


    #collision
    for click in clicks:
        for ship in spaceships:
            if click.colliderect(ship):
                spaceships.remove(ship)
        if isShowing:
            if click.colliderect(friendly_rect):
                isShowing = False
                danger += 5

    #danger management
    new_danger = len(spaceships)
    if new_danger > danger:
        danger = new_danger
    else:
        #decay
        danger -= 0.05

    draw_screen()
    pygame.display.update()
    clock.tick(30)

pygame.quit()