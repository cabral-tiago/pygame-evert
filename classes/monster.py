from typing import Tuple
from pygame.surface import Surface
from pygame.rect import Rect
from classes.enums import Direction
import pygame
import random


class Monster:
    SPEED = 80
    SHOOTING_FREQ = 2
    ROTATE_FREQ = 3
    MAX_HP = 100

    def __init__(self, position: Tuple[int, int]) -> None:
        surface = pygame.image.load("assets/images/catfish.png")
        self.__surface = pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2))
        self.__direction: Direction = Direction(random.randint(0,3))
        self.__position: Tuple[float, float] = position
        self.__prev_position: Tuple[float, float] = position
        
        self.__rotate_timer = 0
        
        self.__hp: int = Monster.MAX_HP
        self.__shooting_timer = 0

    def move(self, dt: float) -> None:
        self.__rotate_timer += dt
        if self.__rotate_timer >= Monster.ROTATE_FREQ:
            self.__rotate()

        direction_x = 0
        direction_y = 0
        match self.__direction:
            case Direction.RIGHT:
                direction_x = 1
            case Direction.LEFT:
                direction_x = -1
            case Direction.DOWN:
                direction_y = 1
            case Direction.UP:
                direction_y = -1
        
        new_x = self.__position[0] + (dt * direction_x * Monster.SPEED)
        new_y = self.__position[1] + (dt * direction_y * Monster.SPEED)
        
        self.__prev_position = self.__position
        self.__position = (new_x, new_y)
    
    def __rotate(self) -> None:
        self.__rotate_timer = 0

        direction = Direction(random.randint(0,3))
        while self.__direction == direction:
            direction = Direction(random.randint(0,3))
        
        self.__direction = direction
    
    def set_world_collision(self) -> None:
        self.__position = self.__prev_position

        self.__rotate()

    def is_alive(self) -> bool:
        return self.__hp > 0

    def get_surface(self) -> Surface:
        return self.__surface

    def get_rect(self) -> Rect:
        position = (int(self.__position[0]), int(self.__position[1]))
        return self.get_surface().get_rect(center=position)
