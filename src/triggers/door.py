from src.triggers.triggerobject import ActivatedObject
from src.physics.physicsobject import PhysicsObject

class Door(PhysicsObject, ActivatedObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = 0
        self.collision = True
        self.pushback_factor = 1

        self.sprites = {
            "closed": "objects/door_closed.png",
            "open": "objects/door_open.png"
        }

        self.set_sprites(self.sprites)

    def on_any_enter(self, player):
        self.change_image("open")
        self.collision = False

    def on_both_leave(self):
        self.change_image("default")
        self.collision = True
