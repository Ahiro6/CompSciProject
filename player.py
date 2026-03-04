import stddraw
import math
import time

from projectile import Projectile


class Character:

    def __init__(
        self,
        x,
        y,
        speed_x,
        speed_y,
        size,
        health,
        damage=0,
        speed_proj=0,
        angle=math.pi / 2,
    ):

        self.x = x
        self.y = y

        self.speed_x = speed_x
        self.speed_y = speed_y

        self.size = size
        self.max_health = health
        self.health = health

        self.vel_x = 0
        self.vel_y = 0

        self.damage = damage

        self.speed_proj = speed_proj
        self.angle = angle

        self.projectiles = []

        self.dead = False

    def move(self):

        pass

    def turn(self):

        pass

    def stop(self):

        self.vel_x = 0
        self.vel_y = 0

    def draw(self):

        self.x += self.vel_x
        self.y += self.vel_y

        self.x = min(max(self.x, self.size), 1.0 - self.size)
        self.y = min(max(self.y, self.size), 1.0 - self.size)

        if self.projectiles:
            p = self.projectiles[-1]
            if p.x > 1.0 or p.x < 0.0 or p.y > 1.0 or p.y < 0:
                self.projectiles.pop(-1)

            for i in self.projectiles:
                i.draw()

    def attack(self, Projectile_Type=Projectile):

        p = Projectile_Type(self.x, self.y, self.speed_proj, self.angle, self.damage)

        self.projectiles.append(p)

    def is_hit(self, projectile):
        x = projectile.x
        y = projectile.y

        if (
            (self.x - self.size) <= x
            and (self.x + self.size) >= x
            and (self.y - self.size) <= y
            and (self.y + self.size) >= y
        ):
            self.take_damage(projectile.damage)

            return True
        return False

    def take_damage(self, damage):

        self.health -= damage

        if self.health <= 0:
            self.dead = True

    def reset(self):

        self.health = self.max_health
        self.projectiles = []
        self.vel_x = 0
        self.vel_y = 0
        self.dead = False


class Player(Character):

    def __init__(
        self, x, y, speed_x, size, health, damage=0, speed_proj=0, angle=math.pi / 2
    ):

        super().__init__(x, y, speed_x, 0, size, health, damage, speed_proj, angle)

    def move(self, direction):
        
        if self.dead:
            return
        
        self.vel_x = -self.speed_x

        if direction == "R":
            self.vel_x = self.speed_x

    def turn(self, change):

        self.angle += change

        self.angle = max(min(self.angle, math.pi), 0)

    def draw(self):

        super().draw()

        stddraw.square(self.x, self.y, self.size)

        x_len = 2 * self.size * math.cos(self.angle)
        y_len = 2 * self.size * math.sin(self.angle)

        stddraw.line(self.x, self.y, self.x + x_len, self.y + y_len)


class Basic(Character):

    def __init__(self, x, y, speed_x, speed_y, size, health, points, damage=0):
        super().__init__(x, y, speed_x, speed_y, size, health, damage=damage)

        self.points = points

    def move(self):

        self.vel_y = -self.speed_y

        if self.vel_x == 0:
            self.vel_x = self.speed_x

        if self.x <= self.size:
            self.vel_x = self.speed_x
        elif self.x >= 1.0 - self.size * 2:
            self.vel_x = -self.speed_x

    def draw(self):

        super().draw()

        stddraw.square(self.x, self.y, self.size)

    def reach_end(self, player):

        if self.y - self.size <= 0.0:
            player.take_damage(player.health)
        
    def ram_player(self, player):
        
        if self.x + self.size < player.x - player.size or self.x - self.size > player.x + player.size:
            return
        elif self.y + self.size < player.y - player.size or self.y - self.size > player.y + player.size:
            return
        
        player.take_damage(player.health)
