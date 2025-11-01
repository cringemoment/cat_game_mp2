import pygame
from src.loadtilemap import load_tilemap
from src.player import Player

pygame.init()

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
WINDOW_TITLE = "catxolotl"

MAX_FRAMES = 60

s = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

background_color = (30, 30, 30)

testlevel = load_tilemap(s, "levels/testlevel.tmx")
testplayer = Player(testlevel.spawn_pos, {"jump": pygame.K_SPACE, "left": pygame.K_a, "right": pygame.K_d})

player_group = pygame.sprite.Group(testplayer)

s.fill(background_color)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        #debug to see whats being printed
        # if event.type == pygame.KEYDOWN:
        #     print(f"Key pressed: {pygame.key.name(event.key)}")

        if event.type == pygame.QUIT:
            running = False

    s.fill(background_color)

    player_group.update(testlevel.collision_tiles)
    player_group.draw(s)

    testlevel.draw(s)
    pygame.display.flip()

    clock.tick(MAX_FRAMES)

pygame.quit()
