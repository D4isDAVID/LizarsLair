from typing import TYPE_CHECKING

from pygame import Rect

from game.entity import HeadEntity
from game.grid import CornerGrid, SideTrailGrid, TileGrid, TrailGrid
from helpers import Helpers
from helpers.assets.enums import MusicSound
from helpers.utils import center_rect

from .scene import Scene

if TYPE_CHECKING:
    from game.entity import Entity


class PlayScene(Scene):
    @staticmethod
    def id() -> str:
        return 'play'

    def __init__(self, helpers: Helpers, surface_rect: Rect) -> None:
        self._music = helpers.assets.sounds[MusicSound.FIGHT.value]
        helpers.event.keyboard.keydown.on(self._keydown)

        self._tiles = TileGrid(helpers)
        center_rect(self._tiles.rect, surface_rect)
        self._trails = TrailGrid()
        center_rect(self._trails.rect, surface_rect)
        self._side_trails = SideTrailGrid()
        center_rect(self._side_trails.rect, surface_rect)
        self._corners = CornerGrid()
        center_rect(self._corners.rect, surface_rect)

        self._corners[5, 5] = HeadEntity(helpers)

        entities: list[Entity] = [
            self._tiles,
            self._trails,
            self._side_trails,
            self._corners,
        ]
        super().__init__(entities)

        self._music.play()

    def __del__(self) -> None:
        self._music.stop()

    def _keydown(self, key: str, _mod: int) -> None:
        pass
