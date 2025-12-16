from src.triggers.triggerobject import Trigger, ActivatedObject

class CameraPos(ActivatedObject):
    def on_trigger(self):
        speed_ms = float(self.properties.get("speed_ms", 0.1))

        self.level.camera.transition_to(
            self.x,
            self.y,
            int(self.properties["screen_width"]),
            speed_ms
        )

class CameraTrigger(Trigger):
    pass
