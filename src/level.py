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
        print(self.camera.x)
        print(self.camera.y)

    def draw(self, surface, dt):
        self.level.decorations.draw(surface)
        self.level.collision_tiles.draw(surface)
        self.level.physics_objects.draw(surface)
        self.level.physics_objects.update(self.level, dt)

testlevel = Level("levels/camera.tmx")
# testlevel = 2
