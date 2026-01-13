import pygame
import math

class TransitionHandler:
    def __init__(self, game, duration = 1):
        self.game = game

        self.closed = False
        self.finished = False

        self.duration = duration
        self.start_radius = 800
        self.end_radius = 0
        self.time = 0

        self.p1_pos = (0, 0) #failsafes
        self.p2_pos = (200, 200)

    def update_timers(self, dt):
        if self.time > 0:
            self.time -= dt

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

        radius = int(self.end_radius + (self.start_radius - self.end_radius) * t)

        if self.closed or self.time > 0:
            self.blackout = pygame.Surface((960, 640), pygame.SRCALPHA)
            self.blackout.fill((0, 0, 0, 255))

        if self.time > 0:
            pygame.draw.circle(self.blackout, (0, 0, 0, 0), self.p1_pos, radius)
            pygame.draw.circle(self.blackout, (0, 0, 0, 0), self.p2_pos, radius)

        if self.closed or self.time > 0:
            surface.blit(self.blackout, (0, 0))

    def update(self, surface, dt):
        self.update_timers(dt)
        self.draw(surface)
