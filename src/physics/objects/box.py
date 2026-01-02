import pygame

from src.physics.physicsobject import PhysicsObject

class Box(PhysicsObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collision = True
        self.pushback_factor = 0.001
        self.trigger_interactible = True

    def sprite_collision(self, sprite):
        if type(sprite).__name__ == "Bullet":
            self.vely -= 5

class HeavyBox(PhysicsObject):
    def __init__(self):
        super().__init__()
        self.collision = True
        self.pushback_factor = 0.8

    def sprite_collision(self, sprite):
        if type(sprite).__name__ == "Bullet":
            self.vely -= 2
