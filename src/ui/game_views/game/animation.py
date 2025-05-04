import pygame


class AnimationSprite(pygame.sprite.Sprite):
    """
    A sprite that plays a sequence of images as an animation. 
    When the animation is finished the sprite removes itself.
    """

    def __init__(self, position, size, image_paths, duration=400):
        """
        Initialize the animation sprite.

        Args:
        position (tuple): The (x, y) center position of the animation on the screen.
        size (Size): A Size object to scale images to same size.
        image_paths (list): All images in the animation.
        duration (int): Total time in milliseconds the animation should take. Default is 400.
        """
        super().__init__()
        self._images = [pygame.image.load(path)
                        .convert_alpha() for path in image_paths]
        self._images = [pygame.transform
                        .scale(img, (size.width, size.height)) for img in self._images]

        self._index = 0
        self._image = self._images[self.index]
        self._rect = self._image.get_rect(center=position)

        self._last_update = pygame.time.get_ticks()
        self._frame_rate = duration // len(self._images)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, surf):
        self._image = surf

    @property
    def images(self):
        return self._images

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, new_rect):
        self._rect = new_rect

    @property
    def last_update(self):
        return self._last_update

    @last_update.setter
    def last_update(self, timestamp):
        self._last_update = timestamp

    @property
    def frame_rate(self):
        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self, fr):
        self._frame_rate = fr

    @property
    def image_count(self):
        return len(self._images)

    def update(self):
        """
        Updates the animation frame. If all frames have been shown, the sprite removes itself.
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index < len(self.images):
                self.image = self.images[self.index]
            else:
                self.kill()
