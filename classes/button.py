from typing import Tuple
from classes.enums import GameState
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.font import Font
import pygame


class Button:
    def __init__(self, text: str, rect: Rect, target_state: GameState, transparent: bool = False) -> None:
        self.__position: Tuple[int, int] = rect.topleft
        self.__transparent: bool = transparent
        self.__target_state: GameState = target_state
        self.__hovered: bool = False
        self.__visible: bool = True

        # Hovered Surface
        self.__hover_surface: Surface = Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(self.__hover_surface, "white", Rect((0, 0), rect.size), border_radius=8)
        
        # Normal Surface
        self.__surface: Surface = Surface(rect.size, pygame.SRCALPHA)
        if not self.__transparent:
            pygame.draw.rect(self.__surface, "grey10", Rect((0, 0), rect.size), border_radius=8)
            pygame.draw.rect(self.__surface, "white", Rect((0, 0), rect.size), 2, 8)

        # Text rendering
        if text != "":
            font = Font("assets/fonts/Roboto-Medium.ttf", 22)
            
            button_text = font.render(text, True, "white")
            button_text_hover = font.render(text, True, "black")
            self.__surface.blit(button_text, (rect.width / 2 - button_text.get_width() / 2,
                                              rect.height / 2 - button_text.get_height() / 2))
            self.__hover_surface.blit(button_text_hover, (rect.width / 2 - button_text.get_width() / 2,
                                                          rect.height / 2 - button_text.get_height() / 2))

    def is_hovering(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()

        if self.get_rect().collidepoint(mouse_pos):
            self.__hovered = True
        else:
            self.__hovered = False

        return self.__hovered
    
    def show(self) -> None:
        self.__visible = True
    
    def hide(self) -> None:
        self.__visible = False
    
    def is_visible(self) -> bool:
        return self.__visible

    def get_surface(self) -> Surface:
        if not self.__hovered or self.__transparent:
            return self.__surface
        else:
            return self.__hover_surface

    def get_target_state(self) -> GameState:
        return self.__target_state

    def get_rect(self) -> Rect:
        return self.get_surface().get_rect(topleft=self.__position)
