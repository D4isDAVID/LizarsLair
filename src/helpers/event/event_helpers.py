from dataclasses import dataclass, field

from .keyboard_helper import KeyboardHelper
from .mouse_helper import MouseHelper


@dataclass
class EventHelpers:
    keyboard: KeyboardHelper = field(default_factory=KeyboardHelper)
    mouse: MouseHelper = field(default_factory=MouseHelper)
