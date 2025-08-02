from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface


class Entity(Sprite):
    def __init__(self, image: Surface, rect: Rect) -> None:
        super().__init__()

        self._image = image
        self._rect = rect
