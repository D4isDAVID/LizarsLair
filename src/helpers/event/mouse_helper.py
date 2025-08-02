from dataclasses import dataclass, field

from .emitter import EventEmitter


@dataclass
class MouseHelper:
    mousemotion: EventEmitter[tuple[int, int]] = field(
        default_factory=EventEmitter,
    )
    mousebuttonup: EventEmitter[tuple[int, int], int] = field(
        default_factory=EventEmitter,
    )
    mousebuttondown: EventEmitter[tuple[int, int], int] = field(
        default_factory=EventEmitter,
    )
