import pygame
import settings
from enum import Enum
from bird import Bird
from pipes import Pipe


class GameState(Enum):
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3


class Game:

    def __init__(self, screen):
        self.state = GameState.PAUSED
        self.screen = screen
        self.birds_group = pygame.sprite.GroupSingle(Bird())
        self.pipes_group = pygame.sprite.Group()
        self.pipe = Pipe()
        self.pipes_group.add(self.pipe)
        self.last_pipe = 0
        self.ellapse_time = 0
        self.score = 0
        self.font = pygame.font.Font(
            r"assets\SpaceMono-Bold.ttf", size=settings.FONT_SIZE
        )

    def colliding(self):
        bird_mask = self.birds_group.sprite.mask
        for pipe in self.pipes_group:
            if pipe.top_mask.overlap(
                bird_mask,
                (
                    self.birds_group.sprite.rect.left - pipe.top_rect.left,
                    self.birds_group.sprite.rect.top - pipe.top_rect.top,
                ),
            ):
                return True
            elif pipe.bottom_mask.overlap(
                bird_mask,
                (
                    self.birds_group.sprite.rect.left - pipe.bottom_rect.left,
                    self.birds_group.sprite.rect.top - pipe.bottom_rect.top,
                ),
            ):
                return True
            else:
                return False

    def display_score(self):
        score_text = self.font.render(f"SCORE : {self.score}", True, "black")
        score_rect = score_text.get_rect(center=(settings.WIDTH // 2, 25))
        self.screen.blit(score_text, score_rect)

    def update(self, dt):
        if self.state != GameState.PLAYING:
            return

        if self.ellapse_time >= settings.PIPE_DELAY:
            pipe = Pipe()
            self.pipes_group.add(pipe)
            self.ellapse_time = 0
        self.ellapse_time += dt

        self.pipes_group.update(dt)
        self.birds_group.update(dt)

        if self.colliding():
            self.state = GameState.GAME_OVER
        if self.birds_group.sprite.rect.top < 0:
            self.birds_group.sprite.rect.top = 0
            self.birds_group.sprite.velocity = 0
        if self.birds_group.sprite.rect.bottom > settings.HEIGHT:
            self.state = GameState.GAME_OVER

        for pipe in self.pipes_group:
            if (
                not pipe.passed
                and self.birds_group.sprite.rect.right > pipe.top_rect.right
            ):
                self.score += 1
                pipe.passed = True

    def draw(self):
        for pipe in self.pipes_group:
            pipe.draw(self.screen)
        self.birds_group.draw(self.screen)
        self.display_score()

        if self.state == GameState.GAME_OVER:
            self.screen.fill("black")
            game_over_text = self.font.render("GAME OVER", True, "white")
            game_over_rect = game_over_text.get_rect(
                center=(settings.WIDTH // 2, settings.HEIGHT // 2)
            )
            self.screen.blit(game_over_text, game_over_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.state == GameState.PLAYING:
                self.birds_group.sprite.jump()
            if keys[pygame.K_a]:
                if self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING
                elif self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
