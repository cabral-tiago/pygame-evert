from classes.projectile import Projectile
from typing import Tuple
from pygame.surface import Surface
from classes.enums import Direction
import pygame


class Fireball(Projectile):
    SPEED = 240
    MAX_DISTANCE = 360
    DAMAGE = 60

    def __init__(self, start: Tuple[int, int], direction: Direction) -> None:
        surface = pygame.image.load("assets/images/fireball.png").convert_alpha()
        hitfx = pygame.image.load("assets/images/fireball_hitfx.png").convert_alpha()

        super().__init__(surface, start, direction, hitfx)

    def get_surface(self) -> Surface:
        match super().get_direction():
            case Direction.UP:
                return pygame.transform.rotate(super().get_surface(), 90)
            case Direction.DOWN:
                return pygame.transform.rotate(super().get_surface(), 270)
            case Direction.LEFT:
                return pygame.transform.rotate(super().get_surface(), 180)
            case _:
                return super().get_surface()
