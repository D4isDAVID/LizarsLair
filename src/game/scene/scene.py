# pyright: reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false

from abc import ABC, abstractmethod

from pygame import Rect
from pygame.sprite import RenderUpdates
from pygame.surface import Surface


class Scene(ABC):
    @staticmethod
    @abstractmethod
    def id() -> str:
        pass

    def __init__(self,
        entities: RenderUpdates, elements: RenderUpdates,
    ) -> None:
        self._entities = entities
        self._elements = elements

    def draw(self, display: Surface) -> list[Rect]:
        game_list = self._entities.draw(display)
        ui_list = self._elements.draw(display)

        return game_list + ui_list
