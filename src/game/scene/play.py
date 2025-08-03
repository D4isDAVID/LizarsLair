import operator
from random import randint
from typing import TYPE_CHECKING

from pygame import K_a, K_d, K_s, K_w, Rect, Surface
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
            f'Score: {self._score}', True, (255, 255, 255),
        )
        display.blit(score_text, (0, 0))

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

        self._turn = not self._turn
        PlayScene._hit_all(self._corners, 1)
        PlayScene._hit_all(self._trails, 1)
        PlayScene._hit_all(self._side_trails, 1)

        prev_pos = self._head_pos
        self._head_pos = (new_x, new_y)

        self._corners[prev_pos] = CornerEntity(self._helpers)
        trail_pos = (prev_pos[0] + min(x, 0), prev_pos[1] + min(y, 0))
        if x == 0:
            self._trails[trail_pos] = TrailEntity(self._helpers)
        else:
            self._side_trails[trail_pos] = SideTrailEntity(self._helpers)

        self._head.rect.x = self._head.rect.width * self._head_pos[0]
        self._head.rect.y = self._head.rect.height * self._head_pos[1]
        if self._corners[self._head_pos] is not None:
            corners = self._find_loop(None, self._head_pos, [])
            for pos in corners:
                self._corners[pos] = None
                self._trails[PlayScene._bind_pos(pos, self._trails.size)] = (
                    None
                )
                self._side_trails[pos] = None
            self._kill_enemies_between_corners(corners)
        self._corners[self._head_pos] = self._head

        if self._turn:
            self._spawn -= 1
            if self._spawn == 0:
                self._spawn = self._spawn_interval

                pos = (
                    randint(0, self._mobs.size[0] - 1),
                    randint(0, self._mobs.size[1] - 1),
                )
                self._mobs[pos] = SaltEntity(self._helpers)

            for pos, entity in list(self._mobs):
                if entity is None:
                    continue

                dir = randint(0, 3)
                damage = 5

                positions = [
                    (pos[0], pos[1] - 1),
                    (pos[0] - 1, pos[1]),
                    (pos[0], pos[1] + 1),
                    (pos[0] + 1, pos[1]),
                ]

                new_pos = PlayScene._bind_pos(positions[dir], self._mobs.size)

                for hit_pos in positions:
                    PlayScene._hit(
                        self._trails,
                        PlayScene._bind_pos(hit_pos, self._trails.size),
                        damage,
                    )
                    PlayScene._hit(
                        self._side_trails,
                        PlayScene._bind_pos(hit_pos, self._side_trails.size),
                        damage,
                    )
                    PlayScene._hit(self._corners, hit_pos, damage)

                if self._mobs[new_pos] is not None:
                    continue

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
                if self._mobs[x, y] is not None:
                    self._mobs[x, y] = None
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
        if key == K_w:
            self._move_head(0, -1)
        elif key == K_a:
            self._move_head(-1, 0)
        elif key == K_s:
            self._move_head(0, 1)
        elif key == K_d:
            self._move_head(1, 0)
