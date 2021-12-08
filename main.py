import pygame
import configs
from game import Game

pygame.init()
screen = pygame.display.set_mode(configs.SCREEN_SIZE)
pygame.display.set_caption(configs.WINDOW_TITLE)

# Loading screen
screen.fill("black")
loading_font = pygame.font.Font("assets/fonts/CarterOne-Regular.ttf", 36)
loading_text = loading_font.render("A carregar...", True, "white")
screen.blit(loading_text,
            (configs.SCREEN_W/2 - loading_text.get_width()/2,
             configs.SCREEN_H/2 - loading_text.get_height()/2))
pygame.display.update()

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
            case pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    game.handle_mouse_click()
    
    screen.fill("black")

    game.update(dt)
    game.draw(screen)

    pygame.display.update()

pygame.quit()
