from classes.projectile import Projectile
from classes.enums import Direction
from typing import Tuple
import pygame


class ToxicLove(Projectile):
    MAX_DISTANCE = 800

    def __init__(self, start: Tuple[int, int], direction: Direction) -> None:
        surface = pygame.image.load("assets/images/toxic_love.png")
        super().__init__(surface, start, direction)
