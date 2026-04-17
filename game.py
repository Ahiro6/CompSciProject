import stddraw
import time
import threading
from picture import Picture

from player import Basic, Player, Tank, Speedster, Bomber
from swarm import Swarm
from globals import *

# Background image assets
SKY_PIC = Picture(SKY)
DEAD_PIC = Picture(SKY_DEAD)
HOME_PIC = Picture(HOME)
LOGO_PIC = Picture(LOGO)

# Icon image assets
BULLET_PIC = Picture(ICON_BULLET)
HEART_PIC = Picture(ICON_HEART)
RELOAD_PIC = Picture(ICON_RELOAD)
PAUSE_PIC = Picture(ICON_PAUSE)

"""
Game: handles all game processes
- player: player object controlled by user
- swarms: list of all active swarms
- powerups: list of all powerups on screen
- background: active game background
- help: true if help/guide screen should be displayed
- controls: true if controls screen should be displayed
- game_on: true if an active game is ongoing, else at home
- live: true if window is active
- score: current score of active game
- highscore: best score achieved so far
- wave: current wave game is on
- thread: executes game over process
- pause: stops/pauses the game by preventing updates for all objects
- legacy: flag that indicates whether game is run on the legacy version or the normal version.
- max_wave: Indicates the number of waves the player needs to complete to win. Only relevant in legacy version.
"""


class Game:

    def __init__(self, player, max_wave=15, legacy=False):

        self.player = player
        self.swarms = []
        self.powerups = []

        self.background = SKY

        self.help = False
        self.controls = False

        self.game_on = False
        self.live = False
        self.pause = False

        self.legacy = legacy

        self.score = 0

        self.thread = None

        # reads highscore from file
        try:
            with open("highscore.txt", "r") as f:
                content = f.read()

                if content.strip() == "":
                    self.highscore = 0
                else:
                    self.highscore = int(content)

        except FileNotFoundError:
            self.highscore = 0

        self.wave = 0
        self.max_wave = max_wave

    # handles keybinds for active game
    def game_keys(self):

        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            # prevent certain actions when paused, but allow others
            if not self.pause:
                if key == "a":
                    self.on_a_pressed()
                if key == "d":
                    self.on_d_pressed()
                if key == " ":
                    self.on_space_pressed()
                if key == "j":
                    self.on_j_pressed()
                if key == "l":
                    self.on_l_pressed()
                if key == "s":
                    self.on_s_pressed()
                if key == "k":
                    self.on_k_pressed()
                if key == "r":
                    self.on_r_pressed()
            if key == "\x1b":
                self.player.take_damage(self.player.health)
            if key == "\x7f":
                self.quit()
            if key == "p":
                self.pause = not self.pause

    # handles keybinds for home menu
    def home_keys(self):
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == " ":
                self.game_start()
            if key == "\x7f":
                self.quit()
            if key == "h":
                self.help = not self.help
                self.controls = False
            if key == "c":
                self.controls = not self.controls
                self.help = False

    # creates home screen
    def home(self):

        self.home_keys()

        stddraw.clear(stddraw.GRAY)

        stddraw.setFontFamily("Verdana")

        # background
        stddraw.picture(HOME_PIC, CENTER_X, CENTER_Y, WIDTH, HEIGHT)

        # logo
        stddraw.picture(
            LOGO_PIC, CENTER_X, CENTER_Y + 0.25 * HEIGHT, WIDTH * 0.85, HEIGHT * 0.35
        )

        # main menu
        if not self.help and not self.controls:
            self.main_screen()

        stddraw.setFontSize(FONT_SIZE)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(CENTER_X, START_Y + 0.05 * HEIGHT, "Press space to start")

        # help screen
        if self.help:
            self.help_screen()

        # controls screen
        if self.controls:
            self.controls_screen()

    # graphics for help screen
    def help_screen(self):
        start_y = 0.1125
        start_x = 0.025

        stddraw.setPenColor(stddraw.GRAY)
        stddraw.filledRectangle(
            START_X + (start_x) * WIDTH,
            START_Y + (start_y) * HEIGHT,
            0.95 * WIDTH,
            0.675 * HEIGHT,
        )
        stddraw.setPenColor(stddraw.DARK_GRAY)
        stddraw.filledRectangle(
            START_X + (start_x + 0.0125) * WIDTH,
            START_Y + (start_y + 0.0125) * HEIGHT,
            0.925 * WIDTH,
            0.65 * HEIGHT,
        )

        stddraw.setPenColor(stddraw.WHITE)

        stddraw.setFontSize(FONT_SIZE)
        stddraw.text(CENTER_X, START_Y + (start_y + 0.05 * 12.25) * HEIGHT, "Guide:")

        stddraw.setFontSize(int(FONT_SIZE * 0.8))
        stddraw.text(
            CENTER_X,
            START_Y + (start_y + 0.05 * 11.25) * HEIGHT,
            "The Goal of the game is to not die",
        )
        stddraw.text(
            CENTER_X,
            START_Y + (start_y + 0.05 * 9.75) * HEIGHT,
            "1. Shoot enemies (Remember to reload)",
        )
        stddraw.text(
            CENTER_X,
            START_Y + (start_y + 0.05 * 8.25) * HEIGHT,
            "2. Collected Powerups (Powerups expire and can't stack)",
        )
        stddraw.text(
            CENTER_X,
            START_Y + (start_y + 0.05 * 6.75) * HEIGHT,
            "3. There are different types of enemies",
        )
        stddraw.text(
            CENTER_X,
            START_Y + (start_y + 0.05 * 5.75) * HEIGHT,
            "(Normal, Tank, Speedster, Shooter)",
        )
        stddraw.text(
            CENTER_X,
            START_Y + (start_y + 0.05 * 4.25) * HEIGHT,
            "4. Survive as many waves as possible",
        )
        stddraw.text(
            CENTER_X,
            START_Y + (start_y + 0.05 * 2.75) * HEIGHT,
            "5. Don't let them reach the end!",
        )
        stddraw.text(
            CENTER_X, START_Y + (start_y + 0.05 * 1.25) * HEIGHT, "Close Help: [H]"
        )

        stddraw.setPenColor(stddraw.BLACK)
        stddraw.rectangle(
            START_X + 0.025 * WIDTH,
            START_Y + (start_y) * HEIGHT,
            0.95 * WIDTH,
            0.675 * HEIGHT,
        )
        stddraw.rectangle(
            START_X + 0.0375 * WIDTH,
            START_Y + (start_y + 0.0125) * HEIGHT,
            0.925 * WIDTH,
            0.65 * HEIGHT,
        )

    # graphics for controls screen
    def controls_screen(self):
        start_y = 0.1
        start_x = 0.15

        stddraw.setPenColor(stddraw.GRAY)
        stddraw.filledRectangle(
            START_X + (start_x) * WIDTH,
            START_Y + (start_y) * HEIGHT,
            0.7 * WIDTH,
            0.55 * HEIGHT,
        )
        stddraw.setPenColor(stddraw.DARK_GRAY)
        stddraw.filledRectangle(
            START_X + (start_x + 0.0125) * WIDTH,
            START_Y + (start_y + 0.0125) * HEIGHT,
            0.675 * WIDTH,
            0.525 * HEIGHT,
        )

        stddraw.setPenColor(stddraw.WHITE)

        stddraw.setFontSize(FONT_SIZE)
        stddraw.text(CENTER_X, START_Y + (start_y + 0.05 * 10) * HEIGHT, "Controls")

        stddraw.setFontSize(int(FONT_SIZE * 0.8))
        stddraw.text(
            CENTER_X,
            START_Y + (start_y + 0.05 * 8) * HEIGHT,
            "Move: [A] - left | [S] - stop | [D] - right",
        )
        stddraw.text(
            CENTER_X,
            START_Y + (start_y + 0.05 * 7) * HEIGHT,
            "Rotate: [J] - left | [K] -stop | [L] - right",
        )
        stddraw.text(CENTER_X, START_Y + (start_y + 0.05 * 6) * HEIGHT, "Reload: [R]")
        stddraw.text(
            CENTER_X, START_Y + (start_y + 0.05 * 5) * HEIGHT, "Shoot: [Space]"
        )
        stddraw.text(CENTER_X, START_Y + (start_y + 0.05 * 4) * HEIGHT, "Pause: [P]")
        stddraw.text(
            CENTER_X, START_Y + (start_y + 0.05 * 3) * HEIGHT, "Quit Game: [esc]"
        )
        stddraw.text(
            CENTER_X, START_Y + (start_y + 0.05 * 2) * HEIGHT, "Close Window: [delete]"
        )
        stddraw.text(
            CENTER_X, START_Y + (start_y + 0.05 * 1) * HEIGHT, "Close Controls: [C]"
        )

        stddraw.setPenColor(stddraw.BLACK)
        stddraw.rectangle(
            START_X + (start_x) * WIDTH,
            START_Y + (start_y) * HEIGHT,
            0.7 * WIDTH,
            0.55 * HEIGHT,
        )
        stddraw.rectangle(
            START_X + (start_x + 0.0125) * WIDTH,
            START_Y + (start_y + 0.0125) * HEIGHT,
            0.675 * WIDTH,
            0.525 * HEIGHT,
        )

    # graphics for main screen
    def main_screen(self):

        start_x = 0.3
        start_y = 0.15
        width = 0.4

        stddraw.setPenColor(stddraw.GRAY)
        stddraw.filledRectangle(
            START_X + (start_x) * WIDTH,
            START_Y + (start_y) * HEIGHT,
            width * WIDTH,
            0.25 * HEIGHT,
        )
        stddraw.setPenColor(stddraw.DARK_GRAY)
        stddraw.filledRectangle(
            START_X + (start_x + 0.0125) * WIDTH,
            START_Y + (start_y + 0.0125) * HEIGHT,
            (width - 0.025) * WIDTH,
            0.225 * HEIGHT,
        )

        stddraw.setFontSize(FONT_SIZE)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(
            CENTER_X,
            START_Y + (start_y + 0.2) * HEIGHT,
            "Highscore: " + str(self.highscore),
        )

        stddraw.setFontSize(int(FONT_SIZE * 0.8))
        stddraw.text(CENTER_X, START_Y + (start_y + 0.11125) * HEIGHT, "Help: [H]")
        stddraw.text(CENTER_X, START_Y + (start_y + 0.06125) * HEIGHT, "Controls: [C]")

        stddraw.setPenColor(stddraw.BLACK)
        stddraw.rectangle(
            START_X + (start_x) * WIDTH,
            START_Y + (start_y) * HEIGHT,
            width * WIDTH,
            0.25 * HEIGHT,
        )
        stddraw.rectangle(
            START_X + (start_x + 0.0125) * WIDTH,
            START_Y + (start_y + 0.0125) * HEIGHT,
            (width - 0.025) * WIDTH,
            0.225 * HEIGHT,
        )

    # handles game loop
    def game(self):

        # keybinds
        self.game_keys()
        # decides swarms to spawn
        self.wave_conditions()

        # HUD details
        stddraw.clear()
        self.game_display()

        # handles player updates and drawing
        if not self.pause:
            self.player.update()
        self.player.draw()

        # handles swarm updates and drawing
        if not self.pause:
            self.swarms[:] = [
                i for i in self.swarms if not i.dead
            ]  # removes dead swarms
            for swarm in self.swarms:

                swarm.move(self.legacy)
                swarm.update()

                # adds points and handles powerups after swarm is hit
                points, powerups = swarm.is_hit(self.player.projectiles)
                self.score += points
                self.powerups.extend(powerups)

                # handles player interaction with swarm
                swarm.reach_end(self.player)
                swarm.ram_player(self.player)
                swarm.hit_player(self.player)

        for swarm in self.swarms:

            swarm.draw()

        # handles powerup updates and drawing
        if not self.pause:
            self.powerups[:] = [
                i for i in self.powerups if not i.collected and not i.expired
            ]  # removes powerups if collected/expired
            for powerup in self.powerups:

                powerup.update()

                # checks if player made contact with powerup
                hit = False

                hit = hit or powerup.is_hit_player(self.player)

                # buffs if player made contact
                if hit:
                    powerup.buff(self.player)

        for powerup in self.powerups:

            powerup.draw()

        # quits game if player is dead
        if self.player.dead:
            self.game_quit()

        # ends game when player wins
        # only in legacy mode and when player completes the max_wave
        if self.legacy and self.wave == self.max_wave + 1:
            self.game_quit(win=True)

    # graphics for game HUD/overlay
    def game_display(self):

        # background
        stddraw.picture(self.background, CENTER_X, CENTER_Y, WIDTH, HEIGHT)

        self.icon(0.0125, 0.8875, f"""Wave: {self.wave}""")  # wave counter
        self.icon(0.0125, 0.7875, f"""Score: {self.score}""")  # score display
        self.icon(0.0125, 0.6875, f"""Best: {self.highscore}""")  # highscore display

        self.icon(0.65, 0.8875, "Pause: [P]", icon=PAUSE_PIC)  # pause option

        # indicates if reloading with icon
        ammo_pic = BULLET_PIC
        if self.player.reloading:
            ammo_pic = RELOAD_PIC

        self.icon(
            0.65, 0.0125, f"""Health: {self.player.health}""", icon=HEART_PIC
        )  # health bar
        self.icon(
            0.0125, 0.0125, f"""Ammo: {self.player.ammo}""", icon=ammo_pic
        )  # ammo indicator

        # displays current collected powerup
        if self.player.powerup is not None:
            stddraw.picture(
                self.player.powerup.pic,
                START_X + 0.07 * WIDTH,
                START_Y + 0.175 * HEIGHT,
                self.player.size * 2,
                self.player.size * 2,
            )

        stddraw.setPenColor(stddraw.BLACK)

    # general icon function
    def icon(self, start_x, start_y, text, icon=None):

        fontSize = int(FONT_SIZE * 0.8)

        width = len(text) / (1.1 * SCREEN_WIDTH / fontSize)
        offset = width * WIDTH / 2

        if icon:
            width += (0.05 * HEIGHT) / WIDTH
            offset += 0.05 * HEIGHT

        stddraw.setFontSize(fontSize)
        stddraw.setPenColor(stddraw.GRAY)
        stddraw.filledRectangle(
            START_X + (start_x) * WIDTH,
            START_Y + (start_y) * HEIGHT,
            width * WIDTH,
            0.10 * HEIGHT,
        )

        stddraw.setPenColor(stddraw.DARK_GRAY)
        stddraw.filledRectangle(
            START_X + (start_x + 0.0125) * WIDTH,
            START_Y + (start_y + 0.0125) * HEIGHT,
            (width - 0.025) * WIDTH,
            0.075 * HEIGHT,
        )

        if icon:
            stddraw.picture(
                icon,
                START_X + (start_x) * WIDTH + 0.05 * HEIGHT,
                START_Y + (start_y) * HEIGHT + 0.05 * HEIGHT,
                0.075 * HEIGHT,
                0.075 * HEIGHT,
            )

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(
            START_X + (start_x) * WIDTH + offset,
            START_Y + (start_y + 0.05) * HEIGHT,
            text,
        )

        stddraw.setPenColor(stddraw.BLACK)
        stddraw.rectangle(
            START_X + (start_x) * WIDTH,
            START_Y + (start_y) * HEIGHT,
            width * WIDTH,
            0.10 * HEIGHT,
        )
        stddraw.rectangle(
            START_X + (start_x + 0.0125) * WIDTH,
            START_Y + (start_y + 0.0125) * HEIGHT,
            (width - 0.025) * WIDTH,
            0.075 * HEIGHT,
        )

    # creates game over sign
    def game_over_display(self, win=False):

        text = "GAME OVER"
        color = stddraw.RED

        # changed if the player wins in legacy mode
        if win:
            text = "VICTORY"
            color = stddraw.GREEN

        if not win:
            self.background = DEAD_PIC

        stddraw.setPenColor(color)
        stddraw.filledRectangle(
            START_X + 0.125 * WIDTH, START_Y + 0.4 * HEIGHT, 0.75 * WIDTH, 0.2 * HEIGHT
        )

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontSize(int(FONT_SIZE * 2.5))
        stddraw.text(CENTER_X, CENTER_Y, text)

        stddraw.setPenColor(stddraw.BLACK)

    # sets initial variables for the start of the game
    def game_start(self):
        self.game_on = True

        self.player.reset()

        self.swarms = []
        self.powerups = []
        self.score = 0
        self.wave = 0
        self.background = SKY_PIC

        self.thread = threading.Thread(target=self.thread_task)

    # initiates end of game when character dies
    def game_quit(self, win=False):

        # stops character from moving
        self.player.stop()
        self.player.stop_angular()

        self.game_over_display(win=win)

        # updates highscore
        if self.score > self.highscore:
            self.highscore = self.score

            with open("highscore.txt", "w") as f:
                f.write(str(self.highscore))

        # returns to home when timer finished
        self.thread = threading.Thread(target=self.thread_task)
        self.thread.start()

    # thread task to return to home
    def thread_task(self):

        time.sleep(2)

        self.game_on = False

    # executed to start live game window
    def start(self):
        self.live = True

        while self.live:

            if self.game_on:
                self.game()

            else:
                self.home()

            stddraw.show(10)

    # ends live loop of window
    def quit(self):

        self.live = False

    # creates a swarm of enemies to be added to game
    def create_swarm(self, n, type=Basic, grid_mode=True, bump=0):

        swarm = Swarm(
            n=n,
            size=E_SIZE,
            speed_x=E_SPEED_X,
            speed_y=E_SPEED_Y,
            health=E_HEALTH,
            points=E_POINTS,
            type_unit=type,
            grid_mode=grid_mode,
            bump=bump,
        )

        self.swarms.append(swarm)

        return swarm.get_bump()

    # rules that decide what type of units/swarms to spawn
    def wave_conditions(self):

        if not len(self.swarms) == 0:
            return

        self.wave += 1

        # first 4 waves act as tutorial to introduce each enemy
        if self.wave == 1:
            self.create_swarm(16)
        elif self.wave == 2:
            self.create_swarm(3, type=Tank)
        elif self.wave == 3:
            self.create_swarm(2, type=Bomber)
        elif self.wave == 4:
            self.create_swarm(1, type=Speedster, grid_mode=False)

        # from wave 5 and on the game actually starts and gets progressively harder
        else:
            # sums bumps together to push swarms below the previous one
            bump = 0

            # speedsters spawn every 5th wave
            if self.wave % 5 == 0:
                bump = bump + self.create_swarm(
                    min(self.wave // 5, 6), type=Speedster, bump=bump, grid_mode=False
                )

            # bombers spawn every 3rd wave
            if self.wave % 3 == 0:
                bump = bump + self.create_swarm(
                    min(6, self.wave // 3 - 1), type=Bomber, bump=bump
                )

            # basics spawn every wave
            bump = bump + self.create_swarm(8 * min(self.wave // 5 + 1, 4), bump=bump)

            # tanks spawn every 2nd wave
            if self.wave % 2 == 0:
                bump = bump + self.create_swarm(
                    min(6, self.wave // 2 - 1), type=Tank, bump=bump
                )

    # when space is pressed the player attacks
    def on_space_pressed(self):
        self.player.attack()

    # when a is pressed the player moves left
    def on_a_pressed(self):
        self.player.move("L")

    # when d is pressed the player moves right
    def on_d_pressed(self):
        self.player.move("R")

    # when s is pressed the player stops moving
    def on_s_pressed(self):
        self.player.stop()

    # when j is pressed the turret turns left
    def on_j_pressed(self):
        self.player.turn("L")

    # when l is pressed the turret turns right
    def on_l_pressed(self):
        self.player.turn("R")

    # when k is pressed the turret stops turning
    def on_k_pressed(self):
        self.player.stop_angular()

    # when r is pressed the player reloads
    def on_r_pressed(self):
        self.player.start_reload()
