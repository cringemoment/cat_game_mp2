from src.triggers.triggerobject import Trigger, ActivatedObject


class ReturnTrigger(Trigger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_interactible = True

    def on_any_enter(self, player):
        if type(player).__name__ == "Box":
            player.x = player.original_x
            player.y = player.original_y

class ReturnTriggerWall(Trigger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_interactible = True

    def on_any_enter(self, player):
        if type(player).__name__ == "Box":
            if player.left > self.rect.x:
                player.x += 40
            else:
                player.x -= 40

class ReturnPlayerTrigger(ActivatedObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self, player):

        if type(player).__name__ == "Player":
            if player.room == self.properties["room"]:
                player.x = self.x
                player.y = self.y

class RoomChange(Trigger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_trigger(self):
        self.players_inside[0].room = self.properties["room"]
        self.players_inside[1].room = self.properties["room"]
