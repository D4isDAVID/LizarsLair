import contextlib
import operator
from random import randint
from typing import TYPE_CHECKING

import pygame
from pygame import (
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_a,
    K_d,
    K_q,
    K_s,
    K_w,
    K_z,
    Rect,
    Surface,
)
from pygame.font import SysFont

from game.entity import HeadEntity
from game.entity.hp import HpEntity
from game.entity.player.corner import CornerEntity
from game.entity.player.side_trail import SideTrailEntity
from game.entity.player.trail import TrailEntity
from game.entity.salt import SaltEntity
from game.grid import CornerGrid, SideTrailGrid, TileGrid, TrailGrid
from game.grid.grid import Grid
from game.grid.mobs import MobGrid
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
        self.FONT = SysFont('Arial', 25)

        self._tiles = TileGrid(helpers)
        center_rect(self._tiles.rect, surface_rect)
        self._mobs = MobGrid()
        center_rect(self._mobs.rect, surface_rect)
        self._trails = TrailGrid()
        center_rect(self._trails.rect, surface_rect)
        self._side_trails = SideTrailGrid()
        center_rect(self._side_trails.rect, surface_rect)
        self._corners = CornerGrid()
        center_rect(self._corners.rect, surface_rect)

        self._head_pos = (5, 5)
        self._head = HeadEntity(helpers)
        self._corners[self._head_pos] = self._head
        self._turn = True
        self._spawn_interval = 7
        self._spawn = self._spawn_interval

        self._score = 0

        entities: list[Entity] = [
            self._tiles,
            self._trails,
            self._mobs,
            self._side_trails,
            self._corners,
        ]
        super().__init__(entities)

        self._music.play(-1)

    def draw(self, display: Surface) -> None:
        super().draw(display)

        score_text = self.FONT.render(
            f'Score: {self._score}',
            True,  # noqa: FBT003
            (255, 255, 255),
        )
        display.blit(score_text, (0, 0))

    def __del__(self) -> None:
        with contextlib.suppress(pygame.error):
            self._music.stop()

    def _move_head(self, pos: tuple[int, int]) -> None:
        new_pos = (self._head_pos[0] + pos[0], self._head_pos[1] + pos[1])

        if not self._corners.in_bounds(new_pos):
            return

        PlayScene._hit_all(self._corners, 1)
        PlayScene._hit_all(self._trails, 1)
        PlayScene._hit_all(self._side_trails, 1)

        prev_pos = self._head_pos
        self._head_pos = new_pos

        self._corners[prev_pos] = CornerEntity(self._helpers)

        trail_pos = (
            prev_pos[0] + min(pos[0], 0),
            prev_pos[1] + min(pos[1], 0),
        )
        if pos[0] == 0:
            if self._trails.in_bounds(trail_pos):
                self._trails[trail_pos] = TrailEntity(self._helpers)
        elif self._side_trails.in_bounds(trail_pos):
            self._side_trails[trail_pos] = SideTrailEntity(self._helpers)

        self._head.rect.x = self._head.rect.width * self._head_pos[0]
        self._head.rect.y = self._head.rect.height * self._head_pos[1]

        if (
            self._corners.in_bounds(self._head_pos)
            and self._corners[self._head_pos] is not None
        ):
            corners = self._find_loop(None, self._head_pos, [])
            for corner_pos in corners:
                self._corners[corner_pos] = None
                if self._trails.in_bounds(corner_pos):
                    self._trails[corner_pos] = None
                if self._side_trails.in_bounds(corner_pos):
                    self._side_trails[corner_pos] = None
            self._kill_enemies_between_corners(corners)

        self._corners[self._head_pos] = self._head

        self._turn = not self._turn
        if self._turn:
            self._handle_turn()

    def _handle_turn(self) -> None:
        self._spawn -= 1
        if self._spawn == 0:
            self._spawn = self._spawn_interval

            pos = (
                randint(0, self._mobs.size[0] - 1),  # noqa: S311
                randint(0, self._mobs.size[1] - 1),  # noqa: S311
            )
            if self._mobs.in_bounds(pos):
                self._mobs[pos] = SaltEntity(self._helpers)

        for pos, entity in list(self._mobs):
            if entity is None:
                continue

            damage = 5

            positions = [
                (pos[0], pos[1] - 1),
                (pos[0] - 1, pos[1]),
                (pos[0], pos[1] + 1),
                (pos[0] + 1, pos[1]),
            ]

            new_pos = PlayScene._bind_pos(
                positions[randint(0, 3)],  # noqa: S311
                self._mobs.size,
            )

            for hit_pos in positions:
                bound_hit_pos = PlayScene._bind_pos(hit_pos, self._trails.size)

                if self._trails.in_bounds(bound_hit_pos):
                    PlayScene._hit(self._trails, bound_hit_pos, damage)

                if self._side_trails.in_bounds(bound_hit_pos):
                    PlayScene._hit(self._side_trails, bound_hit_pos, damage)

                if self._corners.in_bounds(hit_pos):
                    PlayScene._hit(self._corners, hit_pos, damage)

            if self._mobs.in_bounds(new_pos) and self._mobs[new_pos] is None:
                self._mobs[pos] = None
                self._mobs[new_pos] = entity

    def _kill_enemies_between_corners(
        self, corners: list[tuple[int, int]],
    ) -> None:
        while len(corners) > 1:
            x = corners[0][0]
            column = list(filter(lambda p: p[0] == x, corners))
            top_y = min(column, key=operator.itemgetter(1))[1]
            bottom_y = max(column, key=operator.itemgetter(1))[1]
            for pos in column:
                corners.remove(pos)
            for y in range(top_y, bottom_y):
                pos = (x, y)
                if self._mobs.in_bounds(pos) and self._mobs[pos] is not None:
                    self._mobs[pos] = None
                    self._score += 1

    def _find_loop(
        self,
        prev_pos: tuple[int, int] | None,
        current_pos: tuple[int, int],
        corners: list[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        if prev_pos == current_pos or self._corners[current_pos] is None:
            return []
        if current_pos in corners:
            if current_pos == self._head_pos:
                return corners
            return []

        corners.append(current_pos)

        positions = [
            (current_pos[0], current_pos[1] - 1),
            (current_pos[0] - 1, current_pos[1]),
            (current_pos[0], current_pos[1] + 1),
            (current_pos[0] + 1, current_pos[1]),
        ]
        search = [
            self._find_loop(
                current_pos,
                PlayScene._bind_pos(pos, self._corners.size),
                corners.copy(),
            )
            for pos in filter(lambda pos: pos != prev_pos, positions)
        ]

        return max(search, key=len)

    @staticmethod
    def _bind_pos(
        pos: tuple[int, int], bind: tuple[int, int],
    ) -> tuple[int, int]:
        return (
            min(max(pos[0], 0), bind[0] - 1),
            min(max(pos[1], 0), bind[1] - 1),
        )

    @staticmethod
    def _hit_all[T: HpEntity | None](entities: Grid[T], hp: int) -> None:
        for pos, _entity in list(entities):
            PlayScene._hit(entities, pos, hp)

    @staticmethod
    def _hit[T: HpEntity | None](
        entities: Grid[T], pos: tuple[int, int], hp: int,
    ) -> None:
        entity = entities[pos]

        if entity is None or isinstance(entity, HeadEntity):
            return

        entity.hit(hp)
        if entity.hp == 0:
            entities[pos] = None
        else:
            entities[pos] = entity

    def _keydown(self, key: int, _mod: int) -> None:
        # Movement direction map
        direction_map: dict[tuple[int, ...], tuple[int, int]] = {
            (K_w, K_z, K_UP): (0, -1),  # Up
            (K_a, K_q, K_LEFT): (-1, 0),  # Left
            (K_s, K_DOWN): (0, 1),  # Down
            (K_d, K_RIGHT): (1, 0),  # Right
        }

        for keys, direction in direction_map.items():
            if key in keys:
                self._move_head(direction)
                break
