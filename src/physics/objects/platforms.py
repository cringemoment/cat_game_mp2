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
    pass
