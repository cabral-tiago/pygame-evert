import os
import json
from typing import Tuple
from pygame.rect import Rect
from pygame.surface import Surface
from classes.dialoguecharacter import DialogueCharacter
from classes.dialogueline import DialogueLine
from classes.tileset import Tileset
from classes.levellayer import LevelLayer
from classes.enums import LevelType
import configs
import pygame


class Level:
    def __init__(self, path) -> None:
        self.__type: LevelType = LevelType.BLANK
        self.__layers: list[LevelLayer] = []
        self.__background: Surface = Surface(configs.SCREEN_SIZE, pygame.SRCALPHA)
        self.__obstacles: list[Rect] = []

        # Player
        self.__player_appear: bool = False
        self.__player_spawn: Tuple[int, int] = (0, 0)

        # Camera
        self.__camera_offset: Tuple[int, int] = (0, 0)

        # Dialogue characters
        self.__dialogue_lines: list[DialogueLine] = []

        with open(path+"/level_info.json", "r", encoding="utf-8") as file:
            level_info = json.load(file)

            self.__type = LevelType(level_info["type"])
            match self.__type:
                case LevelType.BLANK:
                    self.__background.fill("black")
                
                case LevelType.MAP:
                    self.__load_map(level_info, path)
                
                case LevelType.DIALOGUE:
                    self.__load_dialogue(level_info, path)
    
    def __load_map(self, level_info, path) -> None:
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

    def __load_dialogue(self, level_info, path) -> None:
        if level_info["bg_style"] == "colour":
            self.__background.fill(level_info["bg_colour"])
        elif level_info["bg_style"] == "image":
            image: Surface = pygame.image.load(level_info["bg_image"])
            if image.get_width() > configs.SCREEN_W:
                scale = configs.SCREEN_W / image.get_width()
                scaled_height = int(image.get_height() * scale)
                if level_info["bg_smooth_scale"]:
                    image = pygame.transform.smoothscale(image, (configs.SCREEN_W, scaled_height))
                else:
                    image = pygame.transform.scale(image, (configs.SCREEN_W, scaled_height))

            self.__background.blit(image,(0, 0))

        dialogue_characters: dict[str, DialogueCharacter] = {}
        dialogue_characters[""] = DialogueCharacter("")  # Narrator
        for character in level_info["characters"]:
            dialogue_characters[character] = DialogueCharacter(level_info["characters"][character])
        
        with open(path+"/dialogue.json", "r", encoding="utf-8") as file:
            dialogue_data = json.load(file)

            for line in dialogue_data["dialogue"]:
                for character in line:
                    dialogue_character = dialogue_characters[character]
                    self.__dialogue_lines.append(DialogueLine(dialogue_character, line[character]))

    def get_type(self) -> LevelType:
        return self.__type

    def __get_layer(self, index: int) -> LevelLayer:
        return self.__layers[index]

    def get_width(self) -> int:
        if self.__type == LevelType.MAP:
            return self.__get_layer(0).get_surface().get_width()
        else:
            return self.__background.get_width()

    def get_height(self) -> int:
        if self.__type == LevelType.MAP:
            return self.__get_layer(0).get_surface().get_height()
        else:
            return self.__background.get_height()
    
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