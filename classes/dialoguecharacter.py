import json
from pygame.surface import Surface
from classes.enums import ScreenAlignment
import configs
import pygame


class DialogueCharacter:

    def __init__(self, path: str, start_emotion: str) -> None:
        self.__screen_name: str = ""
        self.__screen_alignment: ScreenAlignment = ScreenAlignment.NULL
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
                    match character_data["screen_alignment"]:
                        case "left":
                            self.__screen_alignment = ScreenAlignment.LEFT
                        case "right":
                            self.__screen_alignment = ScreenAlignment.RIGHT
                        case "center":
                            self.__screen_alignment = ScreenAlignment.CENTER
    
    def set_active(self) -> None:
        self.__active = True

    def set_inactive(self) -> None:
        self.__active = False

    def get_name(self) -> str:
        return self.__screen_name

    def __get_emotion_image(self, emotion: str) -> Surface:
        if emotion == "":
            return self.__emotions[self.__last_emotion]
        else:
            self.__last_emotion = emotion
            return self.__emotions[emotion]

    def get_image(self, emotion: str = "") -> Surface:
        if self.__screen_alignment == ScreenAlignment.NULL:
            return Surface((0,0))

        surface = self.__get_emotion_image(emotion)
        
        if self.__active:
            return surface
        else:
            faded = surface.copy()
            faded.fill((90, 90, 90), special_flags=pygame.BLEND_RGB_SUB)
            return faded        

    def get_width(self) -> int:
        return self.get_image().get_width()

    def get_height(self) -> int:
        return self.get_image().get_height()

    def get_screen_alignment(self) -> ScreenAlignment:
        return self.__screen_alignment
