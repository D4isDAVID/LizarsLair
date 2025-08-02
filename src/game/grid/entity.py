from collections.abc import Callable

from pygame import SRCALPHA, Surface

from game.entity import Entity

from .grid import Grid


class EntityGrid[T: Entity | None](Grid[T], Entity):
    def __init__(
        self,
        size: tuple[int, int],
        entity_size: tuple[int, int],
        default: Callable[[], T],
    ) -> None:
        def default_factory(pos: tuple[int, int]) -> T:
            entity = default()
            if entity is not None:
                entity.rect.x = pos[0] * entity_size[0]
                entity.rect.y = pos[1] * entity_size[1]
            return entity
        super().__init__(size, default_factory)

        surface = Surface(
            (size[0] * entity_size[0], size[1] * entity_size[1]),
            flags=SRCALPHA,
        )
        Entity.__init__(self, surface)

        for column in self._grid:
            for entity in column:
                if entity is not None:
                    surface.blit(entity.image, entity.rect)

    def __setitem__(
        self,
        pos: tuple[int, int],
        value: T | None = None,
    ) -> None:
        old = super().__getitem__(pos)
        if old is not None:
            self.image.fill((0, 0, 0, 0), old.rect)

        if value is not None:
            value.rect.x = value.rect.width * pos[0]
            value.rect.y = value.rect.height * pos[1]
            self.image.blit(value.image, value.rect)

        return super().__setitem__(pos, value)
