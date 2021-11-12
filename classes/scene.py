from pygame.surface import Surface
from classes.gameobject import GameObject


class Scene:
    def __init__(self) -> None:
        self.objects: list[GameObject] = []

    def draw(self, screen: Surface) -> None:
        for object in self.objects:
            screen.blit(object.get_surface(), object.get_position())
