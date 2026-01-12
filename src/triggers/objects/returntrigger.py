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
        self.test = False

    def on_trigger(self):
        print("hello")
        self.test = True

    def on_any_enter(self, player):
        if type(player).__name__ == "Player" and self.test:
            player.x = float(self.properties["return_x"])
            player.y = float(self.properties["return_y"])
