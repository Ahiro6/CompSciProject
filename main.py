import stddraw
import keyboard
import math

from player import Character, Player
from game import Game


def main():

    x = 0.5
    y = 0.075

    speed = 0.05
    size = 0.05
    health = 100

    damage = 100
    speed_proj = 0.1
    angle = math.pi / 2

    player = Player(
        x, y, speed, size, health, damage=damage, speed_proj=speed_proj, angle=angle
    )

    game = Game(player)

    game.start()


if __name__ == "__main__":
    main()
