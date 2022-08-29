import time

def add_hours(hours: int, origin: int = None):
    origin = origin if origin is not None else round(time.time())
    return origin + hours * 60 * 60