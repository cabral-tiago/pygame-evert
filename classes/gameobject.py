from pygame.surface import Surface
from pygame.rect import Rect
from typing import Tuple


class GameObject:
    def __init__(self, surface: Surface, x: float = 0.0, y: float = 0.0) -> None:
        self.x: float = x
        self.y: float = y
        self.__surface: Surface = surface
    
    def get_surface(self) -> Surface:
        return self.__surface
    
    def get_position(self) -> Tuple[int, int]:
        return int(self.x), int(self.y)

    def get_rect(self) -> Rect:
        return self.get_surface().get_rect(topleft=self.get_position())

    def get_width(self) -> int:
        return self.get_surface().get_width()

    def get_height(self) -> int:
        return self.get_surface().get_height()
