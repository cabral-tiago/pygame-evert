from pygame.surface import Surface
from pygame.rect import Rect
from typing import Tuple


class GameObject:
    def __init__(self, image: Surface) -> None:
        self.x: float = 0.0
        self.y: float = 0.0

        self.__image: Surface = image

    def get_image(self) -> Surface:
        return self.__image
    
    def get_position(self) -> Tuple[int, int]:
        return int(self.x), int(self.y)

    def get_rect(self) -> Rect:
        return self.get_image().get_rect(topleft=self.get_position())

    def get_width(self) -> int:
        return self.get_image().get_width()

    def get_height(self) -> int:
        return self.get_image().get_height()
