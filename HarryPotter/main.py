#control the wizard with arrow keys
#cast fire spell with z and wind with x
#try to reach high score
#if you run out of health press space to restart

#priority of code: get 1 enemy and spell working
#for faster/advanced students: get 2
#for most advanced: add more spell types (get creative!)

import pygame
import random

pygame.init()
font = pygame.font.SysFont("Arial", 40)
screen = pygame.display.set_mode((800, 800))

#sounds
bgmusic = pygame.mixer.music.load("Sounds/BGMusic.wav")
pygame.mixer.music.play(-1)
dying = pygame.mixer.Sound("Sounds/Dead.wav")
damaged = pygame.mixer.Sound("Sounds/HIt.wav")
shoot = pygame.mixer.Sound("Sounds/Shoot.wav")

#images

BG = pygame.transform.scale(pygame.image.load("Assets/background.png"), (800, 800))
FG = pygame.transform.scale(pygame.image.load("Assets/foreground.png"), (800, 800))

walk_anim = []
for i in range (4):
    walk_anim.append(pygame.image.load(f"Assets/run/run_{i+1}.png"))

idle = pygame.image.load("Assets/Idle/idle_1.png")

dead_anim = []
for i in range (4):
    dead_anim.append(pygame.image.load(f"Assets/dead/dead_{i+1}.png"))

firespell = []
for i in range(6):
    firespell.append(pygame.image.load(f"Assets/Fire/fire2_{i+1}.png"))
fireIndex = 0

windSpell = []
for i in range(9):
    windSpell.append(pygame.image.load(f"Assets/wind/darkness2_{i+1}.png"))
windIndex = 0

fireEnemySurface = pygame.image.load("Assets/Enemies/fire.png")
iceEnemySurface = pygame.image.load("Assets/Enemies/ice.png")

enemies = ["fire", "ice"]

#variables
running = True
score = 0
highscore = 0
INCREASESCORE = pygame.USEREVENT
pygame.time.set_timer(INCREASESCORE, 2000)
#player variables
playerX_change = 0
playerX = 100
playerY = 650
health = 3
playerIndex = 0
canCast = True
dead = False
#attack variables
type = "null"
onscreen = False
spellX = playerX
spellY = playerY
#enemy variables
current_enemy = "" #represents which enemy will spawn (will be used for decision making)
enemy_surface = "null"
canSpawn = True
enemySpeed = 10


#functions

def state(X_change, health):
    if health < 1:
        return "dead"
    elif X_change != 0:
        return "run"
    else:
        return "idle"



def draw_screen():
    #while the globals make it messy, I want students to organize their code. In an ideal world students would make the
    #player, enemy, and spells into classes (possible enrichment for advanced students)
    global health
    global canSpawn
    global onscreen
    screen.blit(FG, (0,0))
    screen.blit(BG, (0,0))

    current_state = state(playerX_change, health)
    if current_state == "dead":
        player_image = dead_anim[int(playerIndex)]
    elif current_state == "run":
        player_image = walk_anim[int(playerIndex)]
    else:
        player_image = idle
    player_image = pygame.transform.scale(player_image, (100, 100))
    player_rect = player_image.get_rect(midbottom=(playerX, playerY))


    screen.blit(player_image, player_rect)

    if not dead:
        screen.blit(enemy_surface, enemy_rect)

        #health
        pygame.draw.rect(screen, [200, 50, 50], [580, 20, 200/3 * health, 50], False)


    #collision
    if player_rect.colliderect(enemy_rect):
        health -= 1
        canSpawn = True
        if health > 0:
            damaged.play()

    #spell
    if onscreen:
        if type == "fire":
            spell_surface = firespell[fireIndex]
        if type == "wind":
            spell_surface = windSpell[windIndex]
        spell_surface = pygame.transform.scale2x(spell_surface)
        spell_rect = spell_surface.get_rect(bottomleft = (spellX, spellY))
        screen.blit(spell_surface, spell_rect)

        #I am putting collision in here so it doesn't have to check it as often (collision slows down code)

        if spell_rect.colliderect(enemy_rect):
            if type == "fire" and current_enemy == "ice":
                canSpawn = True
                onscreen = False
            elif type == "wind" and current_enemy == "fire":
                canSpawn = True
                onscreen = False


    #score and highscore
    scoredisplay = font.render(str(score), True, (255, 255, 255))
    score_rect = scoredisplay.get_rect(center=(400, 50))
    screen.blit(scoredisplay, score_rect)

    if dead:
        highscore_display = font.render("Highscore: " + str(highscore), True, (255, 255, 255))
        highscore_rect = highscore_display.get_rect(center=(400, 700))
        screen.blit(highscore_display, highscore_rect)


clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not dead:
                if event.key == pygame.K_RIGHT:
                    playerX_change = 10
                if event.key == pygame.K_LEFT:
                    playerX_change = -10

                #casting code (z = fire, x = wind). Onscreen determines whether the player can cast
                if not onscreen:
                    if event.key == pygame.K_z:
                        shoot.play()
                        type = "fire"
                        onscreen = True
                        fireIndex = 0
                        spellX = playerX
                    if event.key == pygame.K_x:
                        shoot.play()
                        type = "wind"
                        windIndex = 0
                        onscreen = True
                        spellX = playerX

            #reset game
            if dead:
                if event.key == pygame.K_SPACE:
                    enemySpeed = 10
                    health = 3
                    canSpawn = True
                    playerY = 650
                    playerX = 100
                    dead = False
                    score = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        if event.type == INCREASESCORE and not dead:
            score += 10

    playerX += playerX_change
    #spells
    if onscreen:
        spellX += 20
    if spellX > 800:
        onscreen = False

    if type == "fire":
        if fireIndex < len(firespell) - 1:
            fireIndex += 1
        else:
            fireIndex = 0
    elif type == "wind":
        if windIndex < len(windSpell) - 1:
            windIndex += 1
        else:
            windIndex = 0


    #enemy
    if canSpawn and not dead:
        current_enemy = random.choice(enemies)
        if current_enemy == "fire":
            enemy_surface = fireEnemySurface
        elif current_enemy == "ice":
            enemy_surface = iceEnemySurface
        enemy_surface = pygame.transform.flip(enemy_surface, True, False)
        enemy_surface = pygame.transform.scale2x(enemy_surface)
        enemy_rect = enemy_surface.get_rect(midleft=(800, 600))
        canSpawn = False
    if enemy_rect.right > 0:
        enemy_rect.centerx -= enemySpeed
    else:
        canSpawn = True

    if health < 1 and not dead:
        dead = True
        playerIndex = 0
        dying.play()
    #animation:
    if playerIndex < 3:
        playerIndex += 0.5
    elif state(playerX_change, health) != "dead":#makes the dead animation not loop
        playerIndex = 0
    draw_screen()

    #difficulty
    if score == 100:
        enemySpeed = 20
    elif score == 150:
        enemySpeed = 30

    if score > highscore:
        highscore = score

    pygame.display.update()
    clock.tick(20)