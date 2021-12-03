from typing import Tuple
from classes.enums import GameState
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.font import Font
import pygame


class Button:

    def __init__(self, text: str, size: Tuple[int, int], position: Tuple[int, int], target_state: GameState) -> None:
        self.__position: Tuple[int, int] = position
        self.__surface: Surface = Surface(size)
        
        self.__target_state: GameState = target_state
        self.__hovered: bool = False

        font = Font(None, 40)

        self.__surface.fill("white")

        button_text = font.render(text, True, "black")
        self.__surface.blit(button_text, (size[0] / 2 - button_text.get_width() / 2,
                                          size[1] / 2 - button_text.get_height() / 2))

    def hover(self) -> None:
        self.__hovered = True

    def normal(self) -> None:
        self.__hovered = False

    def get_surface(self) -> Surface:
        if self.__hovered:
            return self.__surface
        else:
            faded = self.__surface.copy()
            faded.fill((80, 80, 80, 180), special_flags=pygame.BLEND_RGB_MIN)
            return faded

    def get_target_state(self) -> GameState:
        return self.__target_state
    
    def get_position(self) -> Tuple[int, int]:
        return self.__position

    def get_rect(self) -> Rect:
        return self.get_surface().get_rect(topleft=self.get_position())

    def get_width(self) -> int:
        return self.get_surface().get_width()

    def get_height(self) -> int:
        return self.get_surface().get_height()