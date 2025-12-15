import pygame

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 25)

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
    def __init__(self, menu, x, y, text, font, command, align = "left"):
        super().__init__(menu, x, y)
        self.font = font
        self.command = command
        self.color = (255, 255, 255)
        self.default_color = (255, 255, 255)
        self.highlighted_color = (255, 255, 0)
        self.align = align

        self.set_text(text)

    def set_text(self, text = None):
        if text:
            self.text = str(text)

        self.text_surf = self.font.render(self.text, True, self.color)

        if self.align == "left":
            self.rect = self.text_surf.get_rect(topleft=(self.x, self.y))
        elif self.align == "right":
            self.rect = self.text_surf.get_rect(topright=(self.x, self.y))

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

class NumberChooser(TextButton):
    def __init__(self, value = 0, min = None, max = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value

        print(min)
        if min is not None:
            self.min = min
        if max:
            self.max = max

    def left(self):
        if self.value - 1 < self.min: return
        self.value -= 1 #TODO: HOLD DOWN

    def right(self):
        if self.value + 1 > self.max: return
        self.value += 1 #TODO: HOLD DOWN

    def draw(self, surface):
        self.text_surf = self.font.render(str(self.value), True, self.color)
        self.rect = self.text_surf.get_rect(topleft=(self.x, self.y))
        surface.blit(self.text_surf, self.rect)

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

    def menu_down(self):
        if self.current_widget_index + 1 > len(self.widgets) - 1: return

        self.current_widget_index += 1
        self.widgets[self.current_widget_index - 1].on_unhighlight()
        self.widgets[self.current_widget_index].on_highlight()

    def menu_up(self):
        if self.current_widget_index - 1 < 0: return

        self.current_widget_index -= 1
        self.widgets[self.current_widget_index + 1].on_unhighlight()
        self.widgets[self.current_widget_index].on_highlight()

    def menu_left(self):
        self.widgets[self.current_widget_index].left()

    def menu_right(self):
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
            "left": lambda: self.menuhandler.current_menu.menu_left(),
            "right": lambda: self.menuhandler.current_menu.menu_right(),
            "down": lambda: self.menuhandler.current_menu.menu_down(),
            "up": lambda: self.menuhandler.current_menu.menu_up(),
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
            "options": OptionsMenu(self),
            "controls": ControlsMenu(self)
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
            TextButton(self, 875, 75, text="Unpause", font=font, command=self.go_back, align="right"),
            TextButton(self, 875, 150, text="Options", font=font, command=self.open_options, align="right"),
            TextButton(self, 875, 225, text="Controls", font=font, command=self.open_controls, align="right"),
            TextButton(self, 875, 300, text="Main Menu", font=font, command=self.main_menu, align="right")
        ]

    def go_back(self):
        self.menuhandler.pause()

    def open_options(self):
        self.menuhandler.change_menu("options")

    def open_controls(self):
        self.menuhandler.change_menu("controls")

    def main_menu(self):
        pass #TODO: Make this become main menu / main page

class OptionsMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets = [
        ]

class ControlsMenu(Menu):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets = [

        ]

    def go_back(self):
        self.menuhandler.change_menu("default")
