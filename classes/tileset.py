from typing import Tuple
import pygame
from pygame.surface import Surface


class Tileset:
    def __init__(self, path: str, tile_size: Tuple[int, int]) -> None:
        self.__original_image = pygame.image.load(path)
        self.__tiles: list[Surface] = []

        columns = self.__original_image.get_width() // tile_size[0]
        rows = self.__original_image.get_height() // tile_size[1]
        for r in range(rows):
            for c in range(columns):
                position = (tile_size[0] * c, tile_size[1] * r)
                self.__tiles.append(self.__original_image.subsurface(pygame.Rect(position, tile_size)))
    
    def get_tile(self, index: int) -> Surface:
        return self.__tiles[index]