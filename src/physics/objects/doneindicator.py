from src.renderer.spriteobject import Sprite
from src.triggers.triggerobject import ActivatedObject

class DoneIndicator(Sprite, ActivatedObject):
    def __init__(self, level):
        Sprite.__init__(self, level)
        self.transparency = 0
        self.wait_time = 3
        self.wait_time2 = 4
        self.timer = 0
        self.timer2 = 0

    def on_trigger(self):
        self.timer = self.wait_time

    def go(self):
        self.fade_in(2)
        self.timer2 = self.wait_time2

    def update(self, surface, dt, **kwargs):
        super().update(surface, dt, **kwargs)
        if self.timer > 0:
            self.timer -= dt
            if self.timer <= 0:
                self.level.game.sound_handler.play_sound("levelend")
                self.go()

        if self.timer2 > 0:
            self.timer2 -= dt
            if self.timer2 <= 0:
                self.level.game.paused = False
                self.level.game.transition_load_level("main_menu")
