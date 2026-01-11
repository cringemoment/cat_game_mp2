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
    def __init__(self, name, rect, level, image = None, properties = {}):
        self.name = name
        self.players_inside = [False, False]
        self.sprites_inside = []
        self.rect = rect
        self.level = level
        self.image = image
        self.object_interactible = False
        self.properties = properties

    @call_triggers
    def on_trigger(self):
        pass

    @call_triggers
    def on_leave(self, player):
        pass

    @call_triggers
    def on_any_enter(self, player):
        pass

    @call_triggers
    def on_enter(self, player):
        pass

    @call_triggers
    def on_both_leave(self):
        pass

    #helper method for select
    def select(self, player):
        if self.players_inside[player.index]:
            self.on_select(player)

    @call_triggers
    def on_select(self, player):
        pass

    def update_players(self):
        for sprite in self.level.tiles.physics_objects:

            #player interactions
            if type(sprite).__name__ == "Player" and not self.object_interactible:
                if self.rect.colliderect(sprite.rect):
                    if not self.players_inside[sprite.index]:
                        self.players_inside[sprite.index] = True
                        self.on_enter(sprite)

                        if not all(self.players_inside):
                            self.on_any_enter(sprite)

                else:
                    if self.players_inside[sprite.index]:
                        self.players_inside[sprite.index] = False
                        self.on_leave(sprite)

                        if sum(self.players_inside) == 0:
                            self.on_both_leave()

            #interactions with interactible objects
            if not self.object_interactible: continue
            if not sprite.trigger_interactible: continue

            if self.rect.colliderect(sprite.rect):
                if not sprite in self.sprites_inside:
                    self.on_enter(sprite)
                    if self.sprites_inside == []:
                        self.on_any_enter(sprite)

                    self.sprites_inside.append(sprite)

            else:
                if sprite in self.sprites_inside:
                    self.sprites_inside.remove(sprite)
                    self.on_leave(sprite)
                    if self.sprites_inside == []:
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

    def on_any_enter(self, player):
        pass

    def on_leave(self, player):
        pass

    def on_both_leave(self):
        pass

    def on_select(self, playerj):
        pass
