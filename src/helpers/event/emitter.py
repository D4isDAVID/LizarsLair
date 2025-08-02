from collections.abc import Callable


class EventEmitter[**P]:
    def __init__(self) -> None:
        self._listeners: list[Callable[P, None]] = []

    def emit(self, *args: P.args, **kwargs: P.kwargs) -> None:
        for func in self._listeners:
            func(*args, **kwargs)

    def on(self, func: Callable[P, None]) -> None:
        self._listeners.append(func)

    def off(self, func: Callable[P, None]) -> None:
        self._listeners.remove(func)
