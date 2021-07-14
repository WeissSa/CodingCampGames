import random
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))

#music
BGMusic = pygame.mixer.music.load("Assets/BGMusic.mp3")
pygame.mixer.music.play(-1)#pics

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

#background variables
BGX = 0
BG2X = 800
scrollspeed = 10

#PokemonVariables
pokeX1 = 1200
pokeX2 = 600
pokeimage1 = pygame.transform.scale(random.choice(pokemonList), (100, 100))
pokeimage2 = pygame.transform.scale(random.choice(pokemonList), (100, 100))


def display_screen():
    #background
    screen.blit(BG, (0,0))#This is a fix for a bug which I'm not sure why it occurs. it looks a little glitchy but only
    #happens once
    screen.blit(BG, (BGX, 0))
    screen.blit(BG, (BG2X, 0))
    #player
    player_sprite = pygame.transform.scale(run[runIndex], (75, 50))
    player_sprite = pygame.transform.flip(player_sprite, True, False)
    screen.blit(player_sprite, (100, 600))

    #enemies
    screen.blit(pokeimage1, (pokeX1, 550))
    screen.blit(pokeimage2, (pokeX2, 550))


clock  =pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #animation:
    if runIndex < len(run) - 1:
        runIndex += 1
    else:
        runIndex = 0

    #background code
    BGX -= scrollspeed
    BG2X -= scrollspeed
    if BGX <= -800:
        BGX = 800
    elif BG2X <= -800:
        BG2X = 800


    pokeX1 -= scrollspeed
    pokeX2 -= scrollspeed
    if pokeX1 < -800:
        pokeX1 = random.randint(800, 1000)
        pokeimage1 = pygame.transform.scale(random.choice(pokemonList), (100, 100))
    elif pokeX2 < -800:
        pokeX2 = random.randint(800, 1000)
        pokeimage2 = pygame.transform.scale(random.choice(pokemonList), (100, 100))

    display_screen()
    pygame.display.update()
    clock.tick(20)