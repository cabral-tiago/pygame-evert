import json
from typing import Tuple
from pygame.surface import Surface
import configs
import pygame


class DialogueCharacter:

    def __init__(self, path: str, start_emotion: str) -> None:
        self.__screen_name: str = ""
        self.__position: Tuple[int, int] = (0, 0)
        self.__emotions: dict[str, Surface] = {}
        self.__last_emotion: str = start_emotion
        self.__active: bool = False
        
        if path != "":
            with open(path, "r", encoding="utf-8") as file:
                character_data = json.load(file)

                if character_data["screen_name"]:
                    self.__screen_name = character_data["screen_name"]
                
                for emotion in character_data["emotions"]:
                    emotion_path = f"{path[:-5]}_{emotion}.png"
                    emotion_surface = pygame.image.load(emotion_path)
                    if configs.CHARACTER_SIZE[0] != emotion_surface.get_width() or \
                        configs.CHARACTER_SIZE[1] != emotion_surface.get_height():
                        emotion_surface = pygame.transform.smoothscale(emotion_surface, configs.CHARACTER_SIZE)
                    self.__emotions[emotion] = emotion_surface
                
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
    
    def set_active(self) -> None:
        self.__active = True

    def set_inactive(self) -> None:
        self.__active = False

    def get_name(self) -> str:
        return self.__screen_name

    def __get_emotion_image(self, emotion: str) -> Surface:
        if len(self.__emotions) == 0:
            return Surface((0, 0))
        if emotion == "":
            return self.__emotions[self.__last_emotion]
        
        self.__last_emotion = emotion
        return self.__emotions[emotion]

    def get_image(self, emotion: str = "") -> Surface:
        surface = self.__get_emotion_image(emotion)
        
        if self.__active:
            return surface
        else:
            faded = surface.copy()
            faded.fill((90, 90, 90), special_flags=pygame.BLEND_RGB_SUB)
            return faded        

    def get_width(self) -> int:
        return configs.CHARACTER_SIZE[0]

    def get_height(self) -> int:
        return configs.CHARACTER_SIZE[1]

    def get_position(self) -> Tuple[int, int]:
        return self.__position
