from typing import Tuple
from pygame.mixer import Sound
from pygame.rect import Rect
from pygame.surface import Surface


class Collectable:
    def __init__(self, image: Surface, position: Tuple[int, int]) -> None:
        self.__image: Surface = image
        self.__position = position
        self.__collected = False
        self.__soundfx: Sound = Sound("assets/sounds/effects/collect.wav")
    
    def get_image(self) -> Surface:
        return self.__image

    def get_rect(self) -> Rect:
        return self.get_image().get_rect(topleft=self.__position)

    def set_collected(self) -> None:
        self.__soundfx.play()
        self.__collected = True

    def is_collected(self) -> bool:
        return self.__collected

    def reset(self) -> None:
        self.__collected = False
