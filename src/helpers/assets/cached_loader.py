from abc import ABC, abstractmethod
from logging import Logger


class CachedLoader[T](ABC):
    def __init__(self, logger: Logger) -> None:
        self._logger = logger
        self._cache: dict[str, T] = {}

    @staticmethod
    @abstractmethod
    def _load(key: str) -> T:
        pass

    def cache(self, *keys: str) -> None:
        for key in keys:
            self._cache[key] = self._load(f'{key}.png')

    def clear_cache(self) -> None:
        self._cache.clear()

    def __getitem__(self, key: str) -> T:
        if key not in self._cache:
            self._logger.info('Asset %s is used despite not being cached', key)
            self.cache(key)

        return self._cache[key]
