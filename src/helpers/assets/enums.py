from enum import Enum


class GridImage(Enum):
    TILE = 'grid/tile'


class MobImage(Enum):
    SALT = 'mob/salt'


class PlayerHeadImage(Enum):
    HYDRATED = 'player/head/hydrated'
    NORMAL = 'player/head/normal'
    DRIED = 'player/head/dried'


class PlayerCornerImage(Enum):
    HYDRATED = 'player/corner/hydrated'
    NORMAL = 'player/corner/normal'
    DRIED = 'player/corner/dried'


class PlayerTrailImage(Enum):
    HYDRATED = 'player/trail/hydrated'
    NORMAL = 'player/trail/normal'
    DRIED = 'player/trail/dried'


class MusicSound(Enum):
    MAIN_MENU = 'music/main_menu'
    FIGHT = 'music/fight'
    REIGNITED = 'music/reignited'
