from src.triggers.triggerobject import Trigger


class ReturnTrigger(Trigger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_interactible = True

    def on_any_enter(self, player):
        if type(player).__name__ == "Box":
            player.x = player.original_x
            player.y = player.original_y
