import pygame

class Button:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def on_highlight(self):
        pass

    def on_press(self):
        pass

    def draw(self, surface):
        pass

class Menu:
    def __init__(self):
        self.overlay = pygame.Surface((2000, 2000))
        self.overlay.set_alpha(200)
        self.overlay.fill("#1b1b1b")

        self.widgets = []

    def draw_menu(self, surface):
        surface.blit(self.overlay, (0, 0))

        for widget in self.widgets:
            widget.draw(surface)

class MenuInputHandler():
    def __init__(self, menuhandler, input1, input2):
        self.menuhandler = menuhandler
        self.input_1 = input1
        self.input_2 = input2
        self.controls = []
        self.pressed = []

        if type(self.input_1).__name__ == "Keyboard":
            self.controls.append(self.input_1.get_key(pygame.K_ESCAPE))
        else:
            self.controls.append(self.input_1.plus)

        if type(self.input_2).__name__ == "Keyboard":
            self.controls.append(self.input_2.get_key(pygame.K_ESCAPE))
        else:
            self.controls.append(self.input_2.plus)

    def check(self):
        for control in self.controls:
            if control():
                if control in self.pressed: continue

                self.pressed.append(control)
                self.menuhandler.game.paused = not self.menuhandler.game.paused
            else:
                if control in self.pressed:
                    self.pressed.remove(control)

class MenuHandler:
    def __init__(self, game):
        self.game = game
        self.menus = {
            "default": PauseMenu()
        }

        self.current_menu = "default"

    def load_inputs(self, i1, i2):
        self.input_handler = MenuInputHandler(self, i1, i2)

    def draw(self, surface):
        self.menus[self.current_menu].draw_menu(surface)

    def update(self, surface):
        self.input_handler.check()

        if self.game.paused:
            self.draw(surface)

class PauseMenu(Menu):
    def __init__(self):
        super().__init__()
