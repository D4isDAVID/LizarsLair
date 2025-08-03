from pygame import Rect, Surface

from game.entity.hp import HpEntity


class PlayerEntity(HpEntity):
    MAX_HP = 25
    NORMAL_HP = 15
    DRIED_HP = 5

    def __init__(
        self,
        hydrated: Surface,
        normal: Surface,
        dried: Surface,
    ) -> None:
        self._hydrated = hydrated
        self._normal = normal
        self._dried = dried

        super().__init__(PlayerEntity.MAX_HP, self._hydrated)
        self.rect = Rect(self._hydrated.get_rect())

    def _update_image(self) -> None:
        if self._hp <= PlayerEntity.DRIED_HP:
            self.image = self._dried
        elif self._hp <= PlayerEntity.NORMAL_HP:
            self.image = self._normal
        else:
            self.image = self._hydrated
