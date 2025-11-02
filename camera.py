import pygame

class Camera:
    def __init__(self, width, height):
        self.width = width      # level width in pixels
        self.height = height    # level height in pixels
        self.x = 0
        self.y = 0
