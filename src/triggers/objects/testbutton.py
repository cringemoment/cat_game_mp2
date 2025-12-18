from src.renderer.spriteobject import Sprite
from src.triggers.triggerobject import Trigger

from src.renderer.particleobject import testpart

class Button(Sprite, Trigger):
    def __init__(self, *args, **kwargs):
        level = kwargs.pop("level")
        Sprite.__init__(self, level)
        Trigger.__init__(self, *args, **kwargs, level = level)

        sprites = {
            "pressed": "objects/button_pressed.png"
        }

        self.set_sprites(sprites)

    def on_enter(self, player):
        Trigger.on_enter(self, player)
        self.change_image("pressed")

        testpart.spawn_effect(self.level, 100, 100)

    def on_both_leave(self):
        Trigger.on_both_leave(self)
        self.change_image("default")

class PermanentButton(Sprite, Trigger):
    def __init__(self, *args, **kwargs):
        level = kwargs.pop("level")
        Sprite.__init__(self, level)
        Trigger.__init__(self, *args, **kwargs, level = level)
        self.open = False

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