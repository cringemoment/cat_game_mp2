import pygame
from src.renderer.fonts import dialoguefont

DIALOGUE_BOX_WIDTH = 0.85
DIALOGUE_BOX_HEIGHT = 0.3
IMAGE_BOX_RATIO = 1.2

class DialogueBox:
    def __init__(self, image, text, speed = 10, font = None):
        self.image_raw = pygame.image.load(f"assets/{image}")
        self.image = None
        self.next_ready = False

        self.full_text = text
        self.visible_chars = 0

        self.speed = speed #ms
        self.char_delay = speed / 1000.0 #dt is in seconds so we must convert
        self.timer = 0.0

        self.font = font or dialoguefont

        self.padding = 20
        self.bg_color = (20, 20, 20)
        self.border_color = (200, 200, 200)
        self.text_color = (255, 255, 255)

    def draw(self, surface):
        if self.image is None:
            self.image = self.image_raw.convert_alpha()

        sw, sh = surface.get_size()

        box_width = int(sw * DIALOGUE_BOX_WIDTH)
        box_height = int(sh * DIALOGUE_BOX_HEIGHT)
        box_x = (sw - box_width) // 2
        box_y = sh - box_height - self.padding

        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

        img_size = box_height // IMAGE_BOX_RATIO
        img = pygame.transform.scale(self.image, (img_size, img_size))

        img_x = box_x
        img_y = box_y - img_size

        surface.blit(img, (img_x, img_y))

        pygame.draw.rect(surface, self.bg_color, box_rect)
        pygame.draw.rect(surface, self.border_color, box_rect, 2)

        text_x = box_x + self.padding
        text_y = box_y + self.padding
        text_width = box_width - 2 * self.padding

        visible_text = self.full_text[:self.visible_chars]
        self._draw_wrapped_text(surface, visible_text, (text_x, text_y), text_width)

    def _draw_wrapped_text(self, surface, text, pos, max_width):
        x, y = pos
        words = text.split(" ")
        line = ""

        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                surface.blit(self.font.render(line, True, self.text_color), (x, y))
                y += self.font.get_height() + 4
                line = word + " "

        if line:
            surface.blit(self.font.render(line, True, self.text_color), (x, y))

    def update(self, surface, dt, paused):
        if not paused:
            if self.visible_chars < len(self.full_text):
                self.timer += dt
                while self.timer >= self.char_delay:
                    self.timer -= self.char_delay
                    self.visible_chars += 1
                    if self.visible_chars >= len(self.full_text):
                        self.next_ready = True
                        break

        self.draw(surface)

class Dialogue:
    def __init__(self, dialogues):
        self.dialogues = dialogues
        self.current_dialogue_box_index = 0
        self.current_dialogue_box = self.dialogues[0]
        self.finished = False

    def load(self, dialoguehandler):
        self.dialogue_handler = dialoguehandler

    def on_finish(self):
        pass

    def next(self):
        if not self.current_dialogue_box.next_ready: return

        self.current_dialogue_box_index += 1
        if self.current_dialogue_box_index >= len(self.dialogues):
            self.finished = True
            self.on_finish()
            return

        self.current_dialogue_box = self.dialogues[self.current_dialogue_box_index]

    def update(self, surface, dt, paused):
        self.current_dialogue_box.update(surface, dt, paused)

class DialogueInputHandler():
    def __init__(self, dialoguehandler, input1, input2, controls1, controls2):
        self.dialoguehandler = dialoguehandler
        self.inputs = [input1, input2]
        self.controllayouts = [controls1, controls2]

        self.controls = {
            "select": lambda: self.dialoguehandler.current_dialogue.next(),
        }

        self.keys = {}

        for input, control in zip(self.inputs, self.controllayouts):
            for keys in self.controls:
                for key in control.controls[keys]:
                    self.keys[input.get_key(key)] = keys

        self.pressed = []

    def check(self):
        for key in self.keys:
            if key():
                if key in self.pressed: continue

                self.pressed.append(key)
                self.controls[self.keys[key]]()

            else:
                if key in self.pressed:
                    self.pressed.remove(key)

class DialogueHandler:
    def __init__(self, game):
        self.game = game
        self.current_dialogue = None
        self.dialogueinputhandler = None

    def load_inputs(self, input1, input2, controls1, controls2):
        self.dialogueinputhandler = DialogueInputHandler(self, input1, input2, controls1, controls2)

    def set_dialogue(self, d):
        self.current_dialogue = d
        # self.game.sound_handler.play_sound("dialogue")

    def update(self, surface, dt):
        if self.current_dialogue is not None:
            self.game.paused = True
            if self.current_dialogue.finished:
                self.current_dialogue = None
                self.game.paused = False
                return

            self.dialogueinputhandler.check()
            if self.current_dialogue is not None: # bruh
                self.current_dialogue.update(surface, dt, self.game.menu_handler.open)
