from dataclasses import dataclass, field

from .emitter import EventEmitter


@dataclass
class KeyboardHelper:
    keydown: EventEmitter[str, int] = field(default_factory=EventEmitter)
    keyup: EventEmitter[str, int] = field(default_factory=EventEmitter)
