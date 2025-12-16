from src.renderer.spriteobject import Sprite
from src.triggers.triggerobject import ActivatedObject

class Indicator(Sprite, ActivatedObject):
    def __init__(self, level):
        Sprite.__init__(self, level)
        self.transparency = 0

    def on_any_enter(self, player):
        self.fade_in(0.4)

    def on_both_leave(self):
        self.fade_out(0.2)
