from pygame import Surface

from .entity import Entity


class HpEntity(Entity):
    def __init__(self, hp: int, surface: Surface) -> None:
        super().__init__(surface)

        self._max_hp = hp
        self._hp = hp

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, hp: int) -> None:
        self._hp = max(min(hp, self._max_hp), 0)

    def hit(self, hp: int) -> None:
        self.hp = self._hp - hp

    def heal(self, hp: int) -> None:
        self.hp = self._hp + hp
