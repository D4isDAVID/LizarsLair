from game.entity import TrailEntity

from .entity import EntityGrid


class TrailGrid(EntityGrid[TrailEntity | None]):
    def __init__(self) -> None:
        super().__init__((11, 10), (32, 32), lambda: None)
