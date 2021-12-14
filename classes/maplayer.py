from pygame.rect import Rect
from classes.tileset import Tileset
from pygame.surface import Surface
import pygame


class MapLayer:
    def __init__(self, path: str, obstacle: bool, tileset: Tileset) -> None:
        map: list[list[int]] = []
        self.__tileset = tileset
        self.__obstacle_rects: list[Rect] = []

        with open(path, "r", encoding="utf-8") as file:
            line = file.readline().strip()
            while line != "":
                row = [int(n) for n in line.split(",")]
                map.append(row)
                line = file.readline().strip()

        tile_w = tileset.get_tile(0).get_width()
        tile_h = tileset.get_tile(0).get_height()

        width = len(map[0])
        height = len(map)
        self.__surface: Surface = Surface((width * tile_w, height * tile_h), pygame.SRCALPHA)
        
        # List of Rows with Lists of Groups with List of Columns.
        # Used for compressing neighbour obstacle Rects into bigger Rects, massively reducing the number of Rects needed.
        obstacles: list[list[list[int]]] = []
        for h, row in enumerate(map):
            obstacle_row = []
            for w, column in enumerate(row):
                if column != -1:
                    self.__surface.blit(self.__tileset.get_tile(column), (w * tile_w, h * tile_h))
                    if obstacle:
                        obstacle_row.append(w)
            if obstacle:
                new_row = []
                subList = []
                prev_n = -1

                for n in obstacle_row:
                    if prev_n+1 != n:
                        if subList:
                            new_row.append(subList)
                            subList = []
                    subList.append(n)
                    prev_n = n

                if subList:
                    new_row.append(subList)
                obstacles.append(new_row)
        
        for y, line in enumerate(obstacles):
            for group in line:
                self.__obstacle_rects.append(Rect(group[0] * tile_w, y * tile_h, len(group) * tile_w, tile_h))

    def get_obstacle_rects(self) -> list[Rect]:
        return self.__obstacle_rects
        
    def get_surface(self) -> Surface:
        return self.__surface
