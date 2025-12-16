import pygame

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 30
        self.height = 20

        # transition
        self.transition_time = 0
        self.transition_total = 0
        self.start_x = 0
        self.start_y = 0
        self.start_width = 0
        self.target_x = 0
        self.target_y = 0
        self.target_width = 0

    def set_level(self, level):
        self.positions = {}

        for obj in level.activated_objects:
            if type(obj).__name__ == "CameraPos":
                self.positions[obj.name] = obj

        self.x, self.y = self.positions["default"].x, self.positions["default"].y
        self.width = int(self.positions["default"].properties["screen_width"])
        self.height = int(self.positions["default"].properties.get("screen_height", self.width * 2/3))

    def transition_to(self, newx, newy, newwidth, speed_ms_ms):
        self.start_x = self.x
        self.start_y = self.y
        self.start_width = self.width

        self.target_x = newx
        self.target_y = newy
        self.target_width = newwidth

        self.transition_total = speed_ms_ms
        self.transition_time = speed_ms_ms

    def update_timers(self, dt):
        if self.transition_time > 0:
            self.transition_time = max(self.transition_time - dt, 0)

            t = 1 - (self.transition_time / self.transition_total)

            self.x = self.start_x + (self.target_x - self.start_x) * t
            self.y = self.start_y + (self.target_y - self.start_y) * t
            self.width = self.start_width + (self.target_width - self.start_width) * t

    def draw(self, surface, group):
        screen_width, screen_height = surface.get_size()

        tile_size = screen_width / self.width #will always use the width for the size so that it fills horizontally

        offset = pygame.Vector2(self.x, self.y)

        for sprite in group:
            if not getattr(sprite, "image", None):
                continue

            world_pos = pygame.Vector2(sprite.rect.topleft - offset)

            screen_pos = (world_pos.x * (tile_size / 32), world_pos.y * (tile_size / 32))  #assuming original tile size = 32

            scale_factor = tile_size / 32
            scaled_image = pygame.transform.scale(sprite.image, (int(sprite.rect.width * scale_factor), int(sprite.rect.height * scale_factor)))

            surface.blit(scaled_image, screen_pos)
