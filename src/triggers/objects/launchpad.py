from src.renderer.spriteobject import Sprite
from src.triggers.triggerobject import Trigger

class LaunchPad(Sprite, Trigger):
    def __init__(self, *args, **kwargs):
        level = kwargs.pop("level")
        Sprite.__init__(self, level)
        Trigger.__init__(self, *args, **kwargs, level = level)
        self.object_interactible = True

    def on_enter(self, player):
        if "strength" in self.properties:
            player.vely = int(self.properties["strength"])
        else:
            player.vely = -20
        self.level.game.sound_handler.play_sound("boing")
