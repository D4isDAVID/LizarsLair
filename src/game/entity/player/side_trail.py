from pygame.transform import rotate

from helpers import Helpers
from helpers.assets.enums import PlayerTrailImage

from .player import PlayerEntity


class SideTrailEntity(PlayerEntity):
    def __init__(self, helpers: Helpers) -> None:
        super().__init__(
            rotate(helpers.assets.images[PlayerTrailImage.HYDRATED.value], 90),
            rotate(helpers.assets.images[PlayerTrailImage.NORMAL.value], 90),
            rotate(helpers.assets.images[PlayerTrailImage.DRIED.value], 90),
        )
