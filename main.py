import pygame
import configs
from game import Game

pygame.init()
screen = pygame.display.set_mode(configs.SCREEN_SIZE)
pygame.display.set_caption(configs.WINDOW_TITLE)

# Game
game = Game()

# Clock
clock = pygame.time.Clock()

# Main Loop
run = True
while run:
    # Deltatime (ms to s)
    dt = clock.tick(configs.MAX_FPS) / 1000

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                run = False
    
    screen.fill("black")

    game.draw(screen)

    pygame.display.update()

pygame.quit()
