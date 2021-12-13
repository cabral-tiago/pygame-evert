import json
import os
from typing import Tuple
from pygame.surface import Surface
import configs
import pygame


class DialogueCharacter:

    def __init__(self, path: str, start_emotion: str) -> None:
        self.__screen_name: str = ""
        self.__colour: str = "white"
        self.__position: Tuple[int, int] = (0, 0)
        self.__emotions: dict[str, Surface] = {}
        self.__faded_emotions: dict[str, Surface] = {}
        self.__current_emotion: str = start_emotion
        self.__active: bool = False
        
        if path != "":
            with open(path, "r", encoding="utf-8") as file:
                character_data = json.load(file)
                folder = os.path.dirname(path)

                if character_data["screen_name"]:
                    self.__screen_name = character_data["screen_name"]

                if character_data["name_colour"]:
                    self.__colour = character_data["name_colour"]
                
                for emotion in character_data["emotions"]:
                    emotion_path = f"{folder}/{emotion}.png"
                    emotion_surface = pygame.image.load(emotion_path).convert_alpha()
                    if configs.CHARACTER_SIZE[0] != emotion_surface.get_width() or \
                        configs.CHARACTER_SIZE[1] != emotion_surface.get_height():
                        emotion_surface = pygame.transform.smoothscale(emotion_surface, configs.CHARACTER_SIZE)
                    self.__emotions[emotion] = emotion_surface
                    faded = emotion_surface.copy()
                    faded.fill((140, 140, 140), special_flags=pygame.BLEND_RGB_SUB)
                    self.__faded_emotions[emotion] = faded
                
                if character_data["screen_alignment"]:
                    pos_x = 0
                    match character_data["screen_alignment"]:
                        case "left":
                            pos_x = 20
                        case "right":
                            pos_x = configs.SCREEN_W - self.get_width() - 20
                        case "center":
                            pos_x = int(configs.SCREEN_W/2 - self.get_width()/2)

                    self.__position = (pos_x, configs.SCREEN_H - self.get_height())
    
    def set_active(self, emotion: str) -> None:
        self.__active = True
        if emotion != "":
            self.__current_emotion = emotion

    def set_inactive(self) -> None:
        self.__active = False

    def get_name(self) -> str:
        return self.__screen_name

    def get_colour(self) -> str:
        return self.__colour

    def get_image(self) -> Surface:
        if len(self.__emotions) == 0:
            return Surface((0, 0))
        if self.__active:
            return self.__emotions[self.__current_emotion]
        else:
            return self.__faded_emotions[self.__current_emotion]   

    def get_width(self) -> int:
        return configs.CHARACTER_SIZE[0]

    def get_height(self) -> int:
        return configs.CHARACTER_SIZE[1]

    def get_position(self) -> Tuple[int, int]:
        return self.__position

    def get_middle_position(self) -> int:
        return int(self.__position[0] + self.get_width() / 2)
