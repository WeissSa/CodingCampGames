#This is the final game of the summer and I want to try something a bit different
#Click on the spaceships as fast as you can. Avoid clicking on the rocket ship.
#Click on enough spaceships and you escape! If you don't click fast enough the aliens land and you lose :(

import pygame
import random

pygame.init()
font = pygame.font.SysFont("Arial", 40)
screen = pygame.display.set_mode((800, 800))

#music and sounds
pygame.mixer.music.load("Assets/Sounds/JDB - Ashen Queen.wav")
pygame.mixer.music.play(-1)
bad_hit = pygame.mixer.Sound("Assets/Sounds/Beep.wav")
good_hit = pygame.mixer.Sound("Assets/Sounds/Coin.wav")
end_sound = pygame.mixer.Sound("Assets/Sounds/Dead.wav")


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

alien_surface = pygame.image.load("Assets/Creatures/alien1.png")
alien_surface = pygame.transform.scale(alien_surface, (300, 300))

explosion = []
for i in range(8):
    explosion_surface = pygame.image.load(f"Assets/Explosion/explosion2_{i + 1}.png")
    explosion.append(pygame.transform.scale(explosion_surface, (800, 800)))

#variables
running = True
danger = 0
game_over = False
game_lost = False
score = 0
highscore = 0
#player
clicks = []
clickIndexes = []

#enemy
spaceships = []
laserX = 200
laser_length = 50
exploding = False
explodeIndex = 0
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
    if click_rect not in clicks:
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

    if not game_over:
        draw_enemies(spaceships)

        #friendly ship
        if isShowing:
            screen.blit(friend_surface, friendly_rect)

        #enemies must be before clicks
        draw_clicks(clicks)

        #User interface
        pygame.draw.rect(screen, [0, 0, 0], [0, 0, 150, 30], False)
        pygame.draw.rect(screen, [255, 0, 0], [0, 0, danger * 5, 30], False)

        score_display = font.render("Score: " + str(score), True, (0, 0, 0))
        score_rect = score_display.get_rect(topright=(800, 0))
        screen.blit(score_display, score_rect)

    if game_over:
        pygame.draw.rect(screen, [150, 0, 0], [laserX, 300, laser_length, 20], False)

        alien_rect = alien_surface.get_rect(center = (150, 300))
        screen.blit(alien_surface, alien_rect)

        if exploding:
            explosion_surface = explosion[int(explodeIndex)]

            explode_rect = explosion_surface.get_rect(center=(400, 400))

            screen.blit(explosion_surface, explode_rect)

        if game_lost:
            screen.fill((0,0,0))
            end_display = font.render("Game over! Press space to restart.", True, (255, 255, 255))
            end_rect = end_display.get_rect(center = (400, 400))
            screen.blit(end_display, end_rect)

            highscore_display = font.render("Highscore: " + str(highscore), True, (255, 255, 255))
            highscore_rect = highscore_display.get_rect(center = (400, 600))
            screen.blit(highscore_display, highscore_rect)

            score_display = font.render("Score: " + str(score), True, (255, 255, 255))
            score_rect = score_display.get_rect(center = (400, 200))
            screen.blit(score_display, score_rect)



clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP and not game_over:
            pos = pygame.mouse.get_pos()
            create_click(pos)

        if event.type == NEWENEMY:
            create_enemy()

        if event.type == NEWFRIEND:
            if isShowing:
                isShowing = False
            else:
                pos = (random.randint(50, 750),random.randint(50, 750))
                friendly_rect = friend_surface.get_rect(center = pos)
                isShowing = True

        if event.type == pygame.KEYDOWN and game_lost:
            #resets game
            exploding = False
            explodeIndex = 0
            laserX = 200
            score = 0
            danger = 0
            game_over = False
            game_lost = False
            spaceships.clear()
            clicks.clear()
            clickIndexes.clear()
            isShowing = False
            #resets music
            pygame.mixer.music.stop()
            pygame.mixer.music.play(-1)



    #collision
    for click in clicks:
        for ship in spaceships:
            if click.colliderect(ship):
                spaceships.remove(ship)
                score += 1
                good_hit.play()
        if isShowing:
            if click.colliderect(friendly_rect):
                bad_hit.play()
                isShowing = False
                score -= 5

    #danger management
    new_danger = len(spaceships)
    if new_danger > danger:
        danger = new_danger
    else:
        #decay
        danger -= 0.05



    draw_screen()

    #This check is after draw screen so that the black flash occurs
    if danger > 30:
        if game_over == False:
            screen.fill((0,0,0))
            if highscore < score:
                highscore = score
        else:
            laserX += 20
        game_over = True

    if laserX > 800:
        if exploding == False:
            end_sound.play()
        exploding = True
        if explodeIndex < len(explosion) - 0.25:
            explodeIndex += 0.25
        else:
            game_lost = True


    pygame.display.update()
    clock.tick(30)

pygame.quit()