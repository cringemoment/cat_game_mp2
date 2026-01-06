from src.dialogue.dialogueobject import *
from src.levels.level import levels
from src.renderer.fonts import title_font, subtitle_font

level_0 = Dialogue([
    DialogueBox("sprites/players/catdialogue.png", "Who is this?"),
    DialogueBox("sprites/players/missioncontrol.png", "Hello, Agent Calico.", 50),
    DialogueBox("sprites/players/missioncontrol.png", "I know you've been out of the game for a while."),
])

level_name_positions = {
"level_0": (80, 100)
}

new_level_dialogues = {
"level_0": level_0
}

class PhoneBook:
    def __init__(self, game):
        self.game = game
        self.open = True
        self.current_popup = new_level_dialogues["level_0"]

        #preloading render stuff
        self.book = pygame.image.load("assets/menus/book_open.png")

    def open_book(self): #bruh
        self.open = True

    def play(self):
        if not self.current_popup is None:
            self.current_popup.on_finish = self.open_book
            self.game.dialogue_handler.set_dialogue(self.current_popup)
            self.current_popup = None

    def update(self, surface):
        if self.open:
            surface.blit(self.book, (0, 0))
            for level_name in levels:
                level = levels[level_name]
                title = title_font.render(level.name, False, (0, 0, 0))
                subtitle = subtitle_font.render(level.subtitle, False, (88, 88, 88))
                surface.blit(title, level_name_positions[level_name])
                surface.blit(subtitle, (level_name_positions[level_name][0], level_name_positions[level_name][1] + 30)) #bruh
