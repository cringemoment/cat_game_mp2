import pygame
import math

class TransitionHandler:
    def __init__(self, game, duration = 0.9):
        self.game = game

        self.closed = False
        self.finished = False

        self.duration = duration
        self.start_radius = 800
        self.end_radius = 0
        self.time = 0

        self.pause_duration = 0.95
        self.pause_timer = 0

        self.p1_pos = (0, 0) #failsafes
        self.p2_pos = (200, 200)

        #for level loading
        self._transition_state = None
        self._queued_func = None

    def transition_in_out(self, func, p1, p2):
        if self._transition_state is not None:
            return

        self._queued_func = func
        self._transition_state = "closing"
        self.game.sound_handler.play_sound("loading_in")

        self.close(p1, p2)

    def on_finish(self):
        if self._transition_state == "closing":
            if self._queued_func:
                self._queued_func()

            self._transition_state = "waiting"
            self.pause_timer = self.pause_duration

        elif self._transition_state == "opening":
            if "default" in self.game.current_level.dialogues:
                self.game.dialogue_handler.set_dialogue(self.game.current_level.dialogues["default"])
            self._transition_state = None
            self._queued_func = None

    def update_timers(self, dt):
        if self.time > 0:
            self.time -= dt
            if self.time <= 0:
                self.time = 0
                self.on_finish()

        if self._transition_state == "waiting":
            self.pause_timer -= dt
            if self.pause_timer <= 0:
                self._transition_state = "opening"
                self.open(self.game.player1, self.game.player2)

    def close(self, p1, p2):
        if self.game.current_level == None: return

        self.p1_pos = self.game.current_level.camera.get_screen_pos(p1, 20, 15)
        self.p2_pos = self.game.current_level.camera.get_screen_pos(p2, 28, 15)
        self.time = self.duration
        self.closed = True

    def open(self, p1, p2):
        if self.game.current_level == None: return

        self.p1_pos = self.game.current_level.camera.get_screen_pos(p1, 20, 15)
        self.p2_pos = self.game.current_level.camera.get_screen_pos(p2, 28, 15)

        self.time = self.duration
        self.closed = False

    def clamp(self, func, t):
        f0 = func(0)
        f1 = func(1)

        return (func(t) - f0) / (f1 - f0)

    def time_interpolator(self, t):
        return ((2 * (t - 0.37))**5)

    def draw(self, surface):
        t = max(self.time / self.duration, 0)

        if not self.closed:
            t = 1 - t

        t = self.clamp(self.time_interpolator, t)

        self.radius = int(self.end_radius + (self.start_radius - self.end_radius) * t)

        if self.closed or self.time > 0:
            self.blackout = pygame.Surface((960, 640), pygame.SRCALPHA)
            self.blackout.fill((0, 0, 0, 255))

        if self.time > 0:
            pygame.draw.circle(self.blackout, (0, 0, 0, 0), self.p1_pos, self.radius)
            pygame.draw.circle(self.blackout, (0, 0, 0, 0), self.p2_pos, self.radius)

        if self.closed or self.time > 0:
            surface.blit(self.blackout, (0, 0))

    def update(self, surface, dt):
        self.update_timers(dt)
        self.draw(surface)
