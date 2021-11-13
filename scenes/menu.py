from classes.button import Button
from classes.scene import Scene
from game import GameState


class Menu(Scene):
    MENU_BUTTON_SIZE = 200, 40

    def __init__(self) -> None:
        super().__init__()

        button_continue = Button("Continuar", Menu.MENU_BUTTON_SIZE, GameState.GAME_PLAYING)
        button_continue.x = 100
        button_continue.y = 100
        self.buttons.append(button_continue)

        button_start = Button("Começar", Menu.MENU_BUTTON_SIZE, GameState.GAME_FRESH)
        button_start.x = 100
        button_start.y = 200
        self.buttons.append(button_start)
