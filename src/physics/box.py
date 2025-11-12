import pygame

from src.physics.physicsobject import PhysicsObject

class Box(PhysicsObject):
    def __init__(self):
        super().__init__()
        self.collision = True
        self.pushable = True
        self.pushback_factor = 0.001

    def sprite_collision(self, sprite):
        if type(sprite).__name__ == "Bullet":
            self.vely -= 5

class HeavyBox(PhysicsObject):
    def __init__(self):
        super().__init__()
        self.collision = True
        self.pushable = True
        self.pushback_factor = 0.8

    def sprite_collision(self, sprite):
        if type(sprite).__name__ == "Bullet":
            self.vely -= 2
