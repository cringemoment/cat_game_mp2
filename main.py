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
"idle": "smaller_test.png",
"crouch": "smaller_crouch.png"
}

test_controller_spritelist = {
"idle": "player2_idle.png",
"crouch": "player2_idle.png"
}

test_controls = {
    "jump": pygame.K_SPACE,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "crouch": pygame.K_s
}

try:
    testcontroller = pygame.joystick.Joystick(0)
    testcontroller.init()

    testplayer = Player(testlevel.spawn_pos, test_controls, test_spritelist)
    testplayer2 = Player((100, 100), {"jump": pygame.K_SPACE, "left": pygame.K_a, "right": pygame.K_d}, test_controller_spritelist)
except:
    print("controller no work")
    testplayer = Player(testlevel.spawn_pos, test_controls, test_spritelist)
    testplayer2 = Player((100, 100), test_controls, test_controller_spritelist)

sprites = pygame.sprite.Group(testplayer, testplayer2)

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

    sprites.update(testlevel.collision_tiles, dt)
    sprites.draw(s)

    testlevel.draw(s)
    pygame.display.flip()

pygame.quit()
