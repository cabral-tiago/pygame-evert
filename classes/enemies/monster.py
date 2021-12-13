from classes.enemy import Enemy
from classes.enums import Direction
from classes.projectile import Projectile
from classes.projectiles.toxiclove import ToxicLove
from typing import Tuple
import pygame
import random


class Monster(Enemy):
    SPEED = 80
    SHOOTS = True
    SHOOTING_FREQ = 2.5
    CHANGE_DIRECTION_FREQ = 2
    MAX_HP = 100

    def __init__(self, position: Tuple[int, int]) -> None:
        surface = pygame.image.load("assets/images/catfish.png").convert_alpha()
        surface = pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2))

        possible_directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

        super().__init__(surface, position, possible_directions)

    def shoot(self) -> Projectile:
        super().shoot()
        direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
        return ToxicLove(super().get_rect().center, direction)
