import settings
import pygame

pygame.display.init()


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(settings.BIRD_SPRITE).convert_alpha()
        self.image = pygame.transform.scale_by(self.original_image, 0.2)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (10, settings.HEIGHT / 2)
        self.velocity = 0
        self.rotation = 0

    def update(self, dt):
        self.velocity += settings.GRAVITY * dt
        self.rect.y += self.velocity * dt

        if self.rotation > -45:
            self.rotation -= settings.ROTATION_SPEED * dt
            self.image = pygame.transform.rotozoom(
                self.original_image, self.rotation, 0.2
            )

        self.rect = self.image.get_rect(center=self.rect.center)

    def jump(self, dt):
        self.velocity = settings.JUMP_STRENGTH
        self.rotation = 45
