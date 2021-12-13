from classes.enemy import Enemy
from classes.enums import Direction
from typing import Tuple
import pygame


class Monster(Enemy):
    def __init__(self, position: Tuple[int, int]) -> None:
        surface = pygame.image.load("assets/images/catfish.png")
        surface = pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2))

        possible_directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

        super().__init__(surface, position, possible_directions)
