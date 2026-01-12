import pygame
import importlib

from src.levels.loadtilemap import load_tilemap
from src.renderer.camera import Camera

class Level:
    def __init__(self, level_path, name = "no title", subtitle = "uh oh", music = None):
        self.level_path = level_path
        self.dialogues = self.load_dialogue_file(level_path)
        self.name = name
        self.subtitle = subtitle
        self.bg_music = music

    def load_dialogue_file(self, file_path):
        spec = importlib.util.spec_from_file_location("asdkjalkdhdkgjas", f"{file_path}/dialogue.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.dialogues

    def load_game(self, game):
        s = game.window
        self.game = game
        self.tiles = load_tilemap(s, self, f"{self.level_path}/tilemap.tmx")

        self.camera = Camera()
        self.camera.set_level(self.tiles)

    def draw(self, surface):
        objects = []

        groups = [
            self.tiles.physics_objects,
            self.tiles.decorations,
            self.tiles.collision_tiles,
            self.tiles.physics_objects,
            self.tiles.area_triggers
        ]

        for group in groups:
            for obj in group:
                if hasattr(obj, "z"):
                    z = obj.z
                elif hasattr(obj, "properties") and "z" in obj.properties:
                    z = obj.properties["z"]
                else:
                    z = 0

                objects.append((z, obj))

        objects.sort(key=lambda t: t[0])

        for _, obj in objects:
            self.camera.draw(surface, [obj])

    def update_physics(self, dt):
        self.tiles.physics_objects.update(self, dt)
        self.camera.update_timers(dt)

        for trigger in self.tiles.area_triggers:
            trigger.update_players()

main_menu = Level("levels/__main_menu", "", "")
level_0 = Level("levels/level_0", "Level 0", "1-800-HOW-PLAY", "level0_bg")
level_1 = Level("levels/level_1", "Level 1", "569-GET-FILE")
train_station = Level("levels/train_station", "Level 2", "OFF-THE-RAIL")
train_level = Level("levels/level_2")

levels = {
"main_menu": main_menu,
"level_0": level_0,
"level_1": level_1,
"level_2": train_station,
"train_level": train_level,
"level_3": level_1,
}

phonebook_levels = {
    "level_0": level_0,
    "level_1": level_1,
    "level_2": train_station,
    "level_3": level_1,
}
