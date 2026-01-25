from src.physics.physicsobject import PhysicsObject

class Stationary(PhysicsObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collision = True
        self.pushback_factor = 1
        self.trigger_interactible = False

class Intangible(PhysicsObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collision = False
        self.trigger_interactible = False
        self.gravity = 0
