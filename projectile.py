import math
import stddraw
import time
from picture import Picture

from globals import *

#Creating projectile image assets
PROJECTILE_PIC = Picture(PROJECTILE)
P_SCATTERSHOT_PIC = Picture(P_SCATTERSHOT)
P_AREA_PIC = Picture(P_AREA)
P_GREEN_PIC = Picture(P_GREEN)

"""
Parent projectile class and normal/basic projectile:
- x: x coordinate
- y: y coordinate
- speed: speed projectile moves at
- angle: angle projectile moves at
- damage: damage of projectile
- color: projectile color
- radius: determines size of projectile
- hit: if projectile hit a target
- hit_time: time that projectile hit something
- delay: time projectile takes to disappear after hitting target
- pic: projectile picture
"""
class Projectile:

    def __init__(self, x, y, speed, angle, damage):

        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.damage = damage

        self.color = stddraw.BLUE
        self.radius = 0.01 * FACTOR

        self.hit = False
        self.hit_time = None
        self.delay = 0.25

        self.pic = PROJECTILE_PIC

    #draws the graphics for the projectile
    def draw(self):
        stddraw.picture(self.pic, self.x, self.y, self.radius*5, self.radius*5)

    #updates the state of the projectile
    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        
        #removes projectile if out of screen
        if self.x > END_X or self.x < START_X or self.y > END_Y or self.y < START_Y:
            self.hit_time = time.time()
            self.hit = True

    #starts projectile's being hit process (exploding)
    def is_hit(self):

        #increase radius to look exploded
        self.radius *= 2
        self.hit = True
        self.speed = 0
        self.hit_time = time.time()

    #checks if projectile has disappeared after exploding and hitting a target
    def is_faded(self):

        curr_time = time.time()

        if self.hit_time is None:
            return False

        return (curr_time - self.hit_time) > self.delay

    #used to add projectile to its character's projectiles lits
    #also initiates abilities for certain special projectiles
    def add(self, projectiles):

        projectiles.append(self)

"""
Scattershot projectile: When shot spreads out into multiple projectiles
- scatter_num: number of projectiles after spreading out
- damage_nerf: nerfs the damage to balance powerup
"""
class Scattershot(Projectile):

    def __init__(self, x, y, speed, angle, damage, scatter_num=5):

        super().__init__(x, y, speed, angle, damage)

        self.damage_nerf = 0.5
        
        self.color = stddraw.GRAY
        self.radius = 0.01 * FACTOR
        self.damage = damage * self.damage_nerf

        self.scatter_num = scatter_num

        self.pic = P_SCATTERSHOT_PIC

    #same as parent, but also initiates scatter ability
    def add(self, projectiles):

        super().add(projectiles)

        self.scatter(projectiles)

    #initiates scatter ability
    def scatter(self, projectiles):

        i = self.scatter_num - 1
        angle = 0

        #adds projectiles left and right of initial center projectile
        while i > 0:
            angle += math.pi / (2 * self.scatter_num)

            #multiply with inverse of damage nerf to counter act double nerf
            r = Scattershot(
                self.x,
                self.y,
                self.speed,
                self.angle + angle,
                self.damage * (1/self.damage_nerf),
                self.scatter_num - 1,
            )
            l = Scattershot(
                self.x,
                self.y,
                self.speed,
                self.angle - angle,
                self.damage * (1/self.damage_nerf),
                self.scatter_num - 1,
            )

            projectiles.append(r)
            projectiles.append(l)

            i -= 2

"""
Area projectile class: Creates an area explosion on impact
- projectiles: the projectiles list the projectile belongs to
"""
class Area(Projectile):

    def __init__(self, x, y, speed, angle, damage):

        super().__init__(x, y, speed, angle, damage)

        self.color = stddraw.RED
        self.radius = 0.03 * FACTOR

        self.projectiles = None

        self.pic = P_AREA_PIC

    #same as parent, but also starts projectile's area ability
    def is_hit(self):
        super().is_hit()

        self.exploded()

    def add(self, projectiles):

        super().add(projectiles)

        self.projectiles = projectiles

    #initiates area explosion ability by adding multiple projectiles around it
    def exploded(self):

        if self.projectiles is not None:
            self.radius *= 1.5

            tl = Area(
                self.x - 2 * self.radius,
                self.y + 2.5 * self.radius,
                self.speed,
                self.angle,
                self.damage,
            )
            tr = Area(
                self.x + 2 * self.radius,
                self.y + 2.5 * self.radius,
                self.speed,
                self.angle,
                self.damage,
            )
            t = Area(
                self.x,
                self.y + 3 * self.radius,
                self.speed,
                self.angle,
                self.damage,
            )

            l = Area(
                self.x - 2 * self.radius,
                self.y + 1 * self.radius,
                self.speed,
                self.angle,
                self.damage,
            )
            r = Area(
                self.x + 2 * self.radius,
                self.y + 1 * self.radius,
                self.speed,
                self.angle,
                self.damage,
            )

            #starts hit process, but resets hit to false, so can hit other targets            
            t.is_hit(), tl.is_hit(), tr.is_hit(), l.is_hit(), r.is_hit()
            t.hit, tl.hit, tr.hit, l.hit, r.hit = False, False, False, False, False

            self.projectiles.extend([t, tl, tr, l, r])

"""
GreenProjectile Class: Exact same normal projectile but green
Note: Used for bomber, easier to differentiate projectiles
"""
class GreenProjectile(Projectile):
    
    def __init__(self, x, y, speed, angle, damage):
        
        super().__init__(x, y, speed, angle, damage)
        
        self.pic = P_GREEN_PIC