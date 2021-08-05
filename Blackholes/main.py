#This game was made with the intention of a full day camp. if it is used for a half day camp, just teach the flappy bird
#portion of the code.

#controls: spacebar and arrow keys (but only during the lunar lander section)
#reccomended modifications: add collectables to flappy bird section, add enemies to lunar lander, or add a fuel gauge

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))
font = pygame.font.SysFont("Arial", 40)

#music
bgMusic = pygame.mixer.music.load("assets/music/JDB - Innocence.wav")
pygame.mixer.music.play(-1)
change_level = pygame.mixer.Sound("assets/music/change.wav")
gem_sound = pygame.mixer.Sound("assets/music/Coin.wav")
destroyed = pygame.mixer.Sound("assets/music/HIt.wav")


#loading images
bg_surface = pygame.image.load("assets/BG.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (800, 800))

bg_surface2 = pygame.image.load("assets/BG2.jpg").convert()
bg_surface2 = pygame.transform.scale(bg_surface2, (800, 800))

floor_surface = pygame.image.load("assets/ground.png").convert()

spaceship_surface = pygame.image.load("assets/Spaceship.png").convert()
spaceship_surface = pygame.transform.scale(spaceship_surface, (50, 50))
spaceship_surface.set_colorkey((0,0,0))
spaceship_rect = spaceship_surface.get_rect(center=(100, 400))

landing_ship = pygame.transform.rotozoom(spaceship_surface, 90, 1)
landing_ship.set_colorkey((0,0,0))

blackhole_surface = pygame.image.load("assets/blackhole.png").convert()
blackhole_surface = pygame.transform.scale(blackhole_surface, (100, 500))

explosion_animation = []
for i in range (7):
    sprite = pygame.image.load(f"assets/End/{i}.png").convert()
    sprite.set_colorkey((0,0,0))
    explosion_animation.append(pygame.transform.scale(sprite, (50,50)))

gem_animation = []
for i in range(4):
    sprite = pygame.image.load(f"assets/Gem/diamond1_{i+1}.png").convert()
    gem_animation.append(sprite)

gem_rect = gem_animation[0].get_rect(center = (random.randint(50, 750), random.randint(50, 500)))

#game variables
floorX = 0
running = True
cooldown = 10
scrollspeed = 12
game_over = False
score = 0
state = "flappy"
high_score = 0
game_won = False
#player variables
gravity = 1
spaceship_movement = 0
playerIndex = 0
booster = 0
horizontal_change = 0
horizontal_movement = 0
#pipe variables
blackhole_list = []
SPAWNBLACKHOLE = pygame.USEREVENT
pygame.time.set_timer(SPAWNBLACKHOLE, 1200)
blackhole_height = [300, 400, 500, 600]

#collectable variables

gemIndex = 0

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
    #handles what needs to be drawn for flappy bird style
    if state == "flappy":
        screen.blit(bg_surface, (0,0))

        #important to have blackholes before floor
        if not game_over:
            for blackhole in blackholes:
                screen.blit(blackhole_surface, blackhole)

        screen.blit(floor_surface, (floorX,0))
        screen.blit(floor_surface, (floorX + 800, 0))
        if not game_over:
            rotated_ship = rotate_spaceship(spaceship_surface)
            screen.blit(rotated_ship, spaceship_rect)
    #handles what needs to be drawn for lander
    elif state == "lander":
        screen.blit(bg_surface2, (0,0))

        gem_sprite = pygame.transform.scale(gem_animation[gemIndex], (100, 150))
        screen.blit(gem_sprite, gem_rect)

        spaceship_image = pygame.transform.rotozoom(landing_ship, horizontal_movement * -2, 1)
        spaceship_image.set_colorkey((0,0,0))
        if not game_over or game_won:
            screen.blit(spaceship_image, spaceship_rect)

        pygame.draw.rect(screen, [0,0,0], [0, 620, 800, 5], False)

    #aniamtes explosion if you lose
    if game_over and playerIndex < len(explosion_animation) and not game_won:
        screen.blit(explosion_animation[playerIndex], spaceship_rect)


    #score
    if game_over == True:

        #draws score, highscore and the words highscore

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
        #draws score
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
            if event.key == pygame.K_SPACE and state == "flappy":
                spaceship_movement = -12
            elif event.key == pygame.K_SPACE and state == "lander":
                booster = -4

            if event.key == pygame.K_LEFT:
                horizontal_change = - 1
            if event.key == pygame.K_RIGHT:
                horizontal_change = 1


            if event.key == pygame.K_SPACE and game_over == True:
                #resets game if cooldown has passed
                if cooldown == 0:
                    #these are all the important variables to reset (I think)
                    cooldown = 10
                    blackhole_list.clear()
                    spaceship_rect.center = (100, 400)
                    spaceship_movement = 0
                    playerIndex = 0
                    score = 0
                    state = "flappy"
                    boost = 0
                    game_over = False
                    game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and state == "lander":
                booster = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                horizontal_change = 0
        if event.type == SPAWNBLACKHOLE:
            blackhole_list.extend(create_blackhole())


    if state == "flappy":
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
            if game_over:
                destroyed.play()
            score += 0.023
    elif state == "lander":
        if not game_over:

            #booster is necessary to give it lunar lander feel
            spaceship_movement += gravity
            spaceship_movement += booster

            #caps movement and stops a bug
            if spaceship_movement > 20:
                spaceship_movement = 20
            elif spaceship_movement < -20:
                spaceship_movement = -20

            horizontal_movement += horizontal_change

            spaceship_rect.centery += spaceship_movement
            spaceship_rect.centerx += horizontal_movement

            #gem logic
            if gemIndex < len(gem_animation) - 1:
                gemIndex += 1
            else:
                gemIndex = 0

            if gem_rect.colliderect(spaceship_rect):
                gem_rect.center = center = (random.randint(50, 750), random.randint(50, 500))
                score += 1
                gem_sound.play()

            #checks for win/loss
            if spaceship_rect.bottom > 620:
                if spaceship_movement < 10:
                    score += abs(30/spaceship_movement)
                    game_won = True
                else:
                    destroyed.play()
                    score -= 1 * spaceship_movement
                game_over = True




    #animates and handles cooldown (so player doesn't get confused by immediately starting a new game).
    if game_over and playerIndex < len(explosion_animation)-1:
        playerIndex += 1
        if score > high_score:
            high_score = score
    elif game_over:
        playerIndex = 7
        if cooldown != 0:
            cooldown -= 1

    #state check
    if score > 12:
        if state != "lander":
            change_level.play()
            spaceship_rect.center = (400, 200)
        state = "lander"

    draw_screen(blackhole_list, game_over)
    clock.tick(30)
    pygame.display.update()