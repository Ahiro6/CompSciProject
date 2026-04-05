import stddraw
import keyboard
import math

from player import Character, Player
from game import Game
from projectile import *

from globals import *


def main():

    #initiating player character
    player = Player(
        PLAYER_START_X,
        PLAYER_START_Y,
        SPEED,
        SIZE,
        HEALTH,
        ANGULAR_SPEED,
        DAMAGE,
        SPEED_PROJECTILE,
        AMMO,
        SPEED_RELOAD,
        ANGLE,
    )

    #setting window scale and size
    stddraw.setXscale(START_X, END_X)
    stddraw.setYscale(START_Y, END_Y)
    stddraw.setCanvasSize(SCREEN_WIDTH, SCREEN_HEIGHT)

    #initiate and start game application
    game = Game(player)
    game.start()


if __name__ == "__main__":
    main()
