from webbrowser import open_new

import pygame
import json

from src.renderer.fonts import menu_font as font

class Widget:
    def __init__(self, menu, x, y):
        self.menu = menu
        self.x = x
        self.y = y

    def on_highlight(self):
        pass

    def on_unhighlight(self):
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

class NumberChooser(Widget):
    def __init__(self, menu, x, y, text, value = 0, min = None, max = None, font = None, align = "right"):
        super().__init__(menu, x, y)

        self.value = value
        self.text = text
        self.font = font
        self.align = align
        self.value = value

        self.color = (255, 255, 255)

        self.border_radius = 5

        if min is not None:
            self.min = min
        if max:
            self.max = max

        self.text_surf = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surf.get_rect(topleft=(self.x, self.y))
        if align == "right":
            self.x -= self.text_rect.width

        self.set_value_rect()

    def set_value_rect(self):
        self.text_surf = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surf.get_rect(topleft=(self.x, self.y))

        self.number_padding = 10

        self.value_surf = self.font.render(str(self.value), True, self.color)
        self.rect = self.value_surf.get_rect(topright = (self.x - self.number_padding, self.y + self.text_rect.height))

        self.slider_width = 100
        self.slider_height = 6

        self.slider_x = self.text_rect.left
        self.slider_y = self.rect.centery - self.slider_height // 2

        if hasattr(self, "min") and hasattr(self, "max"):
            span = self.max - self.min
            t = (self.value - self.min) / span if span != 0 else 0
            t = max(0, min(1, t))  # clamp
            self.slider_fill_width = int(self.slider_width * t)
        else:
            self.slider_fill_width = 0

    def left(self):
        if self.value - 1 < self.min: return
        self.value -= 1 #TODO: HOLD DOWN
        self.set_value_rect()

    def right(self):
        if self.value + 1 > self.max: return
        self.value += 1 #TODO: HOLD DOWN
        self.set_value_rect()

    def draw(self, surface):
        # Draw text & number
        surface.blit(self.text_surf, self.text_rect)
        surface.blit(self.value_surf, self.rect)

        # Outline
        pygame.draw.rect(surface, (180, 180, 180), (self.slider_x, self.slider_y, self.slider_width, self.slider_height), width = 2, border_radius = self.border_radius)

        # Fill
        pygame.draw.rect(surface, (255, 255, 255), (self.slider_x, self.slider_y, self.slider_fill_width, self.slider_height), border_radius = self.border_radius)

class ControlWidget(Widget):
    def __init__(self, menu, x, y, action, keybind1, keybind2, font=None):
        super().__init__(menu, x, y)
        self.action = action
        self.kb1 = keybind1
        self.kb2 = keybind2
        self.font = font

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
                if self.keys[key] != "pause" and not self.menuhandler.open: continue

                self.pressed.append(key)
                self.menucontrols[self.keys[key]]()

            else:
                if key in self.pressed:
                    self.pressed.remove(key)

class MenuHandler:
    def __init__(self, game):
        self.game = game
        self.open = False
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
        self.open = not self.open
        self.change_menu("default")

        if self.open:
            self.game.sound_handler.bg_music_channel.pause()
        else:
            self.game.sound_handler.bg_music_channel.unpause()

    def update(self, surface):
        self.input_handler.check()

        if self.open:
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
        self.menuhandler.game.paused = False
        self.menuhandler.open = False
        self.menuhandler.game.load_level("main_menu")

class OptionsMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets = [
            NumberChooser(self, 875, 75, text = "Volume", value = 5, min = 0, max = 10, font = font, align = "right")
        ]

class ControlsMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open("src/player/controls/profile_1.json") as f:
            controls = json.load(f)
            for action in controls:
                for keybind in controls[action]:
                    pass
                    # if type(keybind).__name__ == "int":
                    #     # print(f"{action}: {pygame.key.name(keybind)}")
                    # else:
                    #     # print(f"{action}: {keybind}")

        self.widgets = [
            TextButton(self, 875, 75, text="Unpause", font=font, command=self.go_back, align="right")
        ]

    def go_back(self):
        self.menuhandler.change_menu("default")
