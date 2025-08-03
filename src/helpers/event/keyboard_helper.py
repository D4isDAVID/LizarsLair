from dataclasses import dataclass, field

from .emitter import EventEmitter


@dataclass
class KeyboardHelper:
    keydown: EventEmitter[int, int] = field(default_factory=EventEmitter)
    keyup: EventEmitter[int, int] = field(default_factory=EventEmitter)
