from collections.abc import Callable, Generator


class Grid[T]:
    def __init__(
        self,
        size: tuple[int, int],
        default: Callable[[tuple[int, int]], T],
    ) -> None:
        self._default = default
        self._grid = [
            self._default((x, y))
            for y in range(size[1])
            for x in range(size[0])
        ]
        self._size = size

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    def in_bounds(self, pos: tuple[int, int]) -> bool:
        return 0 <= pos[0] < self._size[0] and 0 <= pos[1] < self._size[1]

    def __getitem__(self, pos: tuple[int, int]) -> T:
        return self._grid[pos[0] + (pos[1] * self._size[0])]

    def __setitem__(
        self,
        pos: tuple[int, int],
        value: T | None = None,
    ) -> None:
        if value is None:
            value = self._default(pos)

        self._grid[pos[0] + (pos[1] * self._size[0])] = value

    def __iter__(self) -> Generator[tuple[tuple[int, int], T]]:
        yield from (
            ((x[0] % self._size[0], x[0] // self._size[0]), x[1])
            for x in enumerate(self._grid)
        )
