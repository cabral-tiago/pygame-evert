from pygame.surface import Surface
from classes.gameobject import GameObject


class Scene:
    def __init__(self) -> None:
        self.z_index: int = 0
        self.visible: bool = False
        self.objects: list[GameObject] = []

    def draw(self, screen: Surface) -> None:
        if self.visible:
            for object in self.objects:
                screen.blit(object.get_image(), object.get_position())
