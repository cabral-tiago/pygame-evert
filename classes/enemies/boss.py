from classes.enemy import Enemy
from classes.enums import Direction
from classes.projectile import Projectile
from classes.projectiles.voidbarrage import VoidBarrage
from typing import Tuple
import pygame


class Boss(Enemy):
    SPEED = 80
    SHOOTS = True
    SHOOTING_COOLDOWN_RANGE = 0.75, 1.75
    CHANGE_DIRECTION_FREQ = 4
    MAX_HP = 690

    def __init__(self, position: Tuple[int, int]) -> None:
        surface = pygame.image.load("assets/images/robert.png").convert_alpha()
        possible_directions = [Direction.UP, Direction.DOWN]
        hurt = pygame.mixer.Sound("assets/sounds/effects/robert-pain.wav")

        super().__init__(surface, position, possible_directions, hurt)

    def shoot(self) -> Projectile:
        super().shoot()
        return VoidBarrage(super().get_rect().center)
