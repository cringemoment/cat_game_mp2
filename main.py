import pygame
from src.loadtilemap import load_tilemap
from src.player import Player

from src.playerinput import Controller, Keyboard

pygame.init()

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
WINDOW_TITLE = "catxolotl"

MAX_FRAMES = 60

s = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

background_color = (30, 30, 30)

testlevel = load_tilemap(s, "levels/boxworld.tmx")

test_spritelist = {
"default": "smaller_test.png",
"crouch": "smaller_crouch.png"
}

test_controller_spritelist = {
"default": "player2_smaller.png",
"crouch": "player2_crouch.png"
}

keyboard = Keyboard()
test_controls = {
    "jump": keyboard.get_key(pygame.K_SPACE),
    "left": keyboard.get_key(pygame.K_a),
    "right": keyboard.get_key(pygame.K_d),
    "crouch": keyboard.get_key(pygame.K_s),
    "shoot": keyboard.lmb
}

try:
    testcontroller = pygame.joystick.Joystick(0)

    controller = Controller(testcontroller)
    test_controller_controls = {
        "jump": controller.B_down,
        "left": controller.J1_left,
        "right": controller.J1_right,
        "crouch": controller.J1_down,
        "shoot": controller.RB
    }

    testplayer = Player(testlevel.spawn_pos, test_controls, test_spritelist)
    testplayer2 = Player(testlevel.second_spawn_pos, test_controller_controls, test_controller_spritelist, testcontroller)
except Exception as e:
    print(e)
    print("controller no work")
    testplayer = Player(testlevel.spawn_pos, test_controls, test_spritelist)
    testplayer2 = Player(testlevel.second_spawn_pos, test_controls, test_controller_spritelist)

sprites = testlevel.physics_objects
sprites.add(testplayer, testplayer2)
sprites = pygame.sprite.Group(testplayer, testplayer2, testplayer.gun, testplayer2.gun)

s.fill(background_color)

running = True
clock = pygame.time.Clock()

debugs = {
    "box_x": lambda: testlevel.physics_objects.sprites()[0].x,
    "box_y": lambda: testlevel.physics_objects.sprites()[0].y
}

def print_debugs():
    font = pygame.font.SysFont('Comic Sans MS', 20)
    for i, var in enumerate(debugs):
        color = (0, 255, 0) if bool(debugs[var]()) else (255, 0, 0)
        text = font.render(f"{var}: {debugs[var]()}", False, color, (0, 0, 0))
        s.blit(text, (10, i * 30 + 10))
    # s.blit(test)

while running:
    for event in pygame.event.get():
        # if event.type == pygame.KEYDOWN:
        #     print(f"Key pressed: {pygame.key.name(event.key)}")

        if event.type == pygame.QUIT:
            running = False

    s.fill(background_color)

    #getting the change in time between frames
    dt = clock.tick(MAX_FRAMES) / 1000

    testlevel.draw(s, dt)

    # sprites.update(testlevel, dt)
    sprites.draw(s)

    print_debugs()

    pygame.display.flip()

pygame.quit()
