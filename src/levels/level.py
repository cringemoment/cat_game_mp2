import pygame

from src.levels.loadtilemap import load_tilemap
from src.renderer.camera import Camera

class Level:
    def __init__(self, level_path, name = "no title", subtitle = "uh oh"):
        self.level_path = level_path
<<<<<<< Updated upstream
=======
        self.dialogues = self.load_dialogue_file(level_path)
        self.name = name
        self.subtitle = subtitle
>>>>>>> Stashed changes

    def load_window(self, s):
        self.tiles = load_tilemap(s, self, self.level_path)

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

<<<<<<< Updated upstream
testlevel = Level("levels/level_0.tmx")
=======
main_menu = Level("levels/main_menu")
level_0 = Level("levels/decorated_level_0", "Level 0", "Where our friends get their footing back")

levels = {
"level_0": level_0
}
>>>>>>> Stashed changes
