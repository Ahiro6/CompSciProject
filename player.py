import stddraw
import math
import threading
import time
import random

from picture import Picture

from globals import *

from projectile import *
from powerups import *
import stdaudio

#Character image assets
HERO_PIC = Picture(HERO)
STAFF_PIC = Picture(STAFF)
BASIC_PIC = Picture(BASIC)
SPEEDSTER_PIC = Picture(SPEEDSTER)
BOMBER_PIC = Picture(BOMBER)
TANK_PIC = Picture(TANK)

#Projectile powerup image assets
SCATTERSHOT_PIC = Picture(PU_SCATTERSHOT)
AREA_PIC = Picture(PU_AREA)


"""
Character parent class for all characters:
- x: x coordinate of character
- y: y coordinate of character
- speed_x: the speed in the x axis
- speed_y: the speed in the y axis
- vel_x: the velocity/current speed in x axis
- vel_y: the velocity/current speed in y axis
- size: length of center to the edge of the character (determines hitbox)
- health: the current health
- max_health: the maximum starting health
- angular_speed: the speed the "turret" rotates at (if applicable)
- angular_vel: the current angular speed (if applicable)
- damage: the damage done by projectiles (if applicable)
- speed_proj: speed projectiles move at (if applicable)
- ammo: current ammo (if applicable)
- max_ammo: maximum possible ammo (if applicable)
- reload_time: time takes to reload ammo (if applicable)
- reloading: if character is busy reloading (if applicable)
- angle: angle of "turret" (if applicable)
- Projectile_Type: type of projectile (if applicable)
- projectiles: list of all current projectiles on screen (if applicable)
- pic: image asset
- dead: if character is dead (health = 0)
- last_shot: tracks last time character reloaded or shot projectile (if applicable)

Note: Hitbox of all characters is a square with a center at (x, y)
"""
class Character:

    def __init__(
        self,
        x,
        y,
        speed_x,
        speed_y,
        size,
        health,
        angular_speed=0,
        damage=0,
        speed_proj=0,
        ammo=0,
        reload_time=0,
        angle=math.pi / 2,
        Projectile_Type=None,
    ):

        self.x = x
        self.y = y

        self.speed_x = speed_x * WIDTH
        self.speed_y = speed_y * HEIGHT

        self.size = size * min(HEIGHT, WIDTH)
        self.max_health = health
        self.health = health

        self.vel_x = 0
        self.vel_y = 0

        self.damage = damage

        self.angular_speed = angular_speed
        self.angular_vel = 0

        self.speed_proj = speed_proj * HEIGHT
        self.angle = angle

        self.max_ammo = ammo
        self.ammo = ammo
        self.reload_time = reload_time

        self.Projectile_Type = Projectile_Type

        self.projectiles = []

        self.pic = None

        self.dead = False

        self.reloading = False
        self.last_shot = time.time()

    #sets the velocity and direction of the character
    def move(self):

        pass

    #sets the angular velocity of the character
    def turn(self):

        pass

    #stops character from moving
    def stop(self):

        self.vel_x = 0
        self.vel_y = 0

    #stops turret from turning
    def stop_angular(self):
        self.angular_vel = 0

    #draws the graphics of the character and its projectiles
    def draw(self):
        
        if self.projectiles:
            p = self.projectiles[-1]
            if p.x > END_X or p.x < START_X or p.y > END_Y or p.y < START_Y:
                self.projectiles.pop(-1)

            for i in self.projectiles:
                i.draw()
                
        stddraw.picture(self.pic, self.x, self.y, w=self.size * 3, h=self.size * 3)

    #updates the state of the character and its bullets
    def update(self):

        if self.dead:
            return

        curr_time = time.time()

        #removes projectiles if exploded/faded
        self.projectiles[:] = [p for p in self.projectiles if not p.is_faded()]

        self.x += self.vel_x
        self.y += self.vel_y

        self.angle += self.angular_vel

        #keeps x, y coordinates on screen
        self.x = min(max(self.x, START_X + self.size), END_X - self.size)
        self.y = min(max(self.y, START_Y + self.size), END_Y - self.size)

        self.angle = max(min(self.angle, math.pi), 0)

        #handles projectiles
        if self.projectiles:
            for i in self.projectiles:
                i.update()

        #handles reloading: reloads after time passed
        if self.reloading and (curr_time - self.last_shot) > self.reload_time:
            self.reload()

    #shoots a projectile
    def attack(self):

        if self.dead:
            return

        #prevents shooting
        if self.ammo == 0 or self.reloading:
            return

        x_len = 2 * self.size * math.cos(self.angle)
        y_len = 2 * self.size * math.sin(self.angle)

        p = self.Projectile_Type(
            self.x + x_len, self.y + y_len, self.speed_proj, self.angle, self.damage
        )
        p.add(self.projectiles)

        self.ammo -= 1

    #starts reloading by beginning time
    def start_reload(self):

        if self.dead:
            return
        
        if self.ammo == self.max_ammo:
            return

        self.reloading = True
        self.last_shot = time.time()

    #finishes reloading by setting ammo
    def reload(self):

        if not self.dead:

            self.ammo = self.max_ammo
            self.reloading = False

    #checks if character is hit by projectile
    def is_hit(self, projectile):

        x = projectile.x
        y = projectile.y
        radius = projectile.radius

        if projectile.hit:
            return False

        elif self.x + self.size < x - radius or self.x - self.size > x + radius:
            return False

        elif self.y + self.size < y - radius or self.y - self.size > y + radius:
            return False

        #character loses health based on projectile damage
        self.take_damage(projectile.damage)

        #set projectile to explode
        projectile.is_hit()

        return True

    #gives damage to character
    def take_damage(self, damage):

        self.health -= damage
        # play_sound(S_HIT1)
        
        #declares dead
        if self.health <= 0:
            self.dead = True
            
        self.health = max(self.health, 0)

"""
The Player class: character controller by user
- shoot_delay: delay between when projectiles can shoot
- org_shoot_delay: applicable for when debuffing
- org_Projectile_Type: applicable for when debuffing
- powerup: current collected powerup
"""
class Player(Character):

    def __init__(
        self,
        x,
        y,
        speed_x,
        size,
        health,
        angular_speed,
        damage,
        speed_proj,
        ammo,
        reload_time,
        angle=math.pi / 2,
        Projectile_Type=Projectile,
    ):

        #speed_y by default set to zero
        super().__init__(
            x,
            y,
            speed_x,
            0,
            size,
            health,
            angular_speed,
            damage,
            speed_proj,
            ammo,
            reload_time,
            angle,
            Projectile_Type,
        )

        self.shoot_delay = self.reload_time /4
        self.org_shoot_delay = self.shoot_delay
        self.org_Projectile_Type = Projectile_Type

        self.pic = HERO_PIC

        self.powerup = None

    #sets velocity based on given direction
    def move(self, direction):

        if self.dead:
            return

        self.vel_x = -self.speed_x

        if direction == "R":
            self.vel_x = self.speed_x

    #sets angular_velocity based on given direction
    def turn(self, direction):

        if self.dead:
            return

        self.angular_vel = self.angular_speed

        if direction == "R":
            self.angular_vel = -self.angular_speed

    #extended to draw the graphics of the turret for the player
    def draw(self):

        x_len = 2 * self.size * math.cos(self.angle)
        y_len = 2 * self.size * math.sin(self.angle)

        stddraw.setPenColor(stddraw.BOOK_RED)
        stddraw.setPenRadius(0.015)
        stddraw.line(self.x, self.y, self.x + x_len, self.y + y_len)
        stddraw.setPenRadius(stddraw._DEFAULT_PEN_RADIUS)
        
        stddraw.picture(STAFF_PIC, self.x + x_len, self.y + y_len, self.size, self.size)
        
        super().draw()
        

    #updates the state of the player
    def update(self):

        super().update()

        #handles the state of the powerups
        if self.powerup:
            self.powerup.set_expired()
            
            if self.powerup.expired:
                self.powerup.reverse(self)
                self.powerup = None

    #shoots a projectile if not reloading and with a delay
    def attack(self):
        
        curr_time = time.time()
        
        if not self.reloading and (curr_time - self.last_shot) > self.shoot_delay:
            super().attack()
            # play_sound(S_SHOOT)

            self.last_shot = time.time()
    
    #extended to play reload sound
    def start_reload(self):
        
        super().start_reload()
        
        play_sound(S_RELOAD)
    
    #resets character to starting attributes
    def reset(self):

        self.health = self.max_health
        self.projectiles = []
        self.vel_x = 0
        self.vel_y = 0
        self.dead = False
        self.ammo = self.max_ammo
        self.Projectile_Type = self.org_Projectile_Type
        self.shoot_delay = self.org_shoot_delay

    #resets effects of all powerup buffs
    #used when new powerup is collected before old one is expired
    def debuff(self):

        if self.ammo > self.max_ammo:
            self.ammo = self.max_ammo
        self.Projectile_Type = self.org_Projectile_Type
        self.shoot_delay = self.org_shoot_delay

"""
Basic class: acts as the normal/basic enemy class and the parent class for other enemy characters
- powerup_prob: probability the enemy drops a powerup on death
- points: points added to player score when killed
- powerup: the powerup being dropped if applicable

Note: all projectile variables are ignored because its not applicable
"""
class Basic(Character):

    def __init__(self, x, y, speed_x, speed_y, size, health, points, powerup_prob=0.1):
        super().__init__(x, y, speed_x, speed_y, size, health)

        self.points = points
        self.powerup_prob = powerup_prob

        self.pic = BASIC_PIC

        self.powerup = None

    #sets enemy velocity if moves on own and not part of grid
    def move(self):

        self.vel_y = -self.speed_y

        if self.vel_x == 0:
            self.vel_x = self.speed_x

        #turns character around if reach edge
        if self.x <= START_X + self.size:
            self.vel_x = self.speed_x
        elif self.x >= END_X - self.size:
            self.vel_x = -self.speed_x

    def draw(self):

        super().draw()

    #kills player to end game when reaches bottom of screen
    def reach_end(self, player):

        if self.y - self.size <= START_Y:
            player.take_damage(player.health)

    #kills player to end game if enemy collides with player
    def ram_player(self, player):

        if (
            self.x + self.size < player.x - player.size
            or self.x - self.size > player.x + player.size
        ):
            return
        elif (
            self.y + self.size < player.y - player.size
            or self.y - self.size > player.y + player.size
        ):
            return

        player.take_damage(player.health)

    #decides to whether to drop powerup and which
    def drop_powerup(self):

        num_powerups = 5

        opt_prob = random.random()

        if opt_prob < 1.0 / num_powerups:
            powerup = ProjectilePowerup(
                self.size * 0.75,
                self.x,
                self.y,
                Projectile_Type=Scattershot,
                pic=SCATTERSHOT_PIC,
            )
        elif opt_prob < 2.0 / num_powerups:
            powerup = ProjectilePowerup(
                self.size * 0.75, self.x, self.y, Projectile_Type=Area, pic=AREA_PIC
            )
        elif opt_prob < 3.0 / num_powerups:
            powerup = Bunker(self.size * 0.75, self.x, self.y)
        elif opt_prob < 4.0 / num_powerups:
            powerup = Health(self.size * 0.75, self.x, self.y)
        else:
            powerup = Speedup(self.size * 0.75, self.x, self.y)

        prob = random.random()

        if prob < self.powerup_prob:
            return powerup
        return None

    #extended from parent to assign powerup when applicable
    def take_damage(self, damage):

        super().take_damage(damage)

        if self.dead:
            self.powerup = self.drop_powerup()

"""
Bomber class: enemy that shoots projectile
- all required projectile variables added
"""
class Bomber(Basic):

    def __init__(
        self,
        x,
        y,
        speed_x,
        speed_y,
        size,
        health,
        points,
        powerup_prob=0.25,
        damage=5,
        speed_proj=0.01,
        ammo=1,
        reload_time=1.5,
        angle=-math.pi / 2,
        Projectile_Type=GreenProjectile,
    ):
        super().__init__(x, y, speed_x, speed_y, size, health, points, powerup_prob)

        self.damage = damage
        self.speed_proj = speed_proj * HEIGHT
        self.ammo = ammo
        self.max_ammo = ammo
        self.reload_time = reload_time
        self.angle = angle
        self.Projectile_Type = Projectile_Type

        self.pic = BOMBER_PIC

    def draw(self):
        super().draw()

    #updates Bomber state
    def update(self):
        super().update()

        self.angle = -math.pi / 2

        #handles bomber attacks
        if self.ammo > 0:
            self.attack()

        if self.ammo == 0 and not self.reloading:
            self.start_reload()

"""
Tank class: enemy with additional armour that can take damage
- armour_factor: determines armour health 
- armour_health: armour with multiple of health
"""
class Tank(Basic):

    def __init__(
        self,
        x,
        y,
        speed_x,
        speed_y,
        size,
        health,
        points,
        powerup_prob=0.25,
        armour_factor=3,
    ):
        super().__init__(x, y, speed_x, speed_y, size, health, points, powerup_prob)

        self.armour_health = health * armour_factor
        self.armour_factor = armour_factor

        self.pic = TANK_PIC

    def draw(self):

        super().draw()

    #extended from parent to give damage to armour before health
    def take_damage(self, damage):

        if self.armour_health > 0:
            self.armour_health -= damage

        else:
            super().take_damage(damage)

"""
Speedster class: enemy that can moves extra fast and changes direction randomly
- jerk_prob: probability that speedster changes direction
- speed_x_factor: factor that speed_x gets increased with
- speed_y_factor: factor that speed_y gets increased with
- speed: acts as speedster if true and a basic if false
"""
class Speedster(Basic):

    def __init__(
        self,
        x,
        y,
        speed_x,
        speed_y,
        size,
        health,
        points,
        powerup_prob=0.5,
        jerk_prob=0.05,
        speed_x_factor=6,
        speed_y_factor=2.5,
    ):
        super().__init__(x, y, speed_x, speed_y, size, health, points, powerup_prob)

        self.health *= 2
        self.max_health *= 2

        self.speed_x *= speed_x_factor
        self.speed_y *= speed_y_factor
        self.speed_y_factor = speed_y_factor
        self.speed_x_factor = speed_x_factor

        self.jerk_prob = jerk_prob

        self.speed = True

        self.pic = SPEEDSTER_PIC

    def draw(self):

        super().draw()

        # stddraw.picture(self.pic, self.x, self.y, self.size * 4, self.size * 4)

    #determines if speedster should change direction
    def random_jerk(self):

        prob = random.random()

        if prob < self.jerk_prob:
            self.vel_x = -self.vel_x

    #extended to handle random jerk
    def move(self):

        if self.speed:
            self.random_jerk()

        super().move()

    #extended to disable speedster on first hit
    def is_hit(self, projectile):

        hit = super().is_hit(projectile)

        if hit and self.speed:
            self.speed = False
            self.speed_x /= self.speed_x_factor
            self.vel_x /= self.speed_x_factor
            self.speed_y /= self.speed_y_factor
            self.vel_y /= self.speed_y_factor

        return hit
