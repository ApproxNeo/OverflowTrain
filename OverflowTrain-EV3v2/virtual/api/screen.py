from virtual.api.element import Element


class Screen:
    def __init__(self, name):
        self.name: str = name
        self.elements: list = []

    def add_element(self, element: Element):
        self.elements.append(element)
        return element

    def render(self, surface):
        for element in self.elements:
            element.render(surface)
