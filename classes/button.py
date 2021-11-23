from typing import Tuple
from classes.states import GameState
from classes.gameobject import GameObject
from pygame.surface import Surface
from pygame.font import Font
import pygame


class Button(GameObject):

    def __init__(self, text: str, size: Tuple[int, int], target_state: GameState) -> None:
        self.__target_state: GameState = target_state
        self.hovered: bool = False

        font = Font(None, 40)

        surface: Surface = Surface(size)
        surface.fill("white")

        button_text = font.render(text, True, "black")
        surface.blit(button_text, (size[0] / 2 - button_text.get_width() / 2,
                                   size[1] / 2 - button_text.get_height() / 2))

        super().__init__(surface)

    def get_surface(self) -> Surface:
        if self.hovered:
            return super().get_surface()
        else:
            faded = super().get_surface().copy()
            faded.fill((60, 10, 110, 180), special_flags=pygame.BLEND_RGB_MIN)
            return faded

    def get_target_state(self) -> GameState:
        return self.__target_state
