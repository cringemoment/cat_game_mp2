from src.dialogue.dialogueobject import *
from src.levels.level import levels
from src.renderer.fonts import title_font, subtitle_font

from json import load

level_0 = Dialogue([
    DialogueBox("sprites/players/catdialogue.png", "Who is this?"),
    # DialogueBox("sprites/players/missioncontrol.png", "Hello, Agent Calico.", 50),
    # DialogueBox("sprites/players/missioncontrol.png", "I know you've been out of the game for a while."),
])

left_align_x = 80
left_spine_x = 470
left_count = 5
mysterious_padding = 6

level_name_positions = {
"level_0": 130,
"level_1": 180
}

new_level_dialogues = {
"level_0": level_0,
"level_1": level_0
}

class PhoneBook:
    def __init__(self, game):
        self.game = game
        self.open = False
        self.current_popup = new_level_dialogues["level_0"]
        self.load_levels()

        #preloading render stuff
        self.book = pygame.image.load("assets/menus/book_open.png")

    def open_book(self):
        self.open = True

    def close_book(self):
        self.open = False

    def play(self):
        if not self.current_popup is None:
            self.current_popup.on_finish = self.open_book
            self.game.dialogue_handler.set_dialogue(self.current_popup)
            self.current_popup = None

    def load_levels(self):
        self.level_file = load(open("src/levels/unlocked_levels.json"))

    def update(self, surface):
        if self.open:
            surface.blit(self.book, (0, 0))
            for i, level_name in enumerate(levels[1:]):
                level = levels[level_name]

                if self.level_file[level_name]:
                    title = title_font.render(level.name, False, (0, 0, 0))
                    subtitle = subtitle_font.render(level.subtitle, False, (88, 88, 88))
                else:
                    title = title_font.render(level.name, False, (88, 88, 88))
                    subtitle = subtitle_font.render("***-***-****", False, (88, 88, 88))

                if i < left_count:
                    title_rect = title.get_rect(bottomleft = (left_align_x, level_name_positions[level_name]))
                    subtitle_rect = subtitle.get_rect(bottomright = (left_spine_x, level_name_positions[level_name] - mysterious_padding))
                    surface.blit(title, title_rect)
                    surface.blit(subtitle, subtitle_rect)
