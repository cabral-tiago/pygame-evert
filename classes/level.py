import os
import json
from pygame.surface import Surface
from classes.tileset import Tileset
from classes.levellayer import LevelLayer
import configs
import pygame


class Level:
    def __init__(self, path) -> None:
        self.__layers: list[LevelLayer] = []
        self.__background: Surface = Surface(configs.SCREEN_SIZE, pygame.SRCALPHA)

        with open(path+"/level_info.json", "r", encoding="utf-8") as file:
            level_info = json.load(file)

            match level_info["type"]:
                case "map":
                    tileset = Tileset(level_info["tileset"], level_info["tile_size"], level_info["tile_scale"])

                    layers_path = path + "/layers"
                    layer_files = [f.name for f in os.scandir(layers_path) if f.name.endswith(".csv")]
                    ordered_layers = sorted([(int(i[:-7]), i) for i in layer_files])

                    for _, file in ordered_layers:
                        layer_collide = True if file[:-4].split("_")[1] == "ob" else False
                        layer = LevelLayer(layers_path + "/" + file, layer_collide, tileset)
                        self.__layers.append(layer)
                
                case "background":
                    if level_info["bg_style"] == "colour":
                        self.__background.fill(level_info["bg_colour"])
                    elif level_info["bg_style"] == "image":
                        self.__background.blit(pygame.image.load(level_info["bg_image"]),(0, 0))

    def get_layer(self, index: int) -> LevelLayer:
        return self.__layers[index]

    def draw(self, screen: Surface) -> None:
        screen.blit(self.__background, (0, 0))
        for layer in self.__layers:
            screen.blit(layer.get_surface(), (0, 0))