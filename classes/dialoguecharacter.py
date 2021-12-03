import json
from pygame.surface import Surface
from classes.enums import ScreenAlignment
import pygame


class DialogueCharacter:
    def __init__(self, path: str, start_expression: str) -> None:
        self.__screen_name: str = ""
        self.__screen_alignment: ScreenAlignment = ScreenAlignment.NULL
        self.__expressions: dict[str, Surface] = {}
        self.__last_expression: str = start_expression
        
        if path != "":
            with open(path, "r", encoding="utf-8") as file:
                character_data = json.load(file)

                if character_data["screen_name"]:
                    self.__screen_name = character_data["screen_name"]
                
                for expression in character_data["expressions"]:
                    expression_path = f"{path[:-5]}_{expression}.png"
                    expression_surface = pygame.image.load(expression_path)
                    expression_surface = pygame.transform.smoothscale(expression_surface, (500, 600))
                    self.__expressions[expression] = expression_surface
                
                if character_data["screen_alignment"]:
                    match character_data["screen_alignment"]:
                        case "left":
                            self.__screen_alignment = ScreenAlignment.LEFT
                        case "right":
                            self.__screen_alignment = ScreenAlignment.RIGHT
                        case "center":
                            self.__screen_alignment = ScreenAlignment.CENTER
    
    def get_name(self) -> str:
        return self.__screen_name
    
    def get_image(self, expression: str = "") -> Surface:
        if self.__screen_alignment == ScreenAlignment.NULL:
            return Surface((0,0))
        if expression == "":
            return self.__expressions[self.__last_expression]
        else:
            self.__last_expression = expression
            return self.__expressions[expression]

    def get_width(self) -> int:
        return self.get_image().get_width()

    def get_height(self) -> int:
        return self.get_image().get_height()

    def get_screen_alignment(self) -> ScreenAlignment:
        return self.__screen_alignment
