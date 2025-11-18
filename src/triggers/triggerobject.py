import pygame

def call_triggers(f):
    def w(self, *args, **kwargs):
        allobjs = self.level.tiles.activated_objects
        allobjs.extend(self.level.tiles.physics_objects)
        for obj in self.level.tiles.activated_objects:
            if obj.name == self.name:
                method = getattr(obj, f.__name__)
                method(*args, **kwargs)
    return w

class Trigger:
    def __init__(self, name, rect, level, image = None):
        self.name = name
        self.players_inside = [False, False]
        self.rect = rect
        self.level = level
        self.image = image

    @call_triggers
    def on_trigger(self):
        pass

    @call_triggers
    def on_leave(self, player):
        pass

    @call_triggers
    def on_enter(self, player):
        pass

    @call_triggers
    def on_both_leave(self):
        pass

    def update_players(self):
        for sprite in self.level.tiles.physics_objects:
            if type(sprite).__name__ == "Player":
                if self.rect.colliderect(sprite.rect):
                    if not self.players_inside[sprite.index]:
                        self.players_inside[sprite.index] = True
                        self.on_enter(sprite)

                else:
                    if self.players_inside[sprite.index]:
                        self.players_inside[sprite.index] = False
                        self.on_leave(sprite)

                        if sum(self.players_inside) == 0:
                            self.on_both_leave()

        if sum(self.players_inside) == 2:
            self.on_trigger()

class ActivatedObject:
    def __init__(self, name, x, y, level, properties):
        self.name = name
        self.x = x
        self.y = y
        self.level = level
        self.properties = properties

    def on_trigger(self):
        pass

    def on_enter(self, player):
        pass

    def on_leave(self, player):
        pass

    def on_both_leave(self):
        pass
