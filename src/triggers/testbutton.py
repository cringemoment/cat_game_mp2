from src.renderer.spriteobject import Sprite
from src.triggers.triggerobject import Trigger

class Button(Sprite, Trigger):
    def __init__(self, *args, **kwargs):
        Sprite.__init__(self)
        Trigger.__init__(self, *args, **kwargs)

        sprites = {
            "pressed": "objects/button_pressed.png"
        }

        self.set_sprites(sprites)

    def on_enter(self, player):
        Trigger.on_enter(self, player)
        self.change_image("pressed")

    def on_both_leave(self):
        Trigger.on_both_leave(self)
        self.change_image("default")
