import keyboard
import stddraw
import time
import threading

from player import Player
from swarm import Swarm

SKY = stddraw.BOOK_LIGHT_BLUE
DEAD = stddraw.ORANGE


class Game:

    def __init__(self, player):

        self.player = player
        self.swarms = []
        self.background = SKY
        
        
        self.game_on = False
        self.live = False

        self.score = 0
        
        self.thread = threading.Thread(target=self.thread_task)
        

        try:
            with open("highscore.txt", "r") as f:
                content = f.read()

                if content.strip() == "":
                    self.highscore = 0
                else:
                    self.highscore = int(content)

        except FileNotFoundError:
            self.highscore = 0

    def game_keys(self, last_time=time.time(), cooldown=0.5):
        curr_time = time.time()

        if keyboard.is_pressed("a"):
            self.on_a_pressed()
        if keyboard.is_pressed("d"):
            self.on_d_pressed()
        if keyboard.is_pressed("space") and (curr_time - last_time) > cooldown:
            self.on_space_pressed()
            last_time = time.time()
        if keyboard.is_pressed("k"):
            self.on_k_pressed()
        if keyboard.is_pressed("l"):
            self.on_l_pressed()
        if keyboard.is_pressed("esc"):
            self.player.take_damage(self.player.health)

        keyboard.hook(self.on_released)

        return last_time

    def home_keys(self):
        if keyboard.is_pressed("space"):
            self.game_start()
        if keyboard.is_pressed("delete"):
            self.quit()

    def home(self):

        self.home_keys()

        stddraw.clear(stddraw.GRAY)

        stddraw.setPenColor(stddraw.PINK)
        stddraw.filledRectangle(0.125, 0.75, 0.75, 0.2)
        stddraw.setPenColor(stddraw.BLACK)

        stddraw.setFontFamily("Verdana")
        stddraw.setFontSize(24)
        stddraw.text(0.5, 0.9, "Welcome to the Game!")

        stddraw.setFontSize(20)
        stddraw.text(0.5, 0.8, "Shoot Aliens to Win!")
        stddraw.setFontSize(16)

        stddraw.text(0.5, 0.7, "Highscore: " + str(self.highscore))

        stddraw.setPenColor(stddraw.BOOK_LIGHT_BLUE)
        stddraw.filledRectangle(0.2, 0.15, 0.60, 0.4)
        stddraw.setPenColor(stddraw.BLACK)

        stddraw.setFontSize(16)
        stddraw.text(0.5, 0.5, "Controls")

        stddraw.text(0.5, 0.4, "Move: [A] - left | [D] - right")
        stddraw.text(0.5, 0.35, "Rotate: [K] - left | [L] - right")
        stddraw.text(0.5, 0.3, "Shoot: [Space]")
        stddraw.text(0.5, 0.25, "Quit Game: [esc]")
        stddraw.text(0.5, 0.2, "Close Window: [delete]")
        

        stddraw.setFontSize(20)
        stddraw.text(0.5, 0.05, "Press space to start")

    def game(self):

        self.game_keys()

        stddraw.clear(self.background)

        self.game_display()

        self.player.draw()

        self.swarms[:] = [i for i in self.swarms if not i.dead]

        self.wave_conditions()

        for swarm in self.swarms:

            swarm.move()
            self.score += swarm.is_hit(self.player.projectiles)
            swarm.draw()
            
            swarm.reach_end(self.player)
            swarm.ram_player(self.player)
    
            if self.player.dead:
                self.game_quit()

    def game_display(self):

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontSize(24)
        stddraw.text(0.15, 0.95, "Score: " + str(self.score))
        stddraw.text(0.75, 0.95, "Highscore: " + str(self.highscore))
        stddraw.text(0.15, 0.05, "Ammo: " + str(self.player.ammo))

        stddraw.setPenColor(stddraw.BLACK)

    def game_over_display(self):

        self.background = DEAD
        
        stddraw.setPenColor(stddraw.RED)
        stddraw.filledRectangle(0.125, 0.4, 0.75, 0.2)

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontSize(50)
        stddraw.text(0.5, 0.5, "GAME OVER")

        stddraw.setPenColor(stddraw.BLACK)

    def game_start(self):
        self.game_on = True
        
        self.player.reset()
    
        self.swarms = []
        self.score = 0
        self.background = SKY
        
        self.thread = threading.Thread(target=self.thread_task)

        self.create_swarm()

    def game_quit(self):
        
        self.player.stop()
        
        self.game_over_display()

        if self.score > self.highscore:
            self.highscore = self.score

            with open("highscore.txt", "w") as f:
                f.write(str(self.highscore))
                
        if not self.thread.is_alive():
            self.thread.start()
    
                
                
    def thread_task(self):
        
        time.sleep(2)
        
        self.game_on = False
        

    def start(self):
        self.live = True

        while self.live:

            if self.game_on:
                self.game()

            else:
                self.home()

            stddraw.show(100)
            
    def quit(self):
        
        self.live = False

    def create_swarm(self):

        swarm = Swarm(
            n=30, size=0.04, speed_x=0.01, speed_y=0.003, health=1, points=10, damage=10
        )

        self.swarms.append(swarm)

    def wave_conditions(self):

        if len(self.swarms) == 0:
            self.create_swarm()

    def on_space_pressed(self):
        self.player.attack()

    def on_a_pressed(self):
        self.player.move("L")

    def on_d_pressed(self):
        self.player.move("R")

    def on_k_pressed(self):
        self.player.turn(0.2)

    def on_l_pressed(self):
        self.player.turn(-0.2)

    def on_released(self, event):
        if event.event_type == keyboard.KEY_UP:
            self.player.stop()
