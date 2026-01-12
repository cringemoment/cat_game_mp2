from src.physics.physicsobject import PhysicsObject
from src.triggers.triggerobject import ActivatedObject

class AutoMove(PhysicsObject, ActivatedObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collision = True
        self.gravity = 0
        self.pushback_factor = 1
        self.go = False
        self.dx = 3200
        self.speed = self.dx/60
        self.x -= 30

    def on_trigger(self):
        self.go = True

    def update(self, level, dt):
        super().update(level, dt)

        if not self.dx <= 0:
            self.x += self.speed * dt
            self.dx -= self.speed * dt
