from typing import Tuple
from classes.states import GameState
from classes.gameobject import GameObject
from pygame.surface import Surface
from pygame.font import Font


class Button(GameObject):

    def __init__(self, text: str, size: Tuple[int, int], target_state: GameState) -> None:
        self.__target_state: GameState = target_state

        font = Font(None, 40)

        surface: Surface = Surface(size)
        surface.fill("white")

        button_text = font.render(text, True, "black")
        surface.blit(button_text, (size[0] / 2 - button_text.get_width() / 2,
                                   size[1] / 2 - button_text.get_height() / 2))

        super().__init__(surface)

    def get_target_state(self) -> GameState:
        return self.__target_state
