from classes.gameobject import GameObject
from classes.scene import Scene
from pygame.surface import Surface


class World(Scene):
    def __init__(self) -> None:
        super().__init__()

        placeholder_surface = Surface((100,100))
        placeholder_surface.fill("white")
        placeholder_object = GameObject(placeholder_surface, 10, 10)
        self.objects.append(placeholder_object)