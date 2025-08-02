from pygame import Rect


def center_rect(rect: Rect, parent: Rect) -> None:
    rect.x = parent.width // 2 - rect.width // 2
    rect.y = parent.height // 2 - rect.height // 2
