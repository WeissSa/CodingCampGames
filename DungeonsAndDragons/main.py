#This is the full code. If you run out of time do the arrow shooting LAST. Priority it movement and fireballs/score
#control the character with arrow keys, spacebar, and F to shoot
#dodge fireballs to gain points. Last as long as you can and then kill the dragon to get a bunch of points at once, but your game ends
#you have to balance risk reward of killing dragon VS game over
import random
import pygame
import math

#setup
pygame.init()
screen = pygame.display.set_mode((800,800))
font = pygame.font.SysFont("Arial", 20)

#images
fire1 = pygame.image.load("Assets/Fire2_1.png")
fire2 = pygame.image.load("Assets/Fire2_2.png")
fire3 = pygame.image.load("Assets/Fire2_3.png")
fire4 = pygame.image.load("Assets/Fire2_4.png")
fire5 = pygame.image.load("Assets/Fire2_5.png")
fire6 = pygame.image.load("Assets/Fire2_6.png")
idle1 = pygame.image.load("Assets/idle1.png")
idle2 = pygame.image.load("Assets/idle2.png")
idle3 = pygame.image.load("Assets/idle3.png")
run1 = pygame.image.load("Assets/Run/adventurer-run2-00.png")
run2 = pygame.image.load("Assets/Run/adventurer-run2-01.png")
run3 = pygame.image.load("Assets/Run/adventurer-run2-02.png")
run4 = pygame.image.load("Assets/Run/adventurer-run2-03.png")
run5 = pygame.image.load("Assets/Run/adventurer-run2-04.png")
run6 = pygame.image.load("Assets/Run/adventurer-run2-05.png")
jump1 = pygame.image.load("Assets/Jump/Jump (1).png")
jump2 = pygame.image.load("Assets/Jump/Jump (2).png")
jump3 = pygame.image.load("Assets/Jump/Jump (3).png")
jump4 = pygame.image.load("Assets/Jump/Jump (4).png")
jump5 = pygame.image.load("Assets/Jump/Jump (5).png")
jump6 = pygame.image.load("Assets/Jump/Jump (6).png")
dragon = pygame.image.load("Assets/Dragon.png")
#image lists
fire_ball = [fire1, fire2, fire3, fire4, fire5, fire6]
player_idle = [idle1, idle2, idle3]
player_run = [run1, run2, run3, run4, run5, run6]
player_jump = [jump1, jump2, jump3, jump4, jump5, jump6]
player_animation = player_idle
player_animations = [player_idle, player_run, player_jump]


#variables
run = True
score = 0
FPS = 20
game_over = False
#player variables
playIndex = 0
loopSpeed = 0.8
looping = True
playerX = 100
playerX_change = 0
playerY = 580
playerHealth = 3
playerSpeed = 10
playerY_change = 0
isJump = False
isHit = False
canShoot = True
isLeft = False
isFalling = False
#Dragon variables
dragonIndex = 0
canRoar = True
dragonHealth = 3
dragonX = 700
dragonY = 600
#fireball Variables
fireIndex = 0
cooldown = 10
offscreen = True
fireSpeed = 20
fireX = 700
fireY = 570

#images
bg = pygame.image.load("Assets/bg.png")
bg = pygame.transform.scale(bg, (800, 800))
#sounds
music = pygame.mixer.music.load("Assets/BGMusic.wav")
pygame.mixer.music.play(-1)
intro = pygame.mixer.Sound("Assets/Intruder.wav")
roar = pygame.mixer.Sound("Assets/Dragon.wav")


def draw_screen():
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    score_display = font.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(score_display, (30, 20))
    player_image = pygame.transform.scale(player_animation[int(playIndex)], (100,100))
    if isLeft:
        player_image = pygame.transform.flip(player_image, True, False)
    screen.blit(player_image, (playerX, playerY))

    #dragon display
    dragon_image = pygame.transform.scale(dragon, (200, 400))
    dragon_image = pygame.transform.flip(dragon_image, True, False)
    screen.blit(dragon_image, (600, 380))

    #fireball display
    fireball_image = pygame.transform.scale(fire_ball[fireIndex], (150, 100))
    fireball_image = pygame.transform.flip(fireball_image, True, False)
    if fireX < 700:
        screen.blit(fireball_image, (fireX, fireY))

    #game over
    if game_over:
        screen.fill((0, 0, 0))
        game_over_display = font.render('GAME OVER! Your score was:  ' + str(score), True, (255, 255, 255))
        screen.blit(game_over_display, (280, 380))

#player functions
def animate_player(x,y):
    global player_animation
    global looping
    if y != 0:
        player_animation = player_animations[2]
        looping = False
    elif x != 0:
        player_animation = player_animations[1]
        looping = True
    else:
        player_animation = player_animations[0]
        looping = True

def jump(y, ychange):
    global isFalling
    if y < 300:
        isFalling = True

#dragon functions


#collision
def is_colliding(x1, x2, y1, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distance < 50:
        return True
    else:
        return False

clock = pygame.time.Clock()
intro.play()
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                isLeft = True
                if playerX > 10:
                    playerX_change = -playerSpeed

            if event.key == pygame.K_RIGHT:
                isLeft = False
                if playerX < 650:
                    playerX_change = playerSpeed
            if isJump == False:
                if event.key == pygame.K_SPACE:
                    playerY_change = 50
                    isJump = True

    #moves player and checks for edges
    playerX += playerX_change
    if playerX >= 580:
        playerX = 580
    elif playerX <= 10:
        playerX = 10

    #jump processing
    if isJump:
        jump(playerY, playerY_change)

        if isFalling:
            playerY += playerY_change
        else:
            playerY -= playerY_change

        if playerY > 600:
            playerY = 600
            isFalling = False
            isJump = False
            playerY_change = 0

    #player animation
    animate_player(playerX_change, playerY_change)
    if canShoot:
        if not isHit:
            if playIndex < len(player_idle)-1:
                playIndex += loopSpeed
            else:
                if looping:
                    playIndex = 0

    #dragon section

    #fireball
    if cooldown == 0 and offscreen:
        cooldown = random.randint(10, 40)
        fireX = 700
        offscreen = False
        canRoar = True
    elif cooldown == 0:
        if canRoar:
            roar.play()
            canRoar = False
        fireX -= fireSpeed
        if fireIndex < len(fire_ball)-1:
            fireIndex += 1
        else:
            fireIndex = 0
    else:
        cooldown -= 1
    if fireX < 0:
        offscreen = True
        score += 10

    if is_colliding(playerX,fireX ,playerY , fireY):
        playerHealth -= 1
        cooldown = random.randint(10, 40)
        fireX = 700
        offscreen = False
        canRoar = True
        if playerHealth == 0:
            game_over = True
            canRoar = False

    #OPTIONAL: DIFFICULTY
    if score > 100:
        fireSpeed = 30
    elif score > 300:
        fireSpeed += 40
    draw_screen()
    pygame.display.update()
    clock.tick(FPS)
