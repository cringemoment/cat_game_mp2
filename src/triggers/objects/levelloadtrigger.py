from src.triggers.triggerobject import Trigger

class LevelLoad(Trigger):
    def on_trigger(self):
        self.players_inside[0].level.game.load_level(self.properties["level_name"])
