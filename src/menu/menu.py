import pygame

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)

class Widget:
    def __init__(self, menu, x, y):
        self.menu = menu
        self.x = x
        self.y = y

    def on_highlight(self):
        pass

    def on_select(self):
        pass

    def on_escape(self):
        pass

    def draw(self, surface):
        pass

    def left(self):
        pass

    def right(self):
        pass

class TextButton(Widget):
    def __init__(self, text, font, command, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = font
        self.command = command
        self.color = (255, 255, 255)
        self.default_color = (255, 255, 255)
        self.highlighted_color = (255, 255, 0)

        self.set_text(text)

    def set_text(self, text = None):
        if text:
            self.text = text

        self.text_surf = self.font.render(self.text, True, self.color)
        self.rect = self.text_surf.get_rect(topleft=(self.x, self.y))

    def on_highlight(self):
        self.color = self.highlighted_color
        self.set_text()

    def on_unhighlight(self):
        self.color = self.default_color
        self.set_text()

    def on_select(self):
        self.command()

    def draw(self, surface):
        surface.blit(self.text_surf, self.rect)

class ArrowSelector(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Menu:
    def __init__(self, menuhandler):
        self.overlay = pygame.Surface((2000, 2000))
        self.overlay.set_alpha(200)
        self.overlay.fill("#1b1b1b")
        self.menuhandler = menuhandler

        self.widgets = []
        self.current_widget_index = 0

    def draw_menu(self, surface):
        surface.blit(self.overlay, (0, 0))

        for widget in self.widgets:
            widget.draw(surface)

    def menudown(self):
        if self.current_widget_index + 1 > len(self.widgets) - 1: return

        self.current_widget_index += 1
        self.widgets[self.current_widget_index - 1].on_unhighlight()
        self.widgets[self.current_widget_index].on_highlight()

    def menuup(self):
        if self.current_widget_index - 1 < 0: return

        self.current_widget_index -= 1
        self.widgets[self.current_widget_index + 1].on_unhighlight()
        self.widgets[self.current_widget_index].on_highlight()

    def menuleft(self):
        self.widgets[self.current_widget_index].left()

    def menuright(self):
        self.widgets[self.current_widget_index].right()

    def select(self):
        self.widgets[self.current_widget_index].on_select()

class MenuInputHandler():
    def __init__(self, menuhandler, input1, input2, controls1, controls2):
        self.menuhandler = menuhandler
        self.inputs = [input1, input2]
        self.controllayouts = [controls1, controls2]

        self.menucontrols = {
            "pause": lambda: self.menuhandler.pause(),
            "left": lambda: self.menuhandler.current_menu.menuleft(),
            "right": lambda: self.menuhandler.current_menu.menuright(),
            "down": lambda: self.menuhandler.current_menu.menudown(),
            "up": lambda: self.menuhandler.current_menu.menuup(),
            "select": lambda: self.menuhandler.current_menu.select()
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
                if self.keys[key] != "pause" and not self.menuhandler.game.paused: continue

                self.pressed.append(key)
                self.menucontrols[self.keys[key]]()

            else:
                if key in self.pressed:
                    self.pressed.remove(key)

class MenuHandler:
    def __init__(self, game):
        self.game = game
        self.menus = {
            "default": PauseMenu(self),
            "options": OptionsMenu(self)
        }

        self.current_menu = self.menus["default"]

    def load_inputs(self, i1, i2, c1, c2):
        self.input_handler = MenuInputHandler(self, i1, i2, c1, c2)

    def change_menu(self, menu):
        self.current_menu = self.menus[menu]
        for i in self.current_menu.widgets:
            i.on_unhighlight()
        self.current_menu.widgets[0].on_highlight()
        self.current_menu.current_widget_index = 0

    def pause(self):
        self.game.paused = not self.game.paused
        self.change_menu("default")

    def update(self, surface):
        self.input_handler.check()

        if self.game.paused:
            self.current_menu.draw_menu(surface)

class PauseMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets = [
            TextButton("hello", font, self.go_back, self, 700, 100),
            TextButton("goobi c:", font, self.open_options, self, 700, 150)
        ]

    def go_back(self):
        self.menuhandler.pause()

    def open_options(self):
        self.menuhandler.change_menu("options")

class OptionsMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets = [
            TextButton("Woohoo! you made it", font, lambda: None, self, 500, 500),
            TextButton("Go Back", font, self.go_back, self, 500, 600)
        ]

    def go_back(self):
        self.menuhandler.change_menu("default")
