import pygame

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.level = None
        self.positions = []

    def set_level(self, level):
        self.level = level
        
