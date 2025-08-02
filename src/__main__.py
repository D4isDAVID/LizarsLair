from common.log import get_logger
from game import Game

logger = get_logger('main')
game = Game()


def main() -> None:
    logger.info('Starting the game')
    game.start()


if __name__ == '__main__':
    main()
