from player import Basic
from globals import *
import stddraw

# TODO: formation movement: jump down

"""
Swarm class: manages all the enemies in the formation
- n: number of enemies in formation
- size: size of each enemy
- speed_x: speed in x-axis
- speed_y: speed in y-axis
- vel_x: velocity/current speed in x-axis
- vel_y: velocity/current speed in y-axis
- health: health of each enemy
- points: points each enemy is worth
- units: list of all the enemies
- grid_mode: decides if enemies move together in a grid or move seperately
- type_unit: type of character each unit/enemy is
- dead: dead if all units/enemies are killed
- gap: space between each unit/enemy in the formation (left, right, top, bottom)
- bump: determines the space a formation should be moved down to make space above
- x_start: x coordinate of first enemy in formation
- x_end: x coordinate of last enemy in formation
- y_start: y coordinate of first enemy in formation
- y_end: y coordinate of last enemy in formation
"""


class Swarm:

    def __init__(
        self,
        n,
        size,
        speed_x,
        speed_y,
        health,
        points,
        grid_mode=True,
        type_unit=Basic,
        bump=0,
    ):

        self.n = n
        self.size = size

        self.speed_x = speed_x * WIDTH
        self.speed_y = speed_y * HEIGHT

        self.vel_x = 0
        self.vel_y = 0

        self.health = health
        self.points = points

        self.units = []

        self.grid_mode = grid_mode
        self.type_unit = type_unit

        self.dead = False

        self.gap = self.size * 0.4 * WIDTH
        self.bump = bump

        self.x_start = START_X + self.gap + self.size * WIDTH
        self.x_end = self.x_start

        self.y_end = (
            END_Y - (2 * self.size * HEIGHT + self.gap) + self.size * HEIGHT - self.bump
        )
        self.y_start = self.y_end

        # generates formation of enemies
        self.generate_units(speed_x, speed_y)

    # generates formation of enemies according to the number of n
    # also sets y_start and x_end
    def generate_units(self, speed_x, speed_y, n=None, room_size=3):

        if n is None:
            n = self.n

        i = 0

        # creates rows of units
        while len(self.units) < n:

            # y-coordinate of ith row from bottom
            y = (
                END_Y
                - (i + 1) * (2 * self.size * HEIGHT + self.gap)
                + self.size * HEIGHT
                - self.bump
            )

            x = self.x_start
            space = WIDTH

            # creates row of units, leaving space at end to move
            while (
                space > room_size * (2 * self.size * WIDTH + self.gap)
                and not len(self.units) == n
            ):

                unit = self.type_unit(
                    x,
                    y,
                    speed_x,
                    speed_y,
                    self.size,
                    self.health,
                    self.points,
                )

                self.units.append(unit)

                space -= 2 * self.size * WIDTH + self.gap

                self.x_end = max(x, self.x_end)
                x += self.gap + 2 * self.size * WIDTH

            i += 1

        self.y_start = (
            END_Y
            - (i) * (2 * self.size * HEIGHT + self.gap)
            + self.size * HEIGHT
            - self.bump
        )

    # updates the state of the swarm
    def update(self):
        self.x_start += self.vel_x
        self.x_end += self.vel_x

        self.y_start += self.vel_y
        self.y_end += self.vel_y

        for unit in self.units:
            unit.update()

    # draws the graphics of the swarm
    def draw(self):

        for unit in self.units:
            unit.draw()

    # moves the swarm as a grid
    # also decides vertical movement based on the legacy tag
    def move_grid(self, legacy=False):

        # normal mode: move gradually down
        self.vel_y = 0
        if not legacy:
            self.vel_y = -self.speed_y

        if self.vel_x == 0:
            self.vel_x = self.speed_x

        if self.x_start <= START_X + self.size * WIDTH:
            self.vel_x = self.speed_x

            # legacy mode: jump down when reach edge.
            if legacy:
                self.vel_y = -(2 * self.size * HEIGHT + self.gap)

        elif self.x_end >= END_X - self.size * WIDTH:
            self.vel_x = -self.speed_x

            # legacy mode: jump down when reach edge.
            if legacy:
                self.vel_y = -(2 * self.size * HEIGHT + self.gap)

        self.move_units()

    # moves units when being moved as a grid by assigning grid vel_x and vel_y
    def move_units(self):

        for unit in self.units:
            unit.vel_x = self.vel_x
            unit.vel_y = self.vel_y

    # moves units of swarm when units move seperately
    def move_own(self):
        for unit in self.units:
            unit.move()

    # general move function
    def move(self, legacy=False):

        # chooses move function based on grid_mode variable
        # also passes legacy flag if relevant
        if self.grid_mode:
            self.move_grid(legacy)
        else:
            self.move_own()

    # checks if units in swarm reached the bottom of the screen
    def reach_end(self, player):

        for unit in self.units:
            unit.reach_end(player)

    # checks if units in swarm hit player
    def ram_player(self, player):

        for unit in self.units:
            unit.ram_player(player)

    # checks if units in swarm where hit by projectiles
    # return points and powerups awarded from all units killed
    def is_hit(self, projectiles):

        points = 0

        for unit in self.units:
            for j, projectile in enumerate(projectiles):
                if unit.is_hit(projectile):
                    if unit.dead:
                        points += unit.points
                    break

        powerups = self.get_powerups()

        # removes dead units
        self.units[:] = [i for i in self.units if not i.dead]

        # delcares swarm dead once all units are dead
        if len(self.units) == 0:
            self.dead = True

        return points, powerups

    # gets all the powerups dropped after units where killed
    def get_powerups(self):
        powerups = []

        for unit in self.units:
            if unit.dead and unit.powerup is not None:
                powerups.append(unit.powerup)

        return powerups

    # checks of the projectiles from units in the swarm has hit the player
    def hit_player(self, player):

        for unit in self.units:
            projectiles = unit.projectiles

            for j, projectile in enumerate(projectiles):
                # first checks if projectiles hit the bunker
                hit = player.bunker is not None and player.bunker.is_hit(projectile)
                if not hit:
                    player.is_hit(projectile)

    # calculates the space created by the swarm formation
    def get_bump(self):

        return self.y_end - self.y_start + self.size * 2 * HEIGHT + self.gap
