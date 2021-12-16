import pygame
import configs
from game import Game

pygame.init()
pygame.display.set_caption(configs.WINDOW_TITLE)
pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))
screen = pygame.display.set_mode(configs.SCREEN_SIZE)

# Loading screen
screen.fill("black")
loading_font = pygame.font.Font("assets/fonts/CarterOne-Regular.ttf", 36)
loading_text = loading_font.render("A carregar...", True, "white")
screen.blit(loading_text,
            (configs.SCREEN_W/2 - loading_text.get_width()/2,
             configs.SCREEN_H/2 - loading_text.get_height()/2))
pygame.display.update()

# Music
pygame.mixer.init()

# Game
game = Game()

# Fps Display
fps_font = pygame.font.Font("assets/fonts/Roboto-Medium.ttf", 16)

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
            case pygame.KEYDOWN:
                game.handle_key_down(event.key)
            case pygame.KEYUP:
                game.handle_key_up(event.key)
            
    
    screen.fill("black")

    game.update(dt)
    game.draw(screen)

    if configs.DEBUG:
        fps_text = fps_font.render(f"{clock.get_fps():.0f}/{configs.MAX_FPS} FPS", True, "white")
        screen.blit(fps_text, (configs.SCREEN_W - fps_text.get_width(), 0))

    pygame.display.update()

pygame.quit()
