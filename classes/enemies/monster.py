from classes.enemy import Enemy
from classes.enums import Direction
from classes.projectile import Projectile
from classes.projectiles.toxiclove import ToxicLove
from typing import Tuple
import pygame
import random


class Monster(Enemy):
    SPEED = 50
    SHOOTS = True
    SHOOTING_COOLDOWN_RANGE = 1.75, 2.75
    CHANGE_DIRECTION_FREQ = 2
    MAX_HP = 200

    def __init__(self, position: Tuple[int, int]) -> None:
        surface = pygame.image.load("assets/images/catfish.png").convert_alpha()
        possible_directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        hurt = pygame.mixer.Sound("assets/sounds/effects/catfish-cry.wav")

        super().__init__(surface, position, possible_directions, hurt)

    def shoot(self) -> Projectile:
        super().shoot()
        direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
        return ToxicLove(super().get_rect().center, direction)
