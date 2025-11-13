import pygame

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.positions = []

    def set_level(self, level):
        self.positions = level.camera_positions
        print(self.positions)
        self.x, self.y = 1, 1
