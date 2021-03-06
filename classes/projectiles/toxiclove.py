from classes.projectile import Projectile
from classes.enums import Direction
from typing import Tuple
import pygame


class ToxicLove(Projectile):
    SPEED = 120
    MAX_DISTANCE = 500
    DAMAGE = 70

    def __init__(self, start: Tuple[int, int], direction: Direction) -> None:
        surface = pygame.image.load("assets/images/toxic_love.png").convert_alpha()
        hitfx = pygame.image.load("assets/images/void_hitfx.png").convert_alpha()

        super().__init__(surface, start, direction, hitfx)
