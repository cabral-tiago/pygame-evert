from classes.projectile import Projectile
from classes.enums import Direction
from typing import Tuple
import pygame


class VoidBarrage(Projectile):
    MAX_DISTANCE = 600

    def __init__(self, start: Tuple[int, int]) -> None:
        surface = pygame.image.load("assets/images/void_barrage.png").convert_alpha()
        surface = pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2))
        super().__init__(surface, start, Direction.LEFT)
