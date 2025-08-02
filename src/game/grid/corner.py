from game.entity import CornerEntity, HeadEntity
from game.grid.entity import EntityGrid


class CornerGrid(EntityGrid[HeadEntity | CornerEntity | None]):
    def __init__(self) -> None:
        super().__init__((11, 11), (32, 32), lambda: None)
