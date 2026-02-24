import pygame
import settings
from game import Game


pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
running = True


game = Game(screen)


while running:
    dt = clock.tick(settings.FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle_event(event)

    screen.fill("blue")

    game.update(dt)
    game.draw()

    pygame.display.flip()
