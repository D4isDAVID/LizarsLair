from dataclasses import dataclass, field

from .image_loader import ImageLoader
from .sound_loader import SoundLoader


@dataclass
class AssetHelpers:
    images: ImageLoader = field(default_factory=ImageLoader)
    sounds: SoundLoader = field(default_factory=SoundLoader)
