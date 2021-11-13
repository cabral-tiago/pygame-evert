from pygame.surface import Surface
from classes.button import Button
from classes.gameobject import GameObject


class Scene:
    def __init__(self) -> None:
        self.objects: list[GameObject] = []
        self.buttons: list[Button] = []

    def draw(self, screen: Surface) -> None:
        for object in self.objects:
            screen.blit(object.get_surface(), object.get_position())
        for button in self.buttons:
            screen.blit(button.get_surface(), button.get_position())
