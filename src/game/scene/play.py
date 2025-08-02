from pygame.sprite import RenderUpdates

from .scene import Scene


class PlayScene(Scene):
    @staticmethod
    def id() -> str:
        return 'play'

    def __init__(self) -> None:
        super().__init__(RenderUpdates(), RenderUpdates())  # pyright: ignore[reportUnknownMemberType]
