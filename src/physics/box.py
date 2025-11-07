import pygame

from src.physics.physicsobject import PhysicsObject

class Box(PhysicsObject):
    def __init__(self):
        super().__init__()
        self.collision = True

    def sprite_collision(self, sprite):
        # print("bruh")
        if type(sprite).__name__ == "Bullet":
            print("ow")
            self.vely -= 5
