from typing import Tuple
import pygame
from pygame.surface import Surface
from classes.enums import Direction


class Spritesheet:
    def __init__(self, path: str, sprite_size: Tuple[int, int], scale: int) -> None:
        image = pygame.image.load(path).convert_alpha()
        image_w, image_h = image.get_width() * scale, image.get_height() * scale
        self.__image = pygame.transform.scale(image, (image_w, image_h))
        self.__sprite_size = (sprite_size[0] * scale, sprite_size[1] * scale)

        columns = self.__image.get_width() // self.__sprite_size[0]
        rows = self.__image.get_height() // self.__sprite_size[1]
        
        self.__sprite_rows: list[list[Surface]] = []
        for r in range(rows):
            row: list[Surface] = []

            for c in range(columns):
                position = (self.__sprite_size[0] * c, self.__sprite_size[1] * r)
                row.append(self.__image.subsurface(pygame.Rect(position, self.__sprite_size)))
            
            self.__sprite_rows.append(row)
    
    def get_dictionary(self, ordered_positions: list[Direction]) -> dict[Direction, list[Surface]]:
        dictionary = {}
        for n, row in enumerate(self.__sprite_rows):
            dictionary[ordered_positions[n]] = row
        return dictionary