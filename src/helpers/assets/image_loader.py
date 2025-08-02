from pygame import image
from pygame.surface import Surface

from common.log import get_logger
from helpers.assets.cached_loader import CachedLoader
from helpers.utils import get_assets_path


class ImageLoader(CachedLoader[Surface]):
    def __init__(self) -> None:
        super().__init__(get_logger('image_loader'))

    @staticmethod
    def _load(key: str) -> Surface:
        return image.load(f'{get_assets_path()}/images/{key}.png')
