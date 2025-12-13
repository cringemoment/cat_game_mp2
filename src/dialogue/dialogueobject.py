import pygame

import pygame

class DialogueBox:
    def __init__(self, image, text, speed, font=None):
        # Lazy image loading
        self.image_raw = pygame.image.load(f"assets/{image}")
        self.image = None

        self.full_text = text
        self.visible_chars = 0

        self.speed = speed                  # ms per character
        self.char_delay = speed / 1000.0    # seconds per character
        self.timer = 0.0

        self.font = font or pygame.font.Font(None, 32)

        self.padding = 20
        self.bg_color = (20, 20, 20)
        self.border_color = (200, 200, 200)
        self.text_color = (255, 255, 255)

    def update(self, surface, dt):
        # Advance typing
        if self.visible_chars < len(self.full_text):
            self.timer += dt
            while self.timer >= self.char_delay:
                self.timer -= self.char_delay
                self.visible_chars += 1
                if self.visible_chars >= len(self.full_text):
                    break

        self.draw(surface)

    def draw(self, surface):
        # Lazy convert image (safe after display is set)
        if self.image is None:
            self.image = self.image_raw.convert_alpha()

        sw, sh = surface.get_size()

        box_width = int(sw * 0.9)
        box_height = int(sh * 0.4)
        box_x = (sw - box_width) // 2
        box_y = sh - box_height - self.padding

        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

        # Draw box
        pygame.draw.rect(surface, self.bg_color, box_rect, border_radius=12)
        pygame.draw.rect(surface, self.border_color, box_rect, 2, border_radius=12)

        # Image
        img_size = box_height - 2 * self.padding
        img = pygame.transform.smoothscale(self.image, (img_size, img_size))
        img_pos = (box_x + self.padding, box_y + self.padding)
        surface.blit(img, img_pos)

        # Text
        text_x = img_pos[0] + img_size + self.padding
        text_y = box_y + self.padding
        text_width = box_width - (img_size + 3 * self.padding)

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
                surface.blit(
                    self.font.render(line, True, self.text_color),
                    (x, y)
                )
                y += self.font.get_height() + 4
                line = word + " "

        if line:
            surface.blit(
                self.font.render(line, True, self.text_color),
                (x, y)
            )

class Dialogue:
    def __init__(self, dialogues):
        self.dialogues = dialogues
        self.current_dialogue_box_index = 0
        self.current_dialogue_box = self.dialogues[0]

    def next(self):
        self.current_dialogue_box_index += 1
        self.current_dialogue_box = self.dialogues[self.current_dialogue_box_index]

    def update(self, surface, dt):
        self.current_dialogue_box.update(surface, dt)

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


testtalk = Dialogue([
    DialogueBox("sprites/players/axodialogue1.png", "Hello!!! awawawawawawa >.< >.< aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 20)
])
