from typing import Tuple
from classes.enums import GameState
import configs
from classes.button import Button
from pygame.surface import Surface
import pygame


class ButtonGroup:
    def __init__(self) -> None:
        self.__surface: Surface = Surface(configs.SCREEN_SIZE, pygame.SRCALPHA)
        self.__buttons: list[Button] = []
        self.__visible = True

    def add_button(self, button: Button) -> None:
        self.__buttons.append(button)
    
    def show(self) -> None:
        self.__visible = True

    def hide(self) -> None:
        self.__visible = False
    
    def is_visible(self) -> bool:
        return self.__visible

    def is_hovering(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        flag_hovered = False

        for button in self.__buttons:
            if button.get_rect().collidepoint(mouse_pos):
                button.hover()
                flag_hovered = True
            else:
                button.normal()

        return flag_hovered

    def click(self, mouse_pos: Tuple[int, int]) -> GameState:
        for button in self.__buttons:
            if button.get_rect().collidepoint(mouse_pos):
                return button.get_target_state()
        
        return GameState.NULL
    
    def get_surface(self) -> Surface:
        surface = self.__surface.copy()

        for button in self.__buttons:
            surface.blit(button.get_surface(), button.get_rect())
        
        return surface
