
import pygame

from common.log import get_logger
from game.scene import Scene
from game.scene.play import PlayScene
from helpers import Helpers

TARGET_RES = (420, 420)
TARGET_FPS = 30


class Game:
    def __init__(self) -> None:
        self._logger = get_logger('game')
        self._running = False
        self._helpers = Helpers()

    def load_scene(self, scene: Scene) -> None:
        self._logger.info(
            'Moving from scene %s to %s',
            self._scene.id(),
            scene.id(),
        )

        del self._scene
        self._helpers.assets.images.clear_cache()
        self._helpers.assets.sounds.clear_cache()
        self._scene = scene

    def start(self) -> None:
        self._logger.info('Initializing PyGame')

        pygame.init()

        self._display = pygame.display.set_mode(TARGET_RES, pygame.RESIZABLE)
        self._resolution = pygame.display.get_window_size()
        self._surface_res = TARGET_RES
        self._surface = pygame.Surface(TARGET_RES)
        self._clock = pygame.time.Clock()
        self._scene = PlayScene(self._helpers, self._surface.get_rect())

        self._logger.info('Running game with scene %s', self._scene.id())

        self._running = True
        while self._running:
            self._run()

        self._logger.info('Quitting PyGame')

        pygame.quit()

    def _run(self) -> None:
        self._clock.tick(TARGET_FPS)

        self._scene.draw(self._surface)
        surface = pygame.transform.scale(self._surface, self._surface_res)
        self._display.blit(
            surface,
            (
                self._resolution[0] / 2 - surface.get_width() / 2,
                self._resolution[1] / 2 - surface.get_height() / 2,
            ),
        )
        pygame.display.flip()

        for event in pygame.event.get():
            self._handle_pygame_event(event)

    def _handle_pygame_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.QUIT:
                self._logger.info('Received PyGame QUIT!')
                self._running = False
            case pygame.KEYDOWN:
                self._helpers.event.keyboard.keydown.emit(event.key, event.mod)
            case pygame.KEYUP:
                self._helpers.event.keyboard.keyup.emit(event.key, event.mod)
            case pygame.MOUSEMOTION:
                self._helpers.event.mouse.mousemotion.emit(event.pos)
            case pygame.MOUSEBUTTONUP:
                self._helpers.event.mouse.mousebuttonup.emit(
                    event.pos,
                    event.button,
                )
            case pygame.MOUSEBUTTONDOWN:
                self._helpers.event.mouse.mousebuttondown.emit(
                    event.pos,
                    event.button,
                )
            case pygame.VIDEORESIZE:
                self._resolution = pygame.display.get_window_size()
                res = min(self._resolution[0], self._resolution[1])
                self._surface_res = (res, res)
            case _:
                pass
