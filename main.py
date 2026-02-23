import pygame
import settings
from bird import Bird


pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
running = True
paused = True
dt = 0

birds_group = pygame.sprite.GroupSingle(Bird())


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                birds_group.sprite.jump(dt)

    if birds_group.sprite.rect.top < 0:
        birds_group.sprite.rect.top = 0
        birds_group.sprite.velocity = 0
    if birds_group.sprite.rect.bottom > settings.HEIGHT:
        running = False

    screen.fill("blue")

    birds_group.update(dt)
    birds_group.draw(screen)
    pygame.display.flip()

    dt = clock.tick(120) / 1000
