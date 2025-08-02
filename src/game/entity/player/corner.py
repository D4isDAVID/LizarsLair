from helpers import Helpers
from helpers.assets.enums import PlayerCornerImage

from .player import PlayerEntity


class CornerEntity(PlayerEntity):
    def __init__(self, helpers: Helpers) -> None:
        super().__init__(
            helpers.assets.images[PlayerCornerImage.HYDRATED.value],
            helpers.assets.images[PlayerCornerImage.NORMAL.value],
            helpers.assets.images[PlayerCornerImage.DRIED.value],
        )
