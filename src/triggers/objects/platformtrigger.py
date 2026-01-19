from src.triggers.triggerobject import Trigger

class PlatformTrigger(Trigger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_interactible = True

    def on_enter(self, player):
        if type(player).__name__ == "HorizontalPlatform":
            player.velx = player.velx * -1
        elif type(player).__name__ == "VerticalPlatform":
            player.vely = player.vely * -1
            player.velysave = player.vely
        elif type(player).__name__ == "UpPlatform":
            player.vely = 0
