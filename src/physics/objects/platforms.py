from src.physics.physicsobject import PhysicsObject
from src.triggers.triggerobject import ActivatedObject, Trigger


class HorizontalPlatform(PhysicsObject, ActivatedObject):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = 0
        self.velx = 10
        self.trigger_interactible = True
        self.air_resistance = 0
        self.friction = 0

class VerticalPlatform(PhysicsObject, ActivatedObject):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = 0
        self.vely = 1
        self.trigger_interactible = True
        self.air_resistance = 0
        self.friction = 0
        self.velysave = self.vely

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.vely = self.velysave
    def collide_y(self, obj, iteration):
        super().collide_y(obj, iteration)
        if type(obj).__name__ == "Box" or type(obj).__name__ == "Player":
            if obj.bottom == self.y:
                obj.on_ground = True
                obj.vely = self.velysave - 0.5