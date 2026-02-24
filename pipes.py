import pygame
import random
import settings


class Pipe(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.x = settings.WIDTH + 200
        self.speed = settings.PIPE_SPEED
        self.gap_size = settings.PIPE_GAP
        self.passed = False
        self.top_image = pygame.image.load(settings.TOP_PIPE_SPRITE).convert_alpha()
        self.top_image = pygame.transform.scale_by(self.top_image, 0.7)
        self.bottom_image = pygame.image.load(
            settings.BOTTOM_PIPE_SPRITE
        ).convert_alpha()
        self.bottom_image = pygame.transform.scale_by(self.bottom_image, 0.7)

        self.gap_y = random.randint(100, settings.HEIGHT - 100)

        self.top_rect = self.top_image.get_rect(
            midbottom=(self.x, self.gap_y - self.gap_size // 2)
        )
        self.bottom_rect = self.bottom_image.get_rect(
            midtop=(self.x, self.gap_y + self.gap_size // 2)
        )
        self.top_mask = pygame.mask.from_surface(self.top_image)
        self.bottom_mask = pygame.mask.from_surface(self.bottom_image)
        self.top_mask_image = self.top_mask.to_surface()
        self.bottom_mask_image = self.bottom_mask.to_surface()

    def update(self, dt):
        self.top_rect.x -= self.speed * dt
        self.bottom_rect.x -= self.speed * dt
        if self.top_rect.right < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.top_image, self.top_rect)
        screen.blit(self.bottom_image, self.bottom_rect)
