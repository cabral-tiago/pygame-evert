from typing import Tuple
from classes.enums import Direction
from pygame.surface import Surface
from pygame.rect import Rect


class Projectile:
    SPEED = 120
    MAX_DISTANCE = 250
    DAMAGE = 50

    def __init__(self, surface: Surface, start: Tuple[int, int], direction: Direction, hitfx: Surface) -> None:
        self.__surface = surface
        self.__position: Tuple[float, float] = start  # Float due to deltatime calculations
        self.__start_position: Tuple[int, int] = start
        self.__direction: Direction = direction
        self.__hitfx: Surface = hitfx
        self.__alive = True

    def __get_position(self) -> Tuple[int, int]:
        return int(self.__position[0]), int(self.__position[1])

    def get_direction(self) -> Direction:
        return self.__direction
    
    def get_hitfx(self) -> Surface:
        return self.__hitfx

    def get_surface(self) -> Surface:
        return self.__surface

    def get_rect(self) -> Rect:
        return self.get_surface().get_rect(center=self.__get_position())
    
    def die(self) -> None:
        self.__alive = False

    def is_alive(self) -> bool:
        return self.__alive

    def update(self, dt: float) -> None:
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
        
        new_x = self.__position[0] + (dt * direction_x * self.SPEED)
        new_y = self.__position[1] + (dt * direction_y * self.SPEED)
        self.__position = (new_x, new_y)

        if abs(self.__start_position[0] - self.__position[0])  > self.MAX_DISTANCE or\
           abs(self.__start_position[1] - self.__position[1])  > self.MAX_DISTANCE:
            self.__alive = False
