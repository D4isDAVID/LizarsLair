import sys
from pathlib import Path

from pygame import Rect


def center_rect(rect: Rect, parent: Rect) -> None:
    rect.x = parent.width // 2 - rect.width // 2
    rect.y = parent.height // 2 - rect.height // 2


def get_assets_path() -> str:
    pyinstaller_path = str(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else None  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType, reportAttributeAccessIssue]  # noqa: SLF001
    base_path = pyinstaller_path or f'{__file__}/../../..'

    return str((Path(base_path) / 'assets').resolve())
