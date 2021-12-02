import os
import json
from typing import Tuple
from pygame.rect import Rect
from pygame.surface import Surface
from classes.tileset import Tileset
from classes.levellayer import LevelLayer
import configs
import pygame


class Level:
    def __init__(self, path) -> None:
        self.__layers: list[LevelLayer] = []
        self.__background: Surface = Surface(configs.SCREEN_SIZE, pygame.SRCALPHA)
        self.__obstacles: list[Rect] = []

        # Player
        self.__player_appear: bool = False
        self.__player_spawn: Tuple[int, int] = (0, 0)

        # Camera
        self.__camera_offset: Tuple[int, int] = (0, 0)

        with open(path+"/level_info.json", "r", encoding="utf-8") as file:
            level_info = json.load(file)

            match level_info["type"]:
                case "map":
                    self.__player_appear = level_info["player_appear"]
                    spawn_x, spawn_y = level_info["player_spawn"]
                    spawn_x *= level_info["tile_size"][0] * level_info["tile_scale"]
                    spawn_y *= level_info["tile_size"][1] * level_info["tile_scale"]
                    self.__player_spawn = (spawn_x, spawn_y)

                    tileset = Tileset(level_info["tileset"], level_info["tile_size"], level_info["tile_scale"])

                    layers_path = path + "/layers"
                    layer_files = [f.name for f in os.scandir(layers_path) if f.name.endswith(".csv")]
                    ordered_layers = sorted([(int(i[:-7]), i) for i in layer_files])

                    for _, file in ordered_layers:
                        layer_collide = True if file[:-4].split("_")[1] == "ob" else False
                        layer = LevelLayer(layers_path + "/" + file, layer_collide, tileset)
                        if layer_collide:
                            self.__obstacles.extend(layer.get_obstacle_rects())
                        self.__layers.append(layer)
                
                case "background":
                    if level_info["bg_style"] == "colour":
                        self.__background.fill(level_info["bg_colour"])
                    elif level_info["bg_style"] == "image":
                        self.__background.blit(pygame.image.load(level_info["bg_image"]),(0, 0))

    def get_layer(self, index: int) -> LevelLayer:
        return self.__layers[index]
    
    def get_obstacles(self) -> list[Rect]:
        return self.__obstacles

    def is_player_visible(self) -> bool:
        return self.__player_appear
    
    def get_player_spawn(self) -> Tuple[int, int]:
        return self.__player_spawn
    
    def center_on_player(self, player_rect: Rect) -> None:
        x, y = player_rect.x, player_rect.y
        self.__camera_offset = (configs.SCREEN_W//2 - x, configs.SCREEN_H//2 - y)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.__background, (0, 0))
        for layer in self.__layers:
            screen.blit(layer.get_surface(), self.__camera_offset)