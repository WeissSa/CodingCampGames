#This is the full code. If you run out of time do the arrow shooting LAST. Priority it movement and fireballs/score
#control the character with arrow keys, spacebar, and F to shoot
#dodge fireballs to gain points. Last as long as you can and then kill the dragon to get a bunch of points at once, but your game ends
#you have to balance risk reward of killing dragon VS game over
#Copy this code into your template for the full project to run
import random
import pygame
import math

#setup
pygame.init()
screen = pygame.display.set_mode((800,800))
font = pygame.font.SysFont("Arial", 35)


#sounds
music = pygame.mixer.music.load("Assets/BGMusic.wav")
pygame.mixer.music.play(-1)#SIGNIFICANT
intro = pygame.mixer.Sound("Assets/Intruder.wav")
roar = pygame.mixer.Sound("Assets/Dragon.wav")
bow_sound = pygame.mixer.Sound("Assets/BowAnimation/Bow.wav")
#images
bg = pygame.image.load("Assets/bg.png")
bg = pygame.transform.scale(bg, (800, 800))
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
bow1 = pygame.image.load("Assets/BowAnimation/bow (1).png")
bow2 = pygame.image.load("Assets/BowAnimation/bow (2).png")
bow3 = pygame.image.load("Assets/BowAnimation/bow (3).png")
bow4 = pygame.image.load("Assets/BowAnimation/bow (4).png")
bow5 = pygame.image.load("Assets/BowAnimation/bow (5).png")
bow6 = pygame.image.load("Assets/BowAnimation/bow (6).png")
bow7 = pygame.image.load("Assets/BowAnimation/bow (7).png")
bow8 = pygame.image.load("Assets/BowAnimation/bow (8).png")
bow9 = pygame.image.load("Assets/BowAnimation/bow (9).png")
dragon = pygame.image.load("Assets/Dragon.png")
arrow = pygame.image.load("Assets/Arrow.png")
arrow = pygame.transform.scale(arrow, (50, 25))
#image lists
fire_ball = [fire1, fire2, fire3, fire4, fire5, fire6]
player_idle = [idle1, idle2, idle3]
player_run = [run1, run2, run3, run4, run5, run6]
player_jump = [jump1, jump2, jump3, jump4, jump5, jump6]
bow = [bow1, bow2, bow3, bow4, bow5, bow6, bow7, bow8, bow9]
player_animation = player_idle
player_animations = [player_idle, player_run, player_jump, bow]
#This array of arrays lets us easily navigate between player animations

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
#arrow variables
arrowSpeed = 30
arrowY = 620
arrowX = playerX
arrow_exist = False


def draw_screen():#This manages a majority (if not all) of the blit commands as well as the game over state/UI
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    player_image = pygame.transform.scale(player_animation[int(playIndex)], (100, 100))
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
    #arrow display
    if arrowX < 700 and arrow_exist:
        screen.blit(arrow, (arrowX, arrowY))

    #UI
    score_display = font.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(score_display, (30, 20))
    health_display = font.render('Health: ' + str(playerHealth), True, (255, 255, 255))
    screen.blit(health_display, (30, 70))
    dragon_display = font.render('Dragon Health: ' + str(dragonHealth), True, (255, 255, 255))
    screen.blit(dragon_display, (500, 30))

    #game over
    if game_over:
        screen.fill((0, 0, 0))
        game_over_display = font.render('GAME OVER!', True, (255, 255, 255))
        gg_display2 = font.render('Your score was:  ' + str(score), True, (255, 255, 255))
        screen.blit(game_over_display, (280, 380))
        screen.blit(gg_display2, (280, 420))

#player functions

#for animate_player you could also make the loop speed change with each animation, but I didn't find that necessary
def animate_player(x,y):
    global player_animation
    global looping
    if y != 0:
        player_animation = player_animations[2]
        looping = False
    elif not canShoot:
        player_animation = player_animations[3]
        looping = False
    elif x != 0:
        player_animation = player_animations[1]
        looping = True
    elif canShoot:
        player_animation = player_animations[0]
        looping = True
#This doesn't need to be a function but it could be a good introduction to global variables or just organizing one's code with functions
def jump(y):
    global isFalling#lets us change falling from inside the function
    if y < 300:#detects if we have reached maximum height
        isFalling = True#updates falling

#collision
def is_colliding(x1, x2, y1, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))#this calculates the distance between the 2 objects
    #it uses the pythagorean theorum
    if distance < 50:
        return True
    else:
        return False

clock = pygame.time.Clock()
intro.play()
while run:

    #Control setup
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
            if isJump == False:#In the pygame.KEYDOWN if-statement
                if event.key == pygame.K_SPACE:
                    playIndex = 0#sets animation index to 0. We have not gotten to this variable yet, but it will be important for animation sections
                    playerY_change = 50#sets playerYChang = 50 (represents the speed of the jump)
                    isJump = True#sets the jumping variable to true (important for animation and physics)

            if canShoot == True and not arrow_exist:#You don't need the == but it could be easier for the kids to understand.
                if event.key == pygame.K_f:
                    playIndex = 0
                    canShoot = False


    #moves player and checks for edges
    if canShoot or isJump:
        playerX += playerX_change
        if playerX >= 580:
            playerX = 580
        elif playerX <= 10:
            playerX = 10

    #jump processing
    if isJump:
        canShoot = False
        jump(playerY)

        if isFalling:#this if/else determines whether theyre jumping up or falling down and applies motion accordingly
            playerY += playerY_change
        else:
            playerY -= playerY_change

        if playerY > 600:#this is the check for if theyre on the ground
            playerY = 600
            isFalling = False
            isJump = False
            canShoot = True
            playerY_change = 0

    #player animation
    animate_player(playerX_change, playerY_change)
    if playIndex < len(player_animation) - 1:
        playIndex += loopSpeed
    else:
        if looping:
            playIndex = 0
        elif not canShoot and not isJump:#this specifically checks if the bow animation is over
            isLeft = False
            canShoot = True
            arrow_exist = True
            bow_sound.play()
            arrowX = playerX


    #fireball
    if cooldown == 0 and offscreen:#respawns the fireball with a new and random time until it fires
        cooldown = random.randint(10, 40)
        fireX = 700
        offscreen = False
        canRoar = True
    elif cooldown == 0 and not game_over:#checks if a fireball can be fired
        if canRoar:
            roar.play()
            canRoar = False
        fireX -= fireSpeed
        if fireIndex < len(fire_ball)-1:#animates fireball
            fireIndex += 1
        else:
            fireIndex = 0
    else:#decreases the cooldown (20 decreases per second)
        cooldown -= 1
    if fireX < 0:#checks if fireball is offscrean and adds to the score
        offscreen = True
        score += 10

    #arrow section
    if arrow_exist:
        if is_colliding(arrowX, dragonX, arrowY, dragonY):
            arrow_exist = False
            dragonHealth -= 1
            arrowX = 900
            canShoot = True
            #ramps up difficulty
            fireSpeed += 10
            if dragonHealth == 0:
                game_over = True
                canRoar = False
                score += 100
        else:
            arrowX += arrowSpeed
    #collision checking player and fireball
    if is_colliding(playerX,fireX ,playerY , fireY) and not game_over:#checks to see if the fireball and the player are collding
        isHit = True
        playerHealth -= 1
        cooldown = random.randint(10, 40)
        fireX = 700
        offscreen = False
        canRoar = True


        if playerHealth == 0:#checks for gameover
            game_over = True
            score -= 100

    #OPTIONAL: DIFFICULTY
    if score > 100:
        fireSpeed = 50
    elif score > 300:
        fireSpeed += 55
    #processes that need to be checked every frame
    draw_screen()
    if game_over:
        canRoar = False
    pygame.display.update()
    clock.tick(FPS)

