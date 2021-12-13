from classes.projectile import Projectile
from classes.enums import Direction
from typing import Tuple
import pygame


class ToxicLove(Projectile):
    SPEED = 200
    MAX_DISTANCE = 800

    def __init__(self, start: Tuple[int, int], direction: Direction) -> None:
        surface = pygame.image.load("assets/images/toxic_love.png").convert_alpha()
        surface = pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2))
        super().__init__(surface, start, direction)
