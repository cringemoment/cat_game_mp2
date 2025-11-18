import pygame

from src.loadtilemap import load_tilemap
from src.renderer.camera import Camera

class Level:
    def __init__(self, level_path):
        self.level_path = level_path

    def load_window(self, s):
        self.tiles = load_tilemap(s, self, self.level_path)

        self.camera = Camera()
        self.camera.set_level(self.tiles)

    def draw(self, surface, dt):
        self.tiles.physics_objects.update(self, dt)
        self.camera.draw(surface, self.tiles.physics_objects)
        self.camera.draw(surface, self.tiles.decorations)
        self.camera.draw(surface, self.tiles.collision_tiles)
        self.camera.draw(surface, self.tiles.physics_objects)
        self.camera.draw(surface, self.tiles.area_triggers)

        for trigger in self.tiles.area_triggers:
            trigger.update_players()

testlevel = Level("levels/camera.tmx")
# testlevel = 2
