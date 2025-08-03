from typing import TYPE_CHECKING

from pygame import K_a, K_d, K_s, K_w, Rect

from game.entity import HeadEntity
from game.entity.hp import HpEntity
from game.entity.player.corner import CornerEntity
from game.entity.player.side_trail import SideTrailEntity
from game.entity.player.trail import TrailEntity
from game.grid import CornerGrid, SideTrailGrid, TileGrid, TrailGrid
from game.grid.grid import Grid
from helpers import Helpers
from helpers.assets.enums import MusicSound
from helpers.utils import center_rect

from .scene import Scene

if TYPE_CHECKING:
    from game.entity import Entity


class PlayScene(Scene):
    def __init__(self, helpers: Helpers, surface_rect: Rect) -> None:
        self._music = helpers.assets.sounds[MusicSound.FIGHT.value]
        self._helpers = helpers
        helpers.event.keyboard.keydown.on(self._keydown)

        self._tiles = TileGrid(helpers)
        center_rect(self._tiles.rect, surface_rect)
        self._trails = TrailGrid()
        center_rect(self._trails.rect, surface_rect)
        self._side_trails = SideTrailGrid()
        center_rect(self._side_trails.rect, surface_rect)
        self._corners = CornerGrid()
        center_rect(self._corners.rect, surface_rect)

        self._head_pos = (5, 5)
        self._head = HeadEntity(helpers)
        self._corners[self._head_pos] = self._head

        entities: list[Entity] = [
            self._tiles,
            self._trails,
            self._side_trails,
            self._corners,
        ]
        super().__init__(entities)

        self._music.play(-1)

    def __del__(self) -> None:
        self._music.stop()

    def _move_head(self, x: int, y: int) -> None:
        new_x = self._head_pos[0] + x
        new_y = self._head_pos[1] + y

        if (
            new_x < 0
            or new_x > self._corners.size[0] - 1
            or new_y < 0
            or new_y > self._corners.size[1] - 1
        ):
            return

        PlayScene._hit_all(self._corners, 1)
        PlayScene._hit_all(self._trails, 1)
        PlayScene._hit_all(self._side_trails, 1)

        prev_pos = self._head_pos
        new_pos = (new_x, new_y)

        self._head_pos = new_pos

        self._corners[prev_pos] = CornerEntity(self._helpers)
        trail_x = prev_pos[0] + min(x, 0)
        trail_y = prev_pos[1] + min(y, 0)
        if x == 0:
            trail_pos = (
                min(max(trail_x, 0), self._trails.size[0] - 1),
                min(max(trail_y, 0), self._trails.size[1] - 1),
            )
            self._trails[trail_pos] = TrailEntity(self._helpers)
        else:
            trail_pos = (
                min(max(trail_x, 0), self._side_trails.size[0] - 1),
                min(max(trail_y, 0), self._side_trails.size[1] - 1),
            )
            self._side_trails[trail_pos] = SideTrailEntity(self._helpers)

        self._head.rect.x = self._head.rect.width * self._head_pos[0]
        self._head.rect.y = self._head.rect.height * self._head_pos[1]
        self._corners[self._head_pos] = self._head

    @staticmethod
    def _hit_all[T: HpEntity | None](entities: Grid[T], hp: int) -> None:
        for index, entity in list(entities):
            if entity is None or isinstance(entity, HeadEntity):
                continue

            entity.hit(hp)
            if entity.hp == 0:
                entities[index] = None
            else:
                entities[index] = entity

    def _keydown(self, key: int, _mod: int) -> None:
        if key == K_w:
            self._move_head(0, -1)
        elif key == K_a:
            self._move_head(-1, 0)
        elif key == K_s:
            self._move_head(0, 1)
        elif key == K_d:
            self._move_head(1, 0)
