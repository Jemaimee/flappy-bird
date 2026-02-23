import pygame
import settings
from bird import Bird
from pipes import Pipe


pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
running = True
paused = True
dt = 0
last_pipe = 0
ellapse_time = settings.PIPE_DELAY

birds_group = pygame.sprite.GroupSingle(Bird())

pipes_group = pygame.sprite.Group()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not paused:
                birds_group.sprite.jump(dt)
            if keys[pygame.K_a]:
                if paused:
                    paused = False
                else:
                    paused = True

    if birds_group.sprite.rect.top < 0:
        birds_group.sprite.rect.top = 0
        birds_group.sprite.velocity = 0
    if birds_group.sprite.rect.bottom > settings.HEIGHT:
        running = False

    screen.fill("blue")
    if not paused:
        if ellapse_time >= settings.PIPE_DELAY:
            pipe = Pipe()
            pipes_group.add(pipe)
            ellapse_time = 0
        ellapse_time += dt

        pipes_group.update(dt)
        birds_group.update(dt)

    for pipe in pipes_group:
        pipe.draw(screen)
    birds_group.draw(screen)

    pygame.display.flip()
    print(pipes_group)
    dt = clock.tick(120) / 1000
