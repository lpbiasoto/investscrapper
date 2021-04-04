import json

class PEGrid:
    elements_list = None

    def __init__(self):
        self.elements_list = []
    
    def __str__(self):
        return str(f"#elements: {len(self.elements_list)}\nelements: {[str(x) for x in self.elements_list]}")

    def add_element(self, grid_element):
        self.elements_list.append(grid_element)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
