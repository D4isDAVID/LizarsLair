from pygame import Surface

from .entity import Entity


class HpEntity(Entity):
    def __init__(self, hp: int, surface: Surface) -> None:
        super().__init__(surface)

        self._max_hp = hp
        self._hp = hp

    def hit(self, hp: int) -> None:
        self._hp -= hp

        if self._hp <= 0:
            self.kill()

    def heal(self, hp: int) -> None:
        self._hp = max(self._hp + hp, self._max_hp)
