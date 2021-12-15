from pygame.rect import Rect
from pygame.surface import Surface
from classes.button import Button
from classes.scene import Scene
from classes.enums import GameState
import configs
import pygame


class Menu(Scene):
    MENU_BUTTON_SIZE = 220, 50

    def __init__(self) -> None:
        super().__init__()

        # Background
        self.__bg_surface = Surface(configs.SCREEN_SIZE)
        background = pygame.image.load("assets/images/outside_house_evening_bg.png").convert()
        if background.get_width() != configs.SCREEN_W:
            scale = configs.SCREEN_W / background.get_width()
            scaled_height = int(background.get_height() * scale)
            background = pygame.transform.smoothscale(background, (configs.SCREEN_W, scaled_height))
        self.__bg_surface.blit(background,(0, 0))
        self.__bg_surface.fill((20, 20, 20), special_flags=pygame.BLEND_RGB_SUB)

        # Title
        font_big = pygame.font.Font("assets/fonts/CarterOne-Regular.ttf", 200)
        text_big = font_big.render("Evert", True, "peru")
        shadow_big = font_big.render("Evert", True, "gray10")
        text_big_position = (configs.SCREEN_W / 2 - text_big.get_width() / 2, configs.SCREEN_H / 2 - 200)
        shadow_big_position = (text_big_position[0] + 4, text_big_position[1] + 4)

        font_small = pygame.font.Font("assets/fonts/CarterOne-Regular.ttf", 120)
        text_small = font_small.render("Olá", True, "hotpink2")
        shadow_small = font_small.render("Olá", True, "gray10")
        text_small_position = (text_big_position[0] - 100, text_big_position[1] - 80)
        shadow_small_position = (text_small_position[0] + 4, text_small_position[1] + 4)       

        self.__bg_surface.blit(shadow_big, shadow_big_position)
        self.__bg_surface.blit(shadow_small, shadow_small_position)
        self.__bg_surface.blit(text_big, text_big_position)
        self.__bg_surface.blit(text_small, text_small_position)

        # Buttons
        ref_x = int((configs.SCREEN_W / 2 ) - (Menu.MENU_BUTTON_SIZE[0] /2))
        ref_y = int(configs.SCREEN_H / 2) + 100

        button_start = Button("Jogar", Rect((ref_x, ref_y + 80), Menu.MENU_BUTTON_SIZE), GameState.GAME_FRESH)
        super().add_button(button_start)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.__bg_surface, (0, 0))
        super().draw(screen)
