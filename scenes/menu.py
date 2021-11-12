from classes.menubutton import MenuButton
from classes.scene import Scene
from game import GameState


class Menu(Scene):
    def __init__(self) -> None:
        super().__init__()

        button_continue = MenuButton("Continuar", GameState.GAME_PLAYING)
        button_continue.x = 100
        button_continue.y = 100
        self.objects.append(button_continue)

        button_start = MenuButton("Começar", GameState.GAME_FRESH)
        button_start.x = 100
        button_start.y = 200
        self.objects.append(button_start)
