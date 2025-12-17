import pkgutil
import importlib
import inspect
import src.physics.objects

objects = {}

for _, module_name, _ in pkgutil.iter_modules(src.physics.objects.__path__):
    module = importlib.import_module(f"src.physics.objects.{module_name}")

    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module.__name__:
            objects[name.lower()] = obj

def ObjectFactory(object, *args, **kwargs):
    print(object)
    if object.lower() not in objects:
        raise Exception(f"{object} not loaded in the physics object factory")

    return objects[object.lower()](*args, **kwargs)
