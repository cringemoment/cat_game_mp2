import pygame

from src.loadtilemap import load_tilemap
from src.renderer.camera import Camera

class Level:
    def __init__(self, level_path):
        self.level_path = level_path

    def load_window(self, s):
        self.level = load_tilemap(s, self.level_path)

        self.camera = Camera()
        self.camera.set_level(self.level)

    def draw(self, surface, dt):
        self.level.physics_objects.update(self.level, dt)
        self.camera.draw(surface, self.level.physics_objects)
        self.camera.draw(surface, self.level.decorations)
        self.camera.draw(surface, self.level.collision_tiles)
        self.camera.draw(surface, self.level.physics_objects)

testlevel = Level("levels/camera.tmx")
# testlevel = 2
