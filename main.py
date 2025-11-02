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

test_spritelist = {
"idle": "player1_idle.png"
}

test_controller_spritelist = {
"idle": "player2_idle".png
}

testplayer = Player(testlevel.spawn_pos, {"jump": pygame.K_SPACE, "left": pygame.K_a, "right": pygame.K_d}, test_spritelist)
testplayer2 = Player(testlevel.spawn_pos, {"jump": pygame.K_SPACE, "left": pygame.K_a, "right": pygame.K_d}, test_spritelist)

player_group = pygame.sprite.Group(testplayer)

s.fill(background_color)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        # if event.type == pygame.KEYDOWN:
        #     print(f"Key pressed: {pygame.key.name(event.key)}")

        if event.type == pygame.QUIT:
            running = False

    s.fill(background_color)

    #getting the change in time between frames
    dt = clock.tick(MAX_FRAMES) / 1000

    player_group.update(testlevel.collision_tiles, dt)
    player_group.draw(s)

    testlevel.draw(s)
    pygame.display.flip()

pygame.quit()
