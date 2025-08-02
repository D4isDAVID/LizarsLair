from helpers import Helpers
from helpers.assets.enums import GridImage

from .entity import Entity


class TileEntity(Entity):
    def __init__(self, helpers: Helpers) -> None:
        image = helpers.assets.images[GridImage.TILE.value]

        super().__init__(image)
