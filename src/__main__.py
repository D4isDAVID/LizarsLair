from common.log import get_logger
from game import Game
from game.scene.play import PlayScene

logger = get_logger('main')
game = Game(PlayScene())


def main() -> None:
    logger.info('Starting the game')
    game.start()


if __name__ == '__main__':
    main()
