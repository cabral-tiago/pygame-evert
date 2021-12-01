from pygame.rect import Rect
from classes.tileset import Tileset
from pygame.surface import Surface
import pygame


class LevelLayer:
    def __init__(self, path: str, collide: bool, tileset: Tileset) -> None:
        self.__map: list[list[int]] = []
        self.__collide = collide
        self.__tileset = tileset
        self.__rects: list[Rect] = []

        with open(path, "r", encoding="utf-8") as file:
            line = file.readline().strip()
            while line != "":
                row = [int(n) for n in line.split(",")]
                self.__map.append(row)
                line = file.readline().strip()

        tile_w = tileset.get_tile(0).get_width()
        tile_h = tileset.get_tile(0).get_height()

        width = len(self.__map[0])
        height = len(self.__map)
        self.__surface: Surface = Surface((width * tile_w, height * tile_h), pygame.SRCALPHA)

        for h, row in enumerate(self.__map):
            for w, column in enumerate(row):
                if column != -1:
                    self.__rects.append(Rect(w * tile_w, h * tile_h, tile_w, tile_h))
                    self.__surface.blit(self.__tileset.get_tile(column), (w * tile_w, h * tile_h))

    def is_obstacle(self) -> bool:
        return self.__collide

    def get_obstacle_rects(self) -> list[Rect]:
        return self.__rects
        
    def get_surface(self) -> Surface:
        return self.__surface
