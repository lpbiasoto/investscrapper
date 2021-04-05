import json

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

    def to_JSON(self):
        return json.dumps(self, cls=MyEncoder)

    def to_dict(self):
        dict = {}
        return {"x": self.x, "y": self.y, "value":self.value}

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, PEGridElement):
            return super(MyEncoder, self).default(obj)

        return obj.__dict__
