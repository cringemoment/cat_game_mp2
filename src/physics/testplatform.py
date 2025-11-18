from src.physics.physicsobject import PhysicsObject
from src.triggers.triggerobject import ActivatedObject

class Platform(PhysicsObject, ActivatedObject):
    def __init__(self):
        super().__init__()
        sprites = {
            "gone": "objects/platform_gone.png"
        }

        self.set_sprites(sprites)

        self.pushback_factor = 1
        self.collision = True
        self.gravity = 0

    def on_enter(self, player):
        self.change_image("gone")
        self.collision = False

    def on_both_leave(self):
        self.change_image("default")
        self.collision = True
