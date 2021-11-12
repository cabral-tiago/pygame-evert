from classes.states import GameState
from classes.gameobject import GameObject
from pygame.surface import Surface
from pygame.font import Font


class MenuButton(GameObject):
    MENU_BUTTON_WIDTH = 200
    MENU_BUTTON_HEIGHT = 40

    def __init__(self, text: str, target_state: GameState) -> None:
        self.__target_state: GameState = target_state

        font = Font(None, 40)

        surface: Surface = Surface((MenuButton.MENU_BUTTON_WIDTH,
                                    MenuButton.MENU_BUTTON_HEIGHT))
        surface.fill("white")

        button_text = font.render(text, True, "black")
        surface.blit(button_text, (MenuButton.MENU_BUTTON_WIDTH / 2 - button_text.get_width() / 2,
                                    MenuButton.MENU_BUTTON_HEIGHT /2 - button_text.get_height() / 2))
        
        super().__init__(surface)

    def get_target_state(self) -> GameState:
        return self.__target_state
