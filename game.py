import pygame
from src.levels.loadtilemap import load_tilemap
from src.player.player import Player

from src.levels.level import testlevel
from src.player.playerinput import Controller, Keyboard
from src.menu.menu import MenuHandler

from assets.sprites.players.spritelist import *

from src.player.controls import kbcontrols, jycontrols

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
WINDOW_TITLE = "catxolotl"
MAX_FRAMES = 60

background_color = (30, 30, 30)

class Game:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        self.menu_handler = MenuHandler(self)
        self.paused = False

        self.clock = pygame.time.Clock()

        self.keyboard = Keyboard()
        keyboard = Keyboard()

        try:
            testcontroller = pygame.joystick.Joystick(0)

            controller = Controller(testcontroller)

            self.player1 = Player(0, testlevel, keyboard, kbcontrols, test_spritelist)
            self.player2 = Player(1, testlevel, controller, jycontrols, test_controller_spritelist)
            self.menu_handler.load_inputs(keyboard, controller, kbcontrols, jycontrols)

        except Exception as e:
            print(e)
            self.player1 = Player(0, testlevel, keyboard, kbcontrols, test_spritelist)
            self.player2 = Player(1, testlevel, keyboard, kbcontrols, test_controller_spritelist)

            self.menu_handler.load_inputs(keyboard, keyboard, kbcontrols, kbcontrols)

        testlevel.load_window(self.window)
        self.load_level(testlevel)

        self.fps = 60

    def print_debugs(self):
        debugs = {
            "x": lambda: self.player2.x,
            "y": lambda: self.player2.y,
            "what": lambda: self.current_level.tiles.physics_objects
        }

        font = pygame.font.SysFont('Comic Sans MS', 20)
        for i, var in enumerate(debugs):
            color = (0, 255, 0) if bool(debugs[var]()) else (255, 0, 0)
            text = font.render(f"{var}: {debugs[var]()}", False, color, (0, 0, 0))
            self.window.blit(text, (10, i * 30 + 10))

    def load_level(self, level):
        self.current_level = level
        self.current_level.load_window(self.window)

        self.player1.level = level
        self.player2.level = level

        self.player1.x, self.player1.y = level.tiles.spawn_pos_1
        self.player2.x, self.player2.y = level.tiles.spawn_pos_2

        self.current_level.tiles.physics_objects.add(self.player1, self.player2)

    def update(self):
        self.window.fill(background_color)

        dt = self.clock.tick(MAX_FRAMES) / 1000
        self.fps = round(1/dt, 0)

        self.current_level.draw(self.window)

        self.menu_handler.update(self.window)

        if not self.paused:
            self.current_level.update_physics(dt)

        self.print_debugs()

        pygame.display.flip()

        if self.keyboard.get_key(pygame.K_k)():
            self.player1.fade_in(1)
