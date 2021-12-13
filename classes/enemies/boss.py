from classes.enemy import Enemy
from classes.enums import Direction
from classes.projectile import Projectile
from classes.projectiles.voidbarrage import VoidBarrage
from typing import Tuple
import pygame


class Boss(Enemy):
    SPEED = 120
    SHOOTS = True
    SHOOTING_FREQ = 1.75
    CHANGE_DIRECTION_FREQ = 4
    MAX_HP = 800

    def __init__(self, position: Tuple[int, int]) -> None:
        surface = pygame.image.load("assets/images/robert.png")
        surface = pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2))

        possible_directions = [Direction.UP, Direction.DOWN]

        super().__init__(surface, position, possible_directions)

    def shoot(self) -> Projectile:
        super().shoot()
        return VoidBarrage(super().get_rect().center)
