from globals import *

import stddraw
from picture import Picture
import time

from projectile import *

# Creating Powerup image assets
SPEEDUP_PIC = Picture(PU_SPEEDUP)
HEALTH_PIC = Picture(PU_HEALTH)
BUNKER_PIC = Picture(PU_BUNKER)
SCATTERSHOT_PIC = Picture(PU_SCATTERSHOT)
AREA_PIC = Picture(PU_AREA)

"""
Powerups parent class:
- size: length of center to edge, follows square shape
- x: x coordinate
- y: y coordinate
- speed: y speed that powerups drop at
- duration: time that powerup lasts (only applicable if powerup expires)
- collected: if collected by hero
- expired: if duration expired or dropped out of screen
- started: time that powerup effects started (time collected) - (only applicable if powerup expires)
- pic: powerup picture
"""


class Powerup:

    def __init__(self, size, x, y, speed=0.005, duration=10):

        self.collected = False
        self.expired = False
        self.size = size

        self.y = y
        self.x = x
        self.speed = speed * HEIGHT
        self.duration = duration
        self.started = None

        self.pic = None

    # used to buff player
    def buff(self, player):

        self.started = time.time()
        self.collected = True

        play_sound(S_POWERUP)

        # debuff player from old powerups, before assigning new
        player.debuff()
        player.powerup = self

    # reverses buffed effects (only implemented in powerups that do expire after duration)
    def reverse(self, player):

        pass

    # used to decide if powerups should expire
    def set_expired(self):

        if not self.collected:
            return

        curr_time = time.time()

        self.expired = (curr_time - self.started) > self.duration

    # updates powerup state
    def update(self):

        if self.collected or self.expired:
            return

        self.y -= self.speed

        self.reach_end()

    # draw powerup graphics
    def draw(self):

        if self.collected or self.expired:
            return

        stddraw.picture(self.pic, self.x, self.y, w=self.size * 2.5, h=self.size * 2.5)

    # checks if powerup is hit/collected by projectile
    def is_hit_projectile(self, projectile):

        if self.collected or self.expired:
            return False

        x = projectile.x
        y = projectile.y
        radius = projectile.radius

        if projectile.hit:
            return False

        elif self.x + self.size < x - radius or self.x - self.size > x + radius:
            return False

        elif self.y + self.size < y - radius or self.y - self.size > y + radius:
            return False

        projectile.is_hit()

        return True

    # checks if powerup is hit/collected by player
    def is_hit_player(self, player):

        if self.collected or self.expired:
            return False

        if (
            self.x + self.size < player.x - player.size
            or self.x - self.size > player.x + player.size
        ):
            return False
        elif (
            self.y + self.size < player.y - player.size
            or self.y - self.size > player.y + player.size
        ):
            return False

        return True

    # expires powerup if reaches end
    def reach_end(self):

        if self.collected or self.expired:
            return

        if self.y + self.size <= START_Y:
            self.expired = True


"""
Speedup powerup class: Gives extra ammo and decreases players shooting delay, which increases speed player can shoot at
- org_delay: orginial shooting delay before buff (used when reversing) 
- org_ammo: orginial ammo before buff (used when reversing) 
"""


class Speedup(Powerup):

    def __init__(self, size, x, y):

        super().__init__(size, x, y)

        self.pic = SPEEDUP_PIC

        self.org_delay = None
        self.org_ammo = None

    def buff(self, player):

        super().buff(player)

        self.org_delay = player.shoot_delay
        self.org_ammo = player.max_ammo

        player.shoot_delay = 0
        player.ammo = player.max_ammo * 2

    def reverse(self, player):

        super().reverse(player)

        player.shoot_delay = self.org_delay
        player.ammo = self.org_ammo


"""
Health powerup class: Increases player's health when collected

Note: Does not expire with duration
"""


class Health(Powerup):

    def __init__(self, size, x, y):

        super().__init__(size, x, y)

        self.pic = HEALTH_PIC

    # increases player health with a fraction of the player's max_health
    def buff(self, player):

        super().buff(player)

        player.health += player.max_health // 6

    def reverse(self, player):

        super().reverse(player)


"""
Bunker powerup class: Spawns a bunker the player can hide behind.
- Bunker: class of bunker character passed as argument to prevent circular import

Note: Does not expire with duration

"""


class BunkerPowerup(Powerup):

    def __init__(self, size, x, y, Bunker):

        super().__init__(size, x, y)

        self.pic = BUNKER_PIC
        self.Bunker = Bunker

    # passes bunker as argument to prevent circular import
    def buff(self, player):

        super().buff(player)

        player.bunker = self.Bunker(player.x, player.y, player.size, player.max_health)

    def reverse(self, player):

        super().reverse(player)


"""
ProjectilePowerup: Changes the player's projectile type to a specified type
- Projectile_Type: specified type of powerup
"""


class ProjectilePowerup(Powerup):

    def __init__(self, size, x, y, Projectile_Type=Projectile, pic=SCATTERSHOT_PIC):

        super().__init__(size, x, y)

        self.Projectile_Type = Projectile_Type

        self.pic = pic

    def buff(self, player):

        super().buff(player)

        player.Projectile_Type = self.Projectile_Type

    def reverse(self, player):

        super().reverse(player)

        player.Projectile_Type = Projectile
