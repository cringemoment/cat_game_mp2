from src.renderer.spriteobject import Sprite
from src.triggers.triggerobject import Trigger

from src.renderer.particleobject import testpart

class Button(Sprite, Trigger):
    def __init__(self, *args, **kwargs):
        level = kwargs.pop("level")
        Sprite.__init__(self, level)
        Trigger.__init__(self, *args, **kwargs, level = level)
        self.object_interactible = True
        self.on = False

        self.load_color()

    def load_color(self):
        color = getattr(self.properties, "color", "red")
        sprites = {
            "unpressed": f"objects/{color}_button.png",
            "pressed": f"objects/{color}_button_pressed.png"
        }

        self.set_sprites(sprites)
        self.change_image("unpressed")

    def on_enter(self, player):
        if not self.on:
            Trigger.on_enter(self, player)
            self.change_image("pressed")
            self.level.game.sound_handler.play_sound("button")
            self.on = True

    def on_both_leave(self):
        Trigger.on_both_leave(self)
        self.change_image("unpressed")
        self.level.game.sound_handler.play_sound("button")
        self.on = False

class PermanentButton(Sprite, Trigger):
    def __init__(self, *args, **kwargs):
        level = kwargs.pop("level")
        Sprite.__init__(self, level)
        Trigger.__init__(self, *args, **kwargs, level = level)
        self.open = False
        self.object_interactible = True

        sprites = {
            "pressed": "objects/button_pressed.png"
        }

        self.set_sprites(sprites)

    def on_any_enter(self, player):
        self.open = not self.open
        if self.open:
            self.change_image("pressed")
            Trigger.on_any_enter(self, player)
        else:
            self.change_image("default")
            Trigger.on_both_leave(self)

    def on_both_leave(self):
        pass

class LaunchPad(Button):
    def on_enter(self, player):
        player.vely -= 50