#Additions to add (some files included in project folder some not): health up, music, fuel gauge, other obstacle types
#Some of the code is complicated and too hard for beginners. I've marked it as such.
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))
font = pygame.font.SysFont("Arial", 40)

bg = pygame.image.load("assets/BG.jpg")
bg = pygame.transform.scale(bg, (800, 800))

asteroid = pygame.image.load("assets/Asteroid.jpg")
asteroid.set_colorkey((255,255,255))
asteroid50 = pygame.transform.scale(asteroid, (50, 50))
asteroid100 = pygame.transform.scale(asteroid, (100, 100))
asteroid150 = pygame.transform.scale(asteroid, (150, 150))
sizes = [asteroid50, asteroid100, asteroid150]

player_surface = pygame.image.load("assets/Ship.png")
player_surface = pygame.transform.scale(player_surface, (80, 80))

projectileFrames = []
for i in range (6):
    temp_sprite = pygame.image.load(f"assets/projectile/{i}.png")
    temp_sprite = pygame.transform.rotozoom(temp_sprite, 90, 0.8)
    projectileFrames.append(temp_sprite)

#variables
running = True
score = 0
game_over = False
#player variables
playerX = 400
playerY = 750
playerX_change = 0
speed = 12
health = 3
cooldown = 0
#asteroid variables
asteroidSizeList = []
asteroidLocationList = []
SPAWNASTEROID = pygame.USEREVENT
pygame.time.set_timer(SPAWNASTEROID, 400)
#projectile variables
indexList = []#NOTE: if with beginners I'd recomend either not doing the animation or making it so only 1 projectile
#is onscreen at a time (using booleans). Index list is a more advanced concept
projectileLocations = []

#function

#asteroid functions
def create_asteroid():
    asteroid_choice = random.choice(sizes)
    asteroidSizeList.append(asteroid_choice)
    location = (random.randint(25, 775), 0)#measuring location from midbottom
    asteroidLocationList.append(asteroid_choice.get_rect(midbottom = (location)))

def display_asteroids(surfaces, rects):
    for i in range(len(surfaces)):
        screen.blit(surfaces[i], rects[i])

def move_asteroids(asteroids):
    for asteroid in asteroids:
        asteroid.centery += speed/2
    return asteroids

#projectile functions
def create_projectile():
    indexList.append(0)
    rect = projectileFrames[0].get_rect(midbottom = (playerX, 760))
    return rect

def move_projectiles(projectiles):
    for projectile in projectiles:
        projectile.centery -= speed/2
    return projectiles

def display_projectiles(indexes, rects):
    for i in range(len(indexes)):
        surface = projectileFrames[int(indexes[i])]
        rect = surface.get_rect(midbottom = rects[i].midtop)
        screen.blit(surface, rect)


#general functions
def check_collision(rect, asteroids):
    for asteroid in asteroids:
        if rect.colliderect(asteroid):

            if rect.centery != playerY: #checks to see if it is a player or projectile (optional code: advanced)
                index = asteroidLocationList.index(asteroid)

                #creates 2 smaller asteroids placed to the left and right of the original (optional code)
                if asteroidSizeList[index] == asteroid150:
                    for i in range(2):
                        asteroidSizeList.append(asteroid100)
                    asteroidLocationList.append(asteroid100.get_rect(center=(asteroid.centerx - 50, asteroid.centery)))
                    asteroidLocationList.append(asteroid100.get_rect(center=(asteroid.centerx + 50, asteroid.centery)))

                elif asteroidSizeList[index] == asteroid100:
                    for i in range(2):
                        asteroidSizeList.append(asteroid50)
                    asteroidLocationList.append(asteroid50.get_rect(center=(asteroid.centerx - 25, asteroid.centery)))
                    asteroidLocationList.append(asteroid50.get_rect(center=(asteroid.centerx + 25, asteroid.centery)))

            asteroid.top = 850
            return True
    return False

def draw_screen():
    if not game_over:
        screen.blit(bg, (0,0))

        screen.blit(player_surface, player_rect)

        display_asteroids(asteroidSizeList, asteroidLocationList)
        display_projectiles(indexList, projectileLocations)

        pygame.draw.rect(screen, [220, 100, 100], [600, 0, 200/3 * health, 35], False)

        score_display = font.render("Score: " + str(score), True, [255, 255, 255])
        score_rect = score_display.get_rect(topleft = (0,0))
        screen.blit(score_display, score_rect)

    else:
        screen.fill((100, 50, 200))
        display1 = font.render("Game Over!", True, [255, 255, 255])
        display1_rect = display1.get_rect(center=(400, 300))
        screen.blit(display1, display1_rect)
        display2 = font.render("Your score was: " + str(score), True, [255, 255, 255])
        display2_rect = display2.get_rect(center=(400, 400))
        screen.blit(display2, display2_rect)
        display3 = font.render("Press space to play again!", True, [255, 255, 255])
        display3_rect = display3.get_rect(center=(400, 500))
        screen.blit(display3, display3_rect)

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
                playerX_change = speed
            if event.key == pygame.K_LEFT:
                playerX_change = -speed
            if event.key == pygame.K_SPACE and cooldown < 0:
                if game_over:
                    #resets game
                    game_over = False
                    health = 3
                    asteroidSizeList.clear()
                    asteroidLocationList.clear()
                    projectileLocations.clear()
                    indexList.clear()
                    playerX = 400
                    playerY = 750
                    score = 0
                else:
                    cooldown = 20
                    projectileLocations.append(create_projectile())
        if event.type == SPAWNASTEROID:
            create_asteroid()

    playerX += playerX_change
    player_rect = player_surface.get_rect(center=(playerX, playerY))
    if player_rect.left < 0:
        player_rect.left = 0
    elif player_rect.right > 800:
        player_rect.right = 800

    #asteroids
    asteroidLocationList = move_asteroids(asteroidLocationList)

    if check_collision(player_rect, asteroidLocationList):
        health -= 1



    #projectiles
    projectileLocations = move_projectiles(projectileLocations)

    # animation
    for i in range(len(indexList)):
        if indexList[i] < 5:
            indexList[i] += 0.2

    for projectile in projectileLocations:
        if check_collision(projectile, asteroidLocationList):
            projectile.bottom = 0
            score += 10

    cooldown -= 1

    if health < 1:
        if not game_over:
            cooldown = 15
        game_over = True


    draw_screen()
    pygame.display.update()
    clock.tick(60)