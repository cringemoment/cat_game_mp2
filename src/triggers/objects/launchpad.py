from src.renderer.spriteobject import Sprite
from src.triggers.triggerobject import Trigger

class LaunchPad(Sprite, Trigger):
    def __init__(self, *args, **kwargs):
        level = kwargs.pop("level")
        Sprite.__init__(self, level)
        Trigger.__init__(self, *args, **kwargs, level = level)
        self.object_interactible = True
        self.on = False

        sprites = {
            "pressed": "objects/button_pressed.png"
        }

        self.set_sprites(sprites)

    def on_enter(self, player):
        player.vely = -23

    def on_both_leave(self):
        Trigger.on_both_leave(self)
        self.change_image("default")
        self.level.game.sound_handler.play_sound("button")
        self.on = False
