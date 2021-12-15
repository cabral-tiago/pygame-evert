from classes.scene import Scene
from classes.button import Button
from classes.enums import GameState
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.font import Font
import configs

class PauseScreen(Scene):
    BUTTON_SIZE = 220, 50

    def __init__(self) -> None:
        super().__init__()

        # Background
        self.__surface: Surface = Surface(configs.SCREEN_SIZE)
        self.__surface.fill("black")

        # Title
        font_big = Font("assets/fonts/CarterOne-Regular.ttf", 120)
        text_big = font_big.render("Pausa", True, "peru")
        self.__surface.blit(text_big, (configs.SCREEN_W / 2 - text_big.get_width() / 2, configs.SCREEN_H / 2 - 200))

        # Buttons
        ref_x = int((configs.SCREEN_W / 2 ) - (self.BUTTON_SIZE[0] /2))
        ref_y = int(configs.SCREEN_H / 2) + 80

        button_continue = Button("Continuar", Rect((ref_x, ref_y), self.BUTTON_SIZE), GameState.GAME_UNPAUSE)
        super().add_button(button_continue)

        button_menu = Button("Desistir", Rect((ref_x, ref_y + 150), self.BUTTON_SIZE), GameState.MAIN_MENU)
        super().add_button(button_menu)

        button_exit = Button("Sair", Rect((ref_x, ref_y + 210), self.BUTTON_SIZE), GameState.EXIT)
        super().add_button(button_exit)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.__surface, (0, 0))
        super().draw(screen)
