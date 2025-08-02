# pyright: reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportArgumentType=false

from pygame.sprite import OrderedUpdates
from pygame.surface import Surface

from game.entity import Entity


class Scene:
    def __init__(self, entities: list[Entity]) -> None:
        self._entities = OrderedUpdates(*entities)

    def draw(self, display: Surface) -> None:
        self._entities.draw(display)
