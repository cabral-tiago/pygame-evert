import os
import pygame
from pygame.surface import Surface
from classes.tileset import Tileset


class LevelLayer:
    def __init__(self, path: str, collide: bool, tileset: Tileset) -> None:
        self.__map: list[list[int]] = []
        self.__collide = collide  # TODO: Implement properly the obstacle layers
        self.__tileset = tileset

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
                    self.__surface.blit(self.__tileset.get_tile(column), (w * tile_w, h * tile_h))

    def is_obstacle(self) -> bool:
        return self.__collide

    def get_surface(self) -> Surface:
        return self.__surface


class Level:
    def __init__(self, path) -> None:
        with open(path+"/tileset_info.csv", "r", encoding="utf-8") as file:
            tileset_path = file.readline().strip()
            tile_w, tile_h = [int(x.strip()) for x in file.readline().strip().split(",")]
            tileset_scale = int(file.readline().strip())

        self.__tileset = Tileset(tileset_path, (tile_w, tile_h), tileset_scale)
        self.__tileset_scale = tileset_scale

        layers_path = path + "/layers"
        layer_files = [f.name for f in os.scandir(layers_path) if f.name.endswith(".csv")]
        ordered_layers = sorted([(int(i[:-7]), i) for i in layer_files])

        self.__layers: list[LevelLayer] = []

        for _, file in ordered_layers:
            layer_collide = True if file[:-4].split("_")[1] == "ob" else False
            layer = LevelLayer(layers_path + "/" + file, layer_collide, self.__tileset)
            self.__layers.append(layer)

    def get_layer(self, index: int) -> LevelLayer:
        return self.__layers[index]

    def draw(self, screen: Surface) -> None:
        for layer in self.__layers:
            screen.blit(layer.get_surface(), (0, 0))