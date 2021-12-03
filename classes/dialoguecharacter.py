import json
from pygame.surface import Surface
from classes.enums import ScreenAlignment
import pygame


class DialogueCharacter:
    def __init__(self, path: str) -> None:
        self.__screen_name: str = ""
        self.__screen_alignment: ScreenAlignment = ScreenAlignment.NULL
        self.__expressions: dict[str, Surface] = {}
        
        if path != "":
            with open(path, "r", encoding="utf-8") as file:
                character_data = json.load(file)

                if character_data["screen_name"]:
                    self.__screen_name = character_data["screen_name"]
                
                for expression in character_data["expressions"]:
                    expression_path = f"{path[:-5]}_{expression}.png"
                    expression_surface = pygame.image.load(expression_path)
                    self.__expressions[expression] = expression_surface
                
                if character_data["screen_alignment"]:
                    self.__screen_alignment = character_data
    
    def get_name(self) -> str:
        return self.__screen_name
    
    def get_image(self, expression: str) -> Surface:
        return self.__expressions[expression]

    def get_screen_alignment(self) -> ScreenAlignment:
        return self.__screen_alignment