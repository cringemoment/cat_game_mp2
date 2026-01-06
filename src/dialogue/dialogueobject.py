import pygame

class DialogueBox:
    def __init__(self, image, text, speed = 25, font=None):
        self.image_raw = pygame.image.load(f"assets/{image}")
        self.image = None
        self.next_ready = False

        self.full_text = text
        self.visible_chars = 0

        self.speed = speed #ms
        self.char_delay = speed / 1000.0 #dt is in seconds so we must convert
        self.timer = 0.0

        self.font = font or pygame.font.Font(None, 32)

        self.padding = 20
        self.bg_color = (20, 20, 20)
        self.border_color = (200, 200, 200)
        self.text_color = (255, 255, 255)

    def draw(self, surface):
        pass

    def update(self, surface, dt):
        self.draw(surface)

class Dialogue:
    def __init__(self, dialogues):
        self.dialogues = dialogues
        self.current_dialogue_box_index = 0
        self.current_dialogue_box = self.dialogues[0]
        self.finished = False

    def load(self, dialoguehandler):
        self.dialogue_handler = dialoguehandler

    def next(self):
        if not self.current_dialogue_box.next_ready: return

        self.current_dialogue_box_index += 1
        if self.current_dialogue_box_index >= len(self.dialogues):
            self.finished = True
            self.on_finish()
            return

        self.current_dialogue_box = self.dialogues[self.current_dialogue_box_index]

    def on_finish(self):
        pass

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
            for keys in self.menucontrols:
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

class Dialogue:
    def __init__(self):
        self.dialogues = []
        self.current_dialogue_box_index = 0
        self.current_dialogue_box = self.dialogues[0]

    def next(self):
        self.current_dialogue_box_index += 1
        self.current_dialogue_box = self.dialogues[self.current_dialogue_box_index]

    def update(self):
        self.current_dialogue_box.update()
        self.current_dialogue_box.draw()
