from game.entity import TileEntity
from game.grid.entity import EntityGrid
from helpers import Helpers


class TileGrid(EntityGrid[TileEntity]):
    def __init__(self, helpers: Helpers) -> None:
        super().__init__((10, 10), (32, 32), lambda: TileEntity(helpers))
