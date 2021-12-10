from typing import Tuple
from pygame.rect import Rect
from pygame.surface import Surface
from classes.enums import PlayerDirection
import pygame


class Bullet:
    SPEED = 400
    MAX_DISTANCE = 600

    def __init__(self, start: Tuple[int, int], direction: PlayerDirection) -> None:
        self.__surface = Surface((15,5))
        self.__surface.fill("yellow")

        self.__position: Tuple[float, float] = start
        self.__start_position = start
        self.__direction = direction

        self.__alive = True

    def __get_position(self) -> Tuple[int, int]:
        return int(self.__position[0]), int(self.__position[1])

    def get_rect(self) -> Rect:
        return self.get_surface().get_rect(topleft=self.__get_position())
    
    def get_surface(self) -> Surface:
        if self.__direction == PlayerDirection.DOWN or self.__direction == PlayerDirection.UP:
            return pygame.transform.rotate(self.__surface, 90)
        return self.__surface
    
    def is_alive(self) -> bool:
        return self.__alive

    def update(self, dt: float) -> None:
        direction_x = 0
        direction_y = 0
        match self.__direction:
            case PlayerDirection.RIGHT:
                direction_x = 1
            case PlayerDirection.LEFT:
                direction_x = -1
            case PlayerDirection.DOWN:
                direction_y = 1
            case PlayerDirection.UP:
                direction_y = -1
        
        new_x = self.__position[0] + (dt * direction_x * Bullet.SPEED)
        new_y = self.__position[1] + (dt * direction_y * Bullet.SPEED)
        self.__position = (new_x, new_y)

        if abs(self.__start_position[0] - self.__position[0])  > Bullet.MAX_DISTANCE or\
           abs(self.__start_position[1] - self.__position[1])  > Bullet.MAX_DISTANCE:
            self.__alive = False
