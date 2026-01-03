from src.triggers.triggerobject import Trigger


class ReturnTrigger(Trigger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_interactible = True

    def on_enter(self, player):
        print(type(player).__name__)
        if type(player).__name__ == "Box":
            print('hello')
            player.x = player.original_x
            player.y = player.original_y
