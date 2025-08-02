from game.entity import SideTrailEntity
from game.grid.entity import EntityGrid


class SideTrailGrid(EntityGrid[SideTrailEntity | None]):
    def __init__(self) -> None:
        super().__init__((10, 11), (32, 32), lambda: None)
