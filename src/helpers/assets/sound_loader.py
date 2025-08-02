from pygame.mixer import Sound

from common.log import get_logger
from helpers.assets.cached_loader import CachedLoader
from helpers.utils import get_assets_path


class SoundLoader(CachedLoader[Sound]):
    def __init__(self) -> None:
        super().__init__(get_logger('sound_loader'))

    @staticmethod
    def _load(key: str) -> Sound:
        return Sound(f'{get_assets_path()}/sounds/{key}.mp3')
