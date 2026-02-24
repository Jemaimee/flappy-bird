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
ellapse_time = 0
score = 0
font = pygame.font.Font(r"assets\SpaceMono-Bold.ttf", size=settings.FONT_SIZE)

birds_group = pygame.sprite.GroupSingle(Bird())

pipes_group = pygame.sprite.Group()
pipe = Pipe()
pipes_group.add(pipe)


def colliding(pipes_group, birds_group):
    bird_mask = birds_group.sprite.mask
    for pipe in pipes_group:
        if pipe.top_mask.overlap(
            bird_mask,
            (
                birds_group.sprite.rect.left - pipe.top_rect.left,
                birds_group.sprite.rect.top - pipe.top_rect.top,
            ),
        ):
            return True
        else:
            return False


def display_score(screen, score, font):
    score_text = font.render(f"SCORE : {score}", True, "black")
    score_rect = score_text.get_rect(center=(settings.WIDTH // 2, 25))
    screen.blit(score_text, score_rect)


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

    screen.fill("blue")
    if not paused:
        if ellapse_time >= settings.PIPE_DELAY:
            pipe = Pipe()
            pipes_group.add(pipe)
            ellapse_time = 0
        ellapse_time += dt

        pipes_group.update(dt)
        birds_group.update(dt)

    if colliding(pipes_group, birds_group):
        paused = True
    if birds_group.sprite.rect.top < 0:
        birds_group.sprite.rect.top = 0
        birds_group.sprite.velocity = 0
    if birds_group.sprite.rect.bottom > settings.HEIGHT:
        running = False

    for pipe in pipes_group:
        if not pipe.passed and birds_group.sprite.rect.right > pipe.top_rect.right:
            score += 1
            pipe.passed = True

    for pipe in pipes_group:
        pipe.draw(screen)
    birds_group.draw(screen)
    display_score(screen, score, font)

    pygame.display.flip()
    print(score)
    dt = clock.tick(settings.FPS) / 1000
