import pygame
pygame.init()


def load_images(lst: list, starting_name: str, ending_name: str, num_images: int, starting_num: int) -> list:
    """
    This is the same function from our previous project, except it can start at numbers other than 0 (since that is
    necessary for how the image files are formatted here).
    """
    for i in range(starting_num, starting_num + num_images):
        lst.append(pygame.image.load(starting_name + str(i) + ending_name))
    return lst


def animate(animation: list, current_index: float) -> float:
    """
    Take animation and the current_index and output the next index.
    The animation will loop if the current index == len(animation) -1.

    >>> animate([1,2,3], 1)
    1.2
    >>> animate([1,2,3,4], 3)
    3.2

    """
    if current_index < len(animation) - 1:
        return current_index + 0.2
    else:
        return 0



"""
Below is the assignment and definition of all important images and animations. Try to notice patterns!
I would recommend adding any images you want in the project here.
"""

BG_Shop = pygame.image.load("assets/backgrounds/Shop.jpg")
BG_level = pygame.image.load("assets/backgrounds/background.png")

crumble_animation = []
load_images(crumble_animation, "assets/Effects/crumble/earth2_", ".png", 6, 10)

impact_animation = []
load_images(impact_animation, "assets/Effects/impact/impact5_", ".png", 5, 1)

slash_animation = []
load_images(slash_animation, "assets/Effects/slash/wind1_", ".png", 4, 1)

robot_attack = []
load_images(robot_attack, "assets/enemies/Robot/attack/attack (", ").png", 4, 1)
robot_idle = []
load_images(robot_idle, "assets/enemies/Robot/idle/idle (", ").png", 6, 1)

samurai_attack = []
load_images(samurai_attack, "assets/enemies/Samurai/attack/attack (", ").png", 4, 1)
samurai_idle = []
load_images(samurai_idle, "assets/enemies/Samurai/idle/idle (", ").png", 4, 1)

axes = []
load_images(axes, "assets/items/axe ", ".png", 3, 1)
hammers = []
load_images(hammers, "assets/items/hammer ", ".png", 3, 1)
swords = []
load_images(swords, "assets/items/sword ", ".png", 3, 1)
potions = []
load_images(potions, "assets/items/potion ", ".png", 4, 1)

coin = pygame.image.load("assets/items/Nether_Star.png")

player_walk_up = []
load_images(player_walk_up, "assets/Player/walk-up/walk (", ").png", 10, 1)
player_walk_down = []
load_images(player_walk_down, "assets/Player/walk-down/walk (", ").png", 10, 1)
