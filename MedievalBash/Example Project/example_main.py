import pygame
import image_loader as pictures
import item_handler as items
import enemy
import random

pygame.init()
screen = pygame.display.set_mode((500, 500))
font = pygame.font.SysFont("Arial", 30)


# variables
running = True
state = "shop"
weapon_owned = False
game_won = False

# player variables
player_rect = pictures.player_walk_down[0].get_rect(center=(250, 250))
player_index = 0
walking_up = False

# scrolling variables
BGX = 250
BGY = 250
BG_change = [0, 0]

starting_positions = [(20, 20), (400, 400), (0, 400), (400, 0)]

enemy_1 = enemy.Enemy(x_change=0, y_change=0, sprite=pictures.samurai_idle[0],
                      rect=pictures.samurai_idle[0].get_rect(center=(random.choice(starting_positions))),
                      speed=1, index=0)

# slash variables
slash_index = 4

# intialize items
temp_rect = pygame.draw.rect(screen, (0, 0, 0), (0, 0, 0, 0), False)
money = 70
axe = items.Item(False, pictures.axes, 1, 40, 3, temp_rect)
hammer = items.Item(False, pictures.hammers, 1, 20, 2, temp_rect)
sword = items.Item(False, pictures.swords, 1, 10, 1, temp_rect)
potion = items.Item(False, pictures.potions, 0, 20, 0, temp_rect)
item_list = [axe, hammer, sword, potion]


# functions
def handle_shop() -> None:
    """Handles the shop segment of the game"""
    BG_Shop = pygame.transform.scale(pictures.BG_Shop, (500, 500))
    screen.blit(BG_Shop, (0, 0))

    # UI
    money_icon = pygame.transform.scale(pictures.coin, (30, 30))
    money_rect = money_icon.get_rect(midtop=(230, 10))
    money_display = font.render(str(money), True, (255, 255, 255))
    money_text_rect = money_display.get_rect(midleft=money_rect.midright)
    screen.blit(money_icon, money_rect)
    screen.blit(money_display, money_text_rect)

    if weapon_owned and potion.index > 0:
        space_display = font.render("Press space to continue", True, (255, 255, 255))
        space_rect = space_display.get_rect(center=(250, 450))
        screen.blit(space_display, space_rect)

    # items
    divider = screen.get_width() / (len(item_list) + 2)

    for i in range(1, len(item_list) + 1):
        index = item_list[i - 1].index
        if weapon_owned and item_list[i - 1].owned == False and item_list[i - 1].damage > 0:
            index = 0
        lst = item_list[i - 1].versions
        sprite = pygame.transform.scale(lst[index], (50, 50))
        pygame.draw.rect(screen, (100, 100, 200), (divider * i, 200, 50, 50), False)
        screen.blit(sprite, (divider * i, 200))
        item_list[i - 1].location = sprite.get_rect(topleft=(divider * i, 200))


def handle_dungeon() -> None:
    """Handles the dungeon segment of the game"""
    screen.fill((0, 0, 0))
    BG_level = pictures.BG_level
    BG_rect = BG_level.get_rect(center=(BGX, BGY))
    screen.blit(BG_level, BG_rect)



    if walking_up:
        animation = pictures.player_walk_up
    else:
        animation = pictures.player_walk_down
    player_sprite = pygame.transform.scale(animation[int(player_index)], (40, 50))
    player_rect = player_sprite.get_rect(center=(250, 250))
    screen.blit(player_sprite, player_rect)

    screen.blit(enemy_1.sprite, enemy_1.rect)

    if slash_index < 4:
        screen.blit(pictures.slash_animation[slash_index], (player_rect.left,  player_rect.top - walking_up * 80 + 40))

    pygame.draw.rect(screen, (255, 0, 0), (0, 0, 500 / (potion.index * 30) * health, 30), False)

    if game_won:
        screen.fill((100, 100, 100))
        space_display = font.render("You won!", True, (255, 255, 255))
        space_rect = space_display.get_rect(center=(250, 250))
        screen.blit(space_display, space_rect)


clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            for item in item_list:
                if item.location.collidepoint(pygame.mouse.get_pos()):
                    if item.index < len(item.versions) - 1 and item.price <= money:
                        if not weapon_owned or item.damage < 1:
                            item.index += 1
                            item.owned = True
                            money -= item.price
                            if item.damage > 0:
                                weapon_owned = True
                    elif item.owned:
                        item.index -= 1
                        money += item.price
                        if item.damage > 0:
                            weapon_owned = False
                            item.owned = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == "shop" and weapon_owned and potion.index > 0:
                    health = potion.index * 30
                    state = "dungeon"
                else:
                    slash_index = 0

            if event.key == pygame.K_LEFT:
                BG_change[0] = 10
            if event.key == pygame.K_RIGHT:
                BG_change[0] = -10
            if event.key == pygame.K_UP:
                walking_up = True
                BG_change[1] = 10
            if event.key == pygame.K_DOWN:
                walking_up = False
                BG_change[1] = -10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                BG_change[0] = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                BG_change[1] = 0


    if state == "shop":
        handle_shop()
    else:
        player_index = pictures.animate(pictures.player_walk_up, player_index)
        enemy_1.index = pictures.animate(pictures.samurai_idle, enemy_1.index)
        enemy_1.sprite = pictures.samurai_idle[int(enemy_1.index)]
        # y movement
        if BGY >= -20 and BGY < 530:
            BGY += BG_change[1]
            enemy_1.rect.centery += BG_change[1]
        if BGY >= 530:
            BGY = 529
        elif BGY < -20:
            BGY = -20

        # x movement
        if BGX >= -20 and BGX < 530:
            BGX += BG_change[0]
            enemy_1.rect.centerx += BG_change[0]
        if BGX >= 530:
            BGX = 529
        elif BGX < -20:
            BGX = -20

        handle_dungeon()

        if slash_index < 4:
            slash_index += 1

        if player_rect.colliderect(enemy_1.rect):
            health -= 1

        if health < 0:
            running = False

        if enemy_1.rect.collidepoint((player_rect.left,  player_rect.top - walking_up * 80 + 40)) and slash_index < 4:
            enemy_1.rect.center = (900, 900)
            game_won = True



    clock.tick(30)
    pygame.display.update()

pygame.quit()
