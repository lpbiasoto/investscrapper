
class PEGridElement():
    x = None
    y = None
    value = None

    def __init__(self,x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __str__(self):
        return str(f"x: {self.x}, y: {self.y}, value: {self.value}")