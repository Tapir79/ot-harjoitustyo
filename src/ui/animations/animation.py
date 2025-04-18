import pygame


class AnimationSprite(pygame.sprite.Sprite):
    def __init__(self, position, size, image_paths, duration=400):
        super().__init__()
        self.images = [pygame.image.load(
            path).convert_alpha() for path in image_paths]
        self.images = [pygame.transform.scale(
            img, (size.width, size.height)) for img in self.images]

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=position)

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = duration // len(self.images)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index < len(self.images):
                self.image = self.images[self.index]
            else:
                self.kill()
