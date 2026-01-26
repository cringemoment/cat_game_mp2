import pygame
from src.levels.loadtilemap import load_tilemap
from src.player.player import Player

from src.levels.level import levels
from src.player.playerinput import Controller, Keyboard
from src.menu.menu import MenuHandler

from assets.sprites.players.spritelist import *

from src.player.controls import kbcontrols, joycontrols, nopause
from src.dialogue.dialogueobject import DialogueHandler

from src.levels.phonebook import PhoneBook
from src.sound.sound import Sound

from src.renderer.transitionobject import TransitionHandler

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
WINDOW_TITLE = "catxolotl"
MAX_FRAMES = 60

background_color = (30, 30, 30)

class Game:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED)
        pygame.display.set_caption(WINDOW_TITLE)
        default_level = "level_2"
        self.current_level = None

        self.menu_handler = MenuHandler(self)
        self.dialogue_handler = DialogueHandler(self)
        self.phone_book = PhoneBook(self)
        self.sound_handler = Sound(self)
        self.transition_handler = TransitionHandler(self)

        self.paused = False

        self.clock = pygame.time.Clock()

        self.keyboard = Keyboard()
        keyboard = Keyboard()

        self.player1 = Player(0, test_spritelist)
        self.player2 = Player(1, test_controller_spritelist)

        i1 = keyboard
        c1 = kbcontrols

        try:
            testcontroller = pygame.joystick.Joystick(0)
            controller = Controller(testcontroller)

            i2 = controller
            c2 = joycontrols

        except Exception as e:
            print(e)

            i2 = keyboard
            c2 = nopause

        self.load_inputs(i1, i2, c1, c2)

        self.load_level(default_level)

        self.mi = 20
        self.mimimi = [0] * self.mi

        self.bruh = False
        self.p_pushed = False

    def load_inputs(self, i1, i2, c1, c2):
        self.player1.load_inputs(i1, c1)
        self.player2.load_inputs(i2, c2)

        self.menu_handler.load_inputs(i1, i2, c1, c2)
        self.dialogue_handler.load_inputs(i1, i2, c1, c2)
        self.phone_book.load_inputs(i1, i2, c1, c2)

    def print_debugs(self):
        debugs = {
            "fps": lambda: sum(self.mimimi) // self.mi,
        }

        font = pygame.font.SysFont('Comic Sans MS', 20)
        for i, var in enumerate(debugs):
            color = (0, 255, 0) if bool(debugs[var]()) else (255, 0, 0)
            text = font.render(f"{var}: {debugs[var]()}", False, color, (0, 0, 0))
            self.window.blit(text, (10, i * 30 + 10))

    def transition_load_level(self, level_name):
        self.dialogue_handler.current_dialogue = None
        self.transition_handler.transition_in_out(
            lambda: self.load_level(level_name),
            self.player1,
            self.player2
        )

    def load_level(self, level_name):
        self.current_level_name = level_name
        level = levels[level_name]
        self.current_level = level
        self.current_level.load_game(self)

        self.player1.kill()
        self.player2.kill()

        self.player1.level = level
        self.player2.level = level

        self.player1.x, self.player1.y = level.tiles.spawn_pos_1
        self.player2.x, self.player2.y = level.tiles.spawn_pos_2
        self.player1.velx = 0
        self.player1.vely = 0
        self.player2.velx = 0
        self.player2.vely = 0

        self.current_level.tiles.physics_objects.add(self.player1, self.player2)
        self.current_level.draw(self.window)

        self.dialogue_handler.current_dialogue = None

        self.sound_handler.play_bg_music(level.bg_music)

    def update(self):
        self.window.fill(background_color)

        dt = self.clock.tick(MAX_FRAMES) / 1000
        self.mimimi.append(round(1 / dt, 2))
        self.mimimi.pop(0)

        self.current_level.draw(self.window)
        self.dialogue_handler.update(self.window, dt)
        self.phone_book.update(self.window)

        if not self.paused:
            self.current_level.update_physics(dt)

        self.transition_handler.update(self.window, dt)

        self.menu_handler.update(self.window)

        self.print_debugs()

        pygame.display.flip()

        if self.keyboard.get_key(pygame.K_k)() and self.dialogue_handler.current_dialogue:
            self.dialogue_handler.current_dialogue.finished = True

        if self.keyboard.get_key(pygame.K_p)():
            if self.p_pushed: return
            self.p_pushed = True
            mx, my = pygame.mouse.get_pos()

            cam = self.current_level.camera

            # convert screen → world
            world_x = mx / cam.scale_factor_x + cam.offset.x
            world_y = my / cam.scale_factor_y + cam.offset.y

            self.player1.x = world_x - 32
            self.player1.y = world_y - 32
            self.player2.x = world_x + 32
            self.player2.y = world_y - 32

        else:
            self.p_pushed = False
