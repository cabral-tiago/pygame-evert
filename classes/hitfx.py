from typing import Tuple
from pygame.rect import Rect
from pygame.surface import Surface


class HitFX:
    DURATION = 0.5

    def __init__(self, surface: Surface, center: Tuple[int, int]) -> None:
        self.__surface = surface
        self.__position = center
        self.__time = self.DURATION

    def get_surface(self) -> Surface:
        return self.__surface

    def get_rect(self) -> Rect:
        return self.__surface.get_rect(center=self.__position)

    def is_alive(self) -> bool:
        return self.__time > 0
    
    def update(self, dt: float) -> None:
        self.__time -= dt
