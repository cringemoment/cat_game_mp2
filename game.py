import pygame
from src.levels.loadtilemap import load_tilemap
from src.player.player import Player

from src.levels.level import testlevel
from src.player.playerinput import Controller, Keyboard
from src.menu.menu import MenuHandler

from assets.sprites.players.spritelist import *

from src.player.controls import kbcontrols, jycontrols, nopause

from src.dialogue.dialogueobject import testtalk, DialogueHandler

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
        self.dialogue_handler = DialogueHandler(self)
        self.dialogue_handler.set_dialogue(testtalk)
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
            self.dialogue_handler.load_inputs(keyboard, controller, kbcontrols, jycontrols)

        except Exception as e:
            print(e)
            self.player1 = Player(0, testlevel, keyboard, kbcontrols, test_spritelist)
            self.player2 = Player(1, testlevel, keyboard, nopause, test_controller_spritelist)

            self.menu_handler.load_inputs(keyboard, keyboard, kbcontrols, nopause)
            self.dialogue_handler.load_inputs(keyboard, keyboard, kbcontrols, nopause)

        testlevel.load_window(self.window)
        self.load_level(testlevel)

        self.mi = 20
        self.mimimi = [0] * self.mi

    def print_debugs(self):
        debugs = {
            "fps": lambda: sum(self.mimimi) // self.mi
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

        #REMOVE
        dt = self.clock.tick(MAX_FRAMES) / 1000
        self.mimimi.append(round(1/dt, 2))
        self.mimimi.pop(0)

        self.current_level.draw(self.window)

        if not self.paused:
            self.dialogue_handler.update(self.window, dt)
            self.current_level.update_physics(dt)

        #keep last!!!
        self.menu_handler.update(self.window)

        self.print_debugs()

        pygame.display.flip()

        if self.keyboard.get_key(pygame.K_k)():
            self.player1.fade_in(1)
