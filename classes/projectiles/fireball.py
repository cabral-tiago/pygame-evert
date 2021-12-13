from classes.projectile import Projectile
from typing import Tuple
from pygame.surface import Surface
from classes.enums import Direction
import pygame


class Fireball(Projectile):
    SPEED = 400
    MAX_DISTANCE = 600

    def __init__(self, start: Tuple[int, int], direction: Direction) -> None:
        surface = pygame.image.load("assets/images/fireball.png").convert_alpha()
        surface = pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2))

        super().__init__(surface, start, direction)

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
