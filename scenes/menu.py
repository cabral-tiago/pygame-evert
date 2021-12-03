from classes.button import Button
from classes.scene import Scene
from game import GameState
import configs


class Menu(Scene):
    MENU_BUTTON_SIZE = 200, 40

    def __init__(self) -> None:
        super().__init__()

        ref_x = int((configs.SCREEN_W / 2 ) - (Menu.MENU_BUTTON_SIZE[0] /2))
        ref_y = int(configs.SCREEN_H / 2) + 100

        button_continue = Button("Continuar", Menu.MENU_BUTTON_SIZE, (ref_x, ref_y), GameState.GAME_PLAYING)
        super().add_button(button_continue)

        button_start = Button("Começar", Menu.MENU_BUTTON_SIZE, (ref_x, ref_y+80), GameState.GAME_FRESH)
        super().add_button(button_start)
