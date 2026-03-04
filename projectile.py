import math
import stddraw


class Projectile:

    def __init__(self, x, y, speed, angle, damage):

        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.damage = damage

    def draw(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # stddraw.setPenRadius(0.1)
        stddraw.point(self.x, self.y)
