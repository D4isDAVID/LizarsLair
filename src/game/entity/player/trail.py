from helpers import Helpers
from helpers.assets.enums import PlayerTrailImage

from .player import PlayerEntity


class TrailEntity(PlayerEntity):
    def __init__(self, helpers: Helpers) -> None:
        super().__init__(
            helpers.assets.images[PlayerTrailImage.HYDRATED.value],
            helpers.assets.images[PlayerTrailImage.NORMAL.value],
            helpers.assets.images[PlayerTrailImage.DRIED.value],
        )
