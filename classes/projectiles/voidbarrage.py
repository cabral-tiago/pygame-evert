from classes.projectile import Projectile
from classes.enums import Direction
from typing import Tuple
import pygame


class VoidBarrage(Projectile):
    SPEED = 135
    MAX_DISTANCE = 300
    DAMAGE = 95

    def __init__(self, start: Tuple[int, int]) -> None:
        surface = pygame.image.load("assets/images/void_barrage.png").convert_alpha()
        hitfx = pygame.image.load("assets/images/void_hitfx.png").convert_alpha()

        super().__init__(surface, start, Direction.LEFT, hitfx)
