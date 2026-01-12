from src.physics.physicsobject import PhysicsObject

class Box(PhysicsObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collision = True
        self.pushback_factor = 0.001
        self.trigger_interactible = True
        self.original_x = None
        self.original_y = None

    def sprite_collision(self, sprite):
        if type(sprite).__name__ == "Bullet":
            self.vely -= 5

    def update(self, *args):
        super().update(*args)
        if self.original_x is None:
            self.original_x = self.x
            self.original_y = self.y

class HeavyBox(PhysicsObject):
    def __init__(self):
        super().__init__()
        self.collision = True
        self.pushback_factor = 0.8

    def sprite_collision(self, sprite):
        if type(sprite).__name__ == "Bullet":
            self.vely -= 2
