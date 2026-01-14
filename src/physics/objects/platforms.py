from src.physics.physicsobject import PhysicsObject
from src.triggers.triggerobject import ActivatedObject, Trigger


class HorizontalPlatform(PhysicsObject, ActivatedObject):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = 0
        self.vely = -1
        self.trigger_interactible = True
    def on_any_enter(self, player):
        self.vely = 1

class VerticalPlatform(PhysicsObject, ActivatedObject):
    pass
