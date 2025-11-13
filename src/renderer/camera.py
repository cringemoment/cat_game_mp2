import pygame

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.positions = {}
        self.width = 30
        self.height = 20

    def set_level(self, level):
        self.positions = level.camera_positions
        if "default" in self.positions:
            self.x, self.y = self.positions["default"]["x"], self.positions["default"]["y"]
            self.width, self.height = self.positions["default"]["width"], self.positions["default"]["height"]

    def draw(self, surface, group):
        screen_width, screen_height = surface.get_size()

        tile_width = screen_width / self.width
        tile_height = screen_height / self.height
        tile_size = min(tile_width, tile_height)

        offset = pygame.Vector2(self.x, self.y)

        for sprite in group:
            world_pos = pygame.Vector2(sprite.rect.topleft - offset)

            screen_pos = (world_pos.x * (tile_size / 32), world_pos.y * (tile_size / 32))  # assuming original tile size = 32

            scale_factor = tile_size / 32
            scaled_image = pygame.transform.scale(sprite.image, (int(sprite.rect.width * scale_factor), int(sprite.rect.height * scale_factor)))

            surface.blit(scaled_image, screen_pos)
