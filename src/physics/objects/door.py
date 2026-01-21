from src.triggers.triggerobject import ActivatedObject
from src.physics.physicsobject import PhysicsObject

class Door(PhysicsObject, ActivatedObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = 0
        self.collision = True
        self.pushback_factor = 1
        self.test = True

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if self.test:
            self.test = False
            self.load_color()


    def load_color(self):
        #color = getattr(self.properties, "color", "red")
        color = self.properties["color"]

        sprites = {
            "closed": f"objects/door_{color}.png",
            "open": f"objects/open_door_{color}.png"
        }

        self.set_sprites(sprites)

    def on_any_enter(self, player):
        self.change_image("open")
        self.collision = False
        self.level.game.sound_handler.play_sound("door_open")

    def on_both_leave(self):
        self.change_image("closed")
        self.collision = True
        self.level.game.sound_handler.play_sound("door_close")

class ReverseDoor(PhysicsObject, ActivatedObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = 0
        self.collision = False
        self.pushback_factor = 1
        self.test = True

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if self.test:
            self.test = False
            self.load_color()

    def load_color(self):
        #color = getattr(self.properties, "color", "red")
        color = self.properties["color"]
        sprites = {
            "closed": f"objects/door_{color}.png",
            "open": f"objects/open_door_{color}.png"
        }
        self.set_sprites(sprites)

    def on_any_enter(self, player):
        self.change_image("closed")
        self.collision = True

    def on_both_leave(self):
        self.change_image("open")
        self.collision = False

class ReverseTrapDoor(PhysicsObject, ActivatedObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = 0
        self.collision = False
        self.pushback_factor = 1
        self.test = True

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if self.test:
            self.test = False
            self.load_color()


    def load_color(self):
        #color = getattr(self.properties, "color", "red")
        color = self.properties["color"]

        sprites = {
            "closed": f"objects/trapdoor_{color}.png",
            "open": f"objects/open_trapdoor_{color}.png"
        }

        self.set_sprites(sprites)

    def on_any_enter(self, player):
        self.change_image("closed")
        self.collision = True

    def on_both_leave(self):
        self.change_image("open")
        self.collision = False

class TrapDoor(PhysicsObject, ActivatedObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = 0
        self.collision = True
        self.pushback_factor = 1
        self.test = True

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if self.test:
            self.test = False
            self.load_color()


    def load_color(self):
        #color = getattr(self.properties, "color", "red")
        color = self.properties["color"]

        sprites = {
            "closed": f"objects/trapdoor_{color}.png",
            "open": f"objects/open_trapdoor_{color}.png"
        }

        self.set_sprites(sprites)

    def on_any_enter(self, player):
        self.change_image("open")
        self.collision = False

    def on_both_leave(self):
        self.change_image("closed")
        self.collision = True
