import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))
font = pygame.font.SysFont("Arial", 40)

#loading images
bg_surface = pygame.image.load("assets/BG.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (800, 800))

floor_surface = pygame.image.load("assets/ground.png").convert()

spaceship_surface = pygame.image.load("assets/Spaceship.png").convert()
spaceship_surface = pygame.transform.scale(spaceship_surface, (50, 50))
spaceship_surface.set_colorkey((0,0,0))
spaceship_rect = spaceship_surface.get_rect(center=(100, 400))

blackhole_surface = pygame.image.load("assets/blackhole.png").convert()
blackhole_surface = pygame.transform.scale(blackhole_surface, (100, 500))

explosion_animation = []
for i in range (7):
    sprite = pygame.image.load(f"assets/End/{i}.png").convert()
    sprite.set_colorkey((0,0,0))
    explosion_animation.append(pygame.transform.scale(sprite, (50,50)))

#game variables
floorX = 0
running = True
scrollspeed = 12
game_over = False
score = 0
high_score = 0
#player variables
gravity = 1
spaceship_movement = 0
playerIndex = 0
#pipe variables
blackhole_list = []
SPAWNBLACKHOLE = pygame.USEREVENT
pygame.time.set_timer(SPAWNBLACKHOLE, 1200)
blackhole_height = [300, 400, 500, 600]

def create_blackhole():
    random_height = random.choice(blackhole_height)
    bottom_blackhole = blackhole_surface.get_rect(midtop=(900, random_height))
    top_blackhole = blackhole_surface.get_rect(midbottom=(900, random_height -200))
    return bottom_blackhole, top_blackhole

def move_blackholes(blackholes):
    for blackhole in blackholes:
        blackhole.centerx -= scrollspeed
    return blackholes

def rotate_spaceship(ship):
    new_ship = pygame.transform.rotozoom(ship, spaceship_movement * -2, 1)
    new_ship.set_colorkey((0,0,0))
    return new_ship

def draw_screen(blackholes, game_over):
    screen.blit(bg_surface, (0,0))

    #important to have blackholes before floor
    if not game_over:
        for blackhole in blackholes:
            screen.blit(blackhole_surface, blackhole)

    screen.blit(floor_surface, (floorX,0))
    screen.blit(floor_surface, (floorX + 800, 0))


    if game_over and playerIndex < len(explosion_animation):
        screen.blit(explosion_animation[playerIndex], spaceship_rect)
    elif not game_over:
        rotated_ship = rotate_spaceship(spaceship_surface)
        screen.blit(rotated_ship, spaceship_rect)

    #score
    if game_over == True:

        score_surface = font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(400, 50))
        screen.blit(score_surface, score_rect)


        highscore_text = font.render("Highscore:", True, (255, 255, 255))
        highscore_rect = highscore_text.get_rect(center=(400, 650))
        screen.blit(highscore_text, highscore_rect)

        highscore_surface = font.render(str(int(high_score)), True, (255, 255, 255))
        highscore_rect = highscore_surface.get_rect(center=(400, 700))
        screen.blit(highscore_surface, highscore_rect)
    else:
        score_surface = font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(400, 50))
        screen.blit(score_surface, score_rect)

def check_col(blackholes):
    for blackhole in blackholes:
        if spaceship_rect.colliderect(blackhole):
            return True
    if spaceship_rect.top <= -40 or spaceship_rect.bottom >= 730:
        return True
    else:
        return False


clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over == False:
                spaceship_movement = -12
            if event.key == pygame.K_SPACE and game_over == True:
                blackhole_list.clear()
                spaceship_rect.centery = 400
                spaceship_movement = 0
                playerIndex = 0
                score = 0
                game_over = False
        if event.type == SPAWNBLACKHOLE:
            blackhole_list.extend(create_blackhole())

    # floor code
    floorX -= scrollspeed
    if floorX < -800:
        floorX = 0

    if game_over == False:
        #movement
        spaceship_movement += gravity
        spaceship_rect.centery += spaceship_movement

        #pipes
        blackhole_list = move_blackholes(blackhole_list)

        game_over = check_col(blackhole_list)
        score += 0.023
    else:
        if score > high_score:
            high_score = score


    if game_over and playerIndex < len(explosion_animation)-1:
        playerIndex += 1
    elif game_over:
        playerIndex = 7

    draw_screen(blackhole_list, game_over)
    clock.tick(30)
    pygame.display.update()