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
