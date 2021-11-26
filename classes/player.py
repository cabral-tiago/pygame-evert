from typing import Tuple
from pygame.surface import Surface
from classes.spritesheet import Spritesheet


class Player():
    ANIMATION_INTERVAL = 0.1
    SPEED = 150

    def __init__(self) -> None:
        spritesheet: Spritesheet = Spritesheet("assets/images/elf_spritesheet.png", (18,18), 4)

        self.__sprite_directions = ["down", "up", "right", "left"]
        self.__sprites: dict[str, list[Surface]] = spritesheet.get_dictionary(self.__sprite_directions)

        self.__moving = False
        self.__last_direction = "down"
        self.__current_frame = 0
        self.__max_frames = len(self.__sprites[next(iter(self.__sprites))])
        self.__animation_timer: float = 0
        self.position: Tuple[float, float] = (0, 0)
    
    def update_animation(self, dt: float, direction: str) -> None:
        self.__animation_timer += dt
        if direction == "stopped":
            self.__current_frame = 0
            self.__moving = False
        else:
            if self.__moving == False:
                self.__moving = True
                self.__current_frame = 1
                self.__animation_timer = 0

            if direction != self.__last_direction:
                self.__last_direction = direction
                self.__current_frame = 0
                self.__animation_timer = 0
            
            if self.__animation_timer > Player.ANIMATION_INTERVAL:
                self.__animation_timer -= Player.ANIMATION_INTERVAL
                self.__current_frame += 1
                if self.__current_frame > self.__max_frames - 1:
                    self.__current_frame = 0
    
    def get_surface(self) -> Surface:
        return self.__sprites[self.__last_direction][self.__current_frame]

    def get_rect(self):
        position = int(self.position[0]), int(self.position[1])
        return self.get_surface().get_rect(topleft=position)