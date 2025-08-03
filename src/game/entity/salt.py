from helpers import Helpers
from helpers.assets.enums import MobImage

from .entity import Entity


class SaltEntity(Entity):
    def __init__(self, helpers: Helpers) -> None:
        image = helpers.assets.images[MobImage.SALT.value]

        super().__init__(image)
