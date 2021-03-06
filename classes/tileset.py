from typing import Tuple
import pygame
from pygame.surface import Surface


class Tileset:
    def __init__(self, path: str, tile_size: Tuple[int, int], scale: int) -> None:
        image = pygame.image.load(path).convert()
        image_alpha = pygame.image.load(path).convert_alpha()
        image_w, image_h = image.get_width() * scale, image.get_height() * scale
        self.__image = pygame.transform.scale(image, (image_w, image_h))
        self.__image_alpha = pygame.transform.scale(image_alpha, (image_w, image_h))
        self.__tile_size = (tile_size[0] * scale, tile_size[1] * scale)
        self.__tiles: list[Surface] = []
        self.__tiles_alpha: list[Surface] = []

        columns = self.__image.get_width() // self.__tile_size[0]
        rows = self.__image.get_height() // self.__tile_size[1]
        for r in range(rows):
            for c in range(columns):
                position = (self.__tile_size[0] * c, self.__tile_size[1] * r)
                self.__tiles.append(self.__image.subsurface(pygame.Rect(position, self.__tile_size)))
                self.__tiles_alpha.append(self.__image_alpha.subsurface(pygame.Rect(position, self.__tile_size)))
    
    def get_tile(self, index: int, alpha: bool = True) -> Surface:
        if alpha:
            return self.__tiles_alpha[index]
        return self.__tiles[index]