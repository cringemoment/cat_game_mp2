from src.dialogue.dialogueobject import *
from src.levels.level import levels, phonebook_levels
from src.renderer.fonts import title_font, subtitle_font

from json import load

level_0 = Dialogue([
    DialogueBox("sprites/players/catdialogue.png", "Yello?"),
    DialogueBox("sprites/players/missioncontrol.png", "Hello, Agent Calico.", 40),
    DialogueBox("sprites/players/missioncontrol.png", "I know you've been out of the game for a while,"),
    DialogueBox("sprites/players/missioncontrol.png", "But this intel mission is too critical to put anyone else on the job."),
    DialogueBox("sprites/players/catdoubt.png", "We're out of the business now, man."),
    DialogueBox("sprites/players/catdoubt.png", "Go find someone else."),
    DialogueBox("sprites/players/missioncontrol.png", "Five million dollars."),
    DialogueBox("sprites/players/catdialogue.png", ".."),
    DialogueBox("sprites/players/axolotldialogue.png", ".."),
    DialogueBox("sprites/players/catdoubt.png", "..."),
])

level_1 = Dialogue([
    DialogueBox("sprites/players/missioncontrol.png", "It's getting real now, Agent Calico."),
    DialogueBox("sprites/players/missioncontrol.png", "We've got a real promising lead."),
    DialogueBox("sprites/players/catdialogue.png", "Just say where, and I'll be there."),
])

level_2 = Dialogue([
    DialogueBox("sprites/players/missioncontrol.png", "Agent Calico! No time to explain. We've got a new lead. Get there as soon as you can."),
    DialogueBox("sprites/players/catdoubt.png", "You don't pay us enough for this..."),
    DialogueBox("sprites/players/axolotldialogue.png", "He definitely does..."),
    DialogueBox("sprites/players/catdoubt.png", "..."),
])

left_align_x = 80
left_spine_x = 470
left_count = 5
mysterious_padding = 6

level_name_positions = {
"level_0": 130,
"level_1": 180,
"level_2": 230,
"level_3": 280
}

class PhoneBookInputHandler():
    def __init__(self, handler, input1, input2, controls1, controls2):
        self.handler = handler
        self.inputs = [input1, input2]
        self.controllayouts = [controls1, controls2]

        self.menucontrols = {
            "pause": lambda: self.handler.close_book(),
            "left": lambda: self.handler.left(),
            "right": lambda: self.handler.right(),
            "down": lambda: self.handler.down(),
            "up": lambda: self.handler.up(),
            "select": lambda: self.handler.select()
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
                if not self.handler.open: continue

                self.pressed.append(key)
                self.menucontrols[self.keys[key]]()

            else:
                if key in self.pressed:
                    self.pressed.remove(key)

class PhoneBook:
    def __init__(self, game):
        self.dialogues = {
        "level_0": level_0,
        "level_1": level_1,
        "level_2": level_0,
        "level_3": level_0,
        }

        self.game = game
        self.open = False
        self.current_popup = self.dialogues["level_0"]
        self.load_levels()
        self.oops = False
        self.loading = False

        #preloading render stuff
        self.book = pygame.image.load("assets/menus/book_open.png")

        self.current_level_y = 0

    def load_inputs(self, i1, i2, c1, c2):
        self.input_handler = PhoneBookInputHandler(self, i1, i2, c1, c2)

    def left(self):
        pass

    def right(self):
        pass

    def up(self):
        if self.current_level_y - 1 < 0: return
        self.current_level_y -= 1

    def down(self):
        if self.current_level_y + 1 > self.max_level: return
        self.current_level_y += 1

    def select(self):
        if not self.oops: #incredible
            self.oops = True
            return

        self.open = False
        self.game.paused = False
        self.loading = True
        self.game.transition_load_level(list(levels.keys())[self.current_level_y + 1])

    def open_book(self):
        if not self.loading:
            self.load_levels()
            self.open = True

    def close_book(self):
        self.oops = False #incredible
        self.open = False

    def play(self):
        if not self.current_popup is None:
            self.current_popup.on_finish = self.open_book
            self.game.dialogue_handler.set_dialogue(self.current_popup)
            self.current_popup = None
        else:
            self.open_book()

    def load_levels(self):
        self.level_file = load(open("src/levels/unlocked_levels.json"))
        self.max_level = max(loc for loc, val in enumerate(self.level_file) if self.level_file[val] == 1)

    def update(self, surface):
        if self.open:
            surface.blit(self.book, (0, 0))

            for i, level_name in enumerate(phonebook_levels):
                self.color = (0, 0, 0)

                if not self.level_file[level_name]:
                    self.color = (88, 88, 88)

                if i == self.current_level_y:
                    self.color = (255, 255, 0)

                level = levels[level_name]

                if self.level_file[level_name]:
                    title = title_font.render(level.name, False, self.color)
                    subtitle = subtitle_font.render(level.subtitle, False, (88, 88, 88))
                else:
                    title = title_font.render(level.name, False, self.color)
                    subtitle = subtitle_font.render("***-***-****", False, (88, 88, 88))

                if i < left_count:
                    title_rect = title.get_rect(bottomleft = (left_align_x, level_name_positions[level_name]))
                    subtitle_rect = subtitle.get_rect(bottomright = (left_spine_x, level_name_positions[level_name] - mysterious_padding))
                    surface.blit(title, title_rect)
                    surface.blit(subtitle, subtitle_rect)

            self.input_handler.check()
