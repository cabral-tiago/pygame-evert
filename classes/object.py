from typing import Tuple
from pygame.rect import Rect
from pygame.surface import Surface
import pygame


class Object:
    def __init__(self, image: Surface, scale: int, position: Tuple[int, int],
                 world_scale: int, tile_scale: Tuple[int, int]) -> None:
        self.__image: Surface = image
        self.__position = position[0] * tile_scale[0], position[1] * tile_scale[1]
        self.__collected = False

        if scale != 1:
            size_x = self.__image.get_width()
            size_y = self.__image.get_height()
            self.__image = pygame.transform.scale(self.__image, (size_x * scale, size_y * scale))

        if world_scale != 1:
            pos_x, pos_y = self.__position
            self.__position = (pos_x * world_scale, pos_y * world_scale)
    
    def get_image(self) -> Surface:
        return self.__image

    def get_rect(self) -> Rect:
        return self.get_image().get_rect(topleft=self.__position)

    def collect(self) -> None:
        self.__collected = True

    def is_collected(self) -> bool:
        return self.__collected
