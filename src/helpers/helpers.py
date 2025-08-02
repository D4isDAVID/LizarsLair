from dataclasses import dataclass, field

from .assets import AssetHelpers
from .event import EventHelpers


@dataclass
class Helpers:
    assets: AssetHelpers = field(default_factory=AssetHelpers)
    event: EventHelpers = field(default_factory=EventHelpers)
