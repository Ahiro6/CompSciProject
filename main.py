import stddraw
import sys

from player import Player
from game import Game
from projectile import *

from globals import *


def main():

    # checks if game should be run in legacy mode
    tag = None
    if len(sys.argv) > 1:
        tag = sys.argv[1]

    legacy = tag == "legacy"

    # initiating player character
    player = Player(
        PLAYER_START_X,
        PLAYER_START_Y,
        H_SPEED,
        H_SIZE,
        H_HEALTH,
        H_ANGULAR_SPEED,
        H_DAMAGE,
        H_SPEED_PROJECTILE,
        H_AMMO,
        H_SPEED_RELOAD,
        H_ANGLE,
    )

    # setting window scale and size
    stddraw.setXscale(START_X, END_X)
    stddraw.setYscale(START_Y, END_Y)
    stddraw.setCanvasSize(SCREEN_WIDTH, SCREEN_HEIGHT)

    # initiate and start game application
    game = Game(player, max_wave=MAX_WAVES, legacy=legacy)
    game.start()


if __name__ == "__main__":
    main()
