from src.physics.physicsobject import PhysicsObject
from src.triggers.triggerobject import ActivatedObject, Trigger


class HorizontalPlatform(PhysicsObject, ActivatedObject):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = 0
        self.velx = 0
        self.trigger_interactible = True
        self.air_resistance = 0
        self.friction = 0

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if self.velx == 0:
            self.velx = int(self.properties["speed"])

class VerticalPlatform(PhysicsObject, ActivatedObject):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = 0
        self.vely = 0
        self.trigger_interactible = True
        self.air_resistance = 0
        self.friction = 0
        self.velysave = 0

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if self.vely == 0 and self.velysave == 0:
            self.vely = int(self.properties["speed"])
            self.velysave = self.vely
        self.vely = self.velysave
    def collide_y(self, obj, iteration):
        super().collide_y(obj, iteration)
        if type(obj).__name__ == "Box" or type(obj).__name__ == "Player":
            if obj.bottom == self.y:
                obj.on_ground = True
                obj.vely = self.velysave - 0.5

class UpPlatform(PhysicsObject, ActivatedObject):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = 0
        self.vely = 0
        self.trigger_interactible = True
        self.air_resistance = 0
        self.friction = 0
        self.velysave = self.vely
        self.original_y = None

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if self.original_y == None:
            self.original_y = self.y
        self.vely = self.velysave if self.y > self.original_y-(int(self.properties["max_height"])*32) else 0

    def collide_y(self, obj, iteration):
        super().collide_y(obj, iteration)
        if self.original_y != None:
            self.vely = self.velysave if self.y > self.original_y - (int(self.properties["max_height"]) * 32) else 0
        if type(obj).__name__ == "Box" or type(obj).__name__ == "Player":
            if obj.bottom == self.y and self.vely != 0:
                obj.on_ground = True
                obj.vely = self.velysave - 0.5 if self.velysave < 0 else 0

    def on_any_enter(self, player):
        self.gravity = 0
        self.velysave = int(self.properties["speed"])

    def on_both_leave(self):
        self.gravity = -self.velysave
        self.velysave = 0