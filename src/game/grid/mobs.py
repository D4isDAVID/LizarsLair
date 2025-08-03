from game.entity.salt import SaltEntity
from game.grid.entity import EntityGrid


class MobGrid(EntityGrid[SaltEntity | None]):
    def __init__(self) -> None:
        super().__init__((10, 10), (32, 32), lambda: None)
