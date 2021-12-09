from pygame.surface import Surface
from classes.button import Button
from classes.buttongroup import ButtonGroup
from classes.scene import Scene
from game import GameState
import configs
import pygame


class Menu(Scene):
    MENU_BUTTON_SIZE = 200, 40

    def __init__(self) -> None:
        super().__init__()

        # Background
        self.__bg_surface = Surface(configs.SCREEN_SIZE)
        background = pygame.image.load("assets/images/outside_house_evening_bg.png")
        if background.get_width() != configs.SCREEN_W:
            scale = configs.SCREEN_W / background.get_width()
            scaled_height = int(background.get_height() * scale)
            background = pygame.transform.smoothscale(background, (configs.SCREEN_W, scaled_height))
        self.__bg_surface.blit(background,(0, 0))
        self.__bg_surface.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_SUB)

        # Title
        font_big = pygame.font.Font("assets/fonts/CarterOne-Regular.ttf", 200)
        font_small = pygame.font.Font("assets/fonts/CarterOne-Regular.ttf", 120)
        text_big = font_big.render("Evert", True, "peru")
        text_small = font_small.render("Olá", True, "hotpink2")
        text_big_position = (configs.SCREEN_W / 2 - text_big.get_width() / 2,
                             configs.SCREEN_H / 2 - 200)
        text_small_position = text_big_position[0] - 100, text_big_position[1] - 80

        self.__bg_surface.blit(text_big, text_big_position)
        self.__bg_surface.blit(text_small, text_small_position)

        # Buttons
        ref_x = int((configs.SCREEN_W / 2 ) - (Menu.MENU_BUTTON_SIZE[0] /2))
        ref_y = int(configs.SCREEN_H / 2) + 100

        self.__menu_buttons: ButtonGroup = ButtonGroup()

        button_continue = Button("Continuar", Menu.MENU_BUTTON_SIZE, (ref_x, ref_y), GameState.GAME_PLAYING)
        self.__menu_buttons.add_button(button_continue)

        button_start = Button("Começar", Menu.MENU_BUTTON_SIZE, (ref_x, ref_y+80), GameState.GAME_FRESH)
        self.__menu_buttons.add_button(button_start)

        super().add_button_group(self.__menu_buttons)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.__bg_surface, (0, 0))
        super().draw(screen)
