from src.renderer.camera import CameraPos, CameraTrigger
from src.triggers.testbutton import Button

def TriggerFactory(object, **kwargs):
    objects = {
        "CameraTrigger": CameraTrigger,
        "CameraPos": CameraPos,
        "Button": Button
    }

    return objects[object](**kwargs) if object in objects else None
