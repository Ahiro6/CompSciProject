from player import Basic


class Swarm:

    def __init__(
        self, n, size, speed_x, speed_y, health, points, damage, type_unit=Basic
    ):

        self.n = n
        self.size = size

        self.speed_x = speed_x
        self.speed_y = speed_y

        self.health = health
        self.points = points
        self.damage = damage

        self.units = []

        self.type_unit = type_unit

        self.generate_units()

        self.dead = False

    def generate_units(self):

        gap = self.size * 0.4

        i = 0

        y = 1.0 - (gap + self.size)
        while len(self.units) < self.n:

            y = 1.0 - (i + 1) * (2 * self.size + gap)

            x = gap + self.size
            space = 1.0

            while space > 4 * self.size + gap and not len(self.units) == self.n:

                unit = self.type_unit(
                    x,
                    y,
                    self.speed_x,
                    self.speed_y,
                    self.size,
                    self.health,
                    self.points,
                    damage=self.damage,
                )

                self.units.append(unit)

                space -= 2 * self.size + gap

                x += gap + 2 * self.size
            i += 1

    def draw(self):

        for unit in self.units:
            unit.draw()

    def move(self):

        for unit in self.units:
            unit.move()

    def reach_end(self, player):

        for unit in self.units:
            unit.reach_end(player)
    
    def ram_player(self, player):
        
        for unit in self.units:
            unit.ram_player(player)

    def is_hit(self, projectiles):

        used_projs = []

        points = 0

        for j, projectile in enumerate(projectiles):
            dead = -1
            for i, unit in enumerate(self.units):
                if unit.is_hit(projectile):
                    if unit.dead:
                        points += unit.points
                        dead = i
                        used_projs.append(j)

            if not dead == -1:
                self.units.pop(dead)

        if len(self.units) == 0:
            self.dead = True

        return points
