from pygame.sprite import Sprite
from pygame.surface import Surface


class Entity(Sprite):
    def __init__(self, surface: Surface) -> None:
        super().__init__()

        self.image = surface
        self.rect = surface.get_rect()
