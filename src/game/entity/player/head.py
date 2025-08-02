from helpers import Helpers
from helpers.assets.enums import PlayerHeadImage

from .player import PlayerEntity


class HeadEntity(PlayerEntity):
    def __init__(self, helpers: Helpers) -> None:
        super().__init__(
            helpers.assets.images[PlayerHeadImage.HYDRATED.value],
            helpers.assets.images[PlayerHeadImage.NORMAL.value],
            helpers.assets.images[PlayerHeadImage.DRIED.value],
        )
