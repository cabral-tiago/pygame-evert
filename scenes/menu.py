from classes.menubutton import MenuButton
from classes.scene import Scene


class Menu(Scene):
    def __init__(self) -> None:
        super().__init__()

        button_start = MenuButton("Começar")
        button_start.x = 100
        button_start.y = 100

        self.objects.append(button_start)