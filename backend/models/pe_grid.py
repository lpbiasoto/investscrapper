import json

class PEGrid:
    elements_list = None

    def __init__(self):
        self.elements_list = []
    
    def __str__(self):
        return str(f"#elements: {len(self.elements_list)}, elements: {[str(x) for x in self.elements_list]}")

    def add_element(self, grid_element):
        self.elements_list.append(grid_element)

    def get_elements_list(self):
        return self.elements_list
