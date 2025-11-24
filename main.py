import pygame
from src.loadtilemap import load_tilemap
from src.player import Player

from src.level import testlevel
from src.playerinput import Controller, Keyboard
from src.renderer.spriteobject import Animation

#FIX MOUSE AIMING WITH CAMERA ZOOMED IN !!!!!

pygame.init()

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
WINDOW_TITLE = "catxolotl"

MAX_FRAMES = 60

s = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

background_color = (30, 30, 30)

# testlevel = load_tilemap(s, "levels/boxworld.tmx")
testlevel.load_window(s)

idleanimation = Animation([
    "sprites/catidle1.png",
    "sprites/catidle2.png"
], 0.3)

idle2 = Animation([
    "sprites/axoidle1.png",
    "sprites/axoidle2.png"
], 0.3)

runninganim = Animation([
    "sprites/catrun1.png",
    "sprites/catrun2.png",
    "sprites/catrun3.png",
    "sprites/catrun4.png",
], 0.1)

runninganim2 = Animation([
    "sprites/axorun1.png",
    "sprites/axorun2.png",
    "sprites/axorun3.png",
    "sprites/axorun4.png",
], 0.1)

crouch = Animation([
    "sprites/catcrouch1.png",
    "sprites/catcrouch2.png",
    "sprites/catcrouch3.png",
    "sprites/catcrouch4.png",
    "sprites/catcrouch5.png",
    "sprites/catcrouch6.png",
    "sprites/catcrouch7.png",
], 0.01)

test_spritelist = {
"default": idleanimation,
"crouchanim": crouch,
"crouch": "sprites/catcrouch.png",
"running": runninganim
}

test_controller_spritelist = {
"default": idle2,
"crouchanim": "sprites/axocrouch.png",
"crouch": "sprites/axocrouch.png",
"running": runninganim2
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

    testplayer = Player(0, testlevel, testlevel.tiles.spawn_pos_1, test_controls, test_spritelist)
    testplayer2 = Player(1, testlevel, testlevel.tiles.spawn_pos_2, test_controller_controls, test_controller_spritelist, testcontroller)
except Exception as e:
    print(e)
    print("controller no work")
    testplayer = Player(0, testlevel, testlevel.tiles.spawn_pos_1, test_controls, test_spritelist)
    testplayer2 = Player(1, testlevel, testlevel.tiles.spawn_pos_2, test_controls, test_controller_spritelist)

sprites = testlevel.tiles.physics_objects
sprites.add(testplayer, testplayer2)
# sprites = pygame.sprite.Group(testplayer, testplayer2, testplayer.gun, testplayer2.gun)

s.fill(background_color)

running = True
clock = pygame.time.Clock()

fps = 60
breh = 100
framesavg = [0 for i in range(breh)]

def update_fps(length):
    framesavg.pop(0)
    framesavg.append(fps)
    return round(sum(framesavg)/length, 0)

debugs = {
    # "ground": lambda: testplayer.on_ground,
    "x": lambda: testplayer.x,
    # "velx": lambda: testplayer.velx,
    # "vely": lambda: testplayer.vely,
    # "camerax": lambda: testlevel.camera.x,
    # "cameray": lambda: testlevel.camera.y,
    "fps": lambda: update_fps(breh),
    "": lambda: testlevel.tiles.physics_objects
}

def print_debugs():
    font = pygame.font.SysFont('Comic Sans MS', 20)
    for i, var in enumerate(debugs):
        color = (0, 255, 0) if bool(debugs[var]()) else (255, 0, 0)
        text = font.render(f"{var}: {debugs[var]()}", False, color, (0, 0, 0))
        s.blit(text, (10, i * 30 + 10))

while running:
    for event in pygame.event.get():
        # if event.type == pygame.KEYDOWN:
        #     print(f"Key pressed: {pygame.key.name(event.key)}")

        if event.type == pygame.QUIT:
            running = False

    s.fill(background_color)

    #getting the change in time between frames
    dt = clock.tick(MAX_FRAMES) / 1000
    fps = round(1/dt, 0)

    testlevel.draw(s, dt)

    # sprites.update(testlevel, dt)
    # sprites.draw(s)

    print_debugs()

    pygame.display.flip()

pygame.quit()
