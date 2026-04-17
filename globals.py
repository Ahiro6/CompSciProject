import math
import threading
import stdaudio

# Game Constants and global functions
# Factor to be modified to scale all globals
# Globals also used to scale positions and speed in game
FACTOR = 1.5

FONT_SIZE = int(FACTOR * 20)

# actual width and height
SCREEN_WIDTH = FACTOR * 512
SCREEN_HEIGHT = FACTOR * 512

END_X = FACTOR * 1.0
END_Y = FACTOR * 1.0

START_X = FACTOR * -1.0
START_Y = FACTOR * -1.0

# relative width and height
WIDTH = END_X - START_X
HEIGHT = END_Y - START_Y

CENTER_X = (END_X + START_X) / 2.0
CENTER_Y = (END_Y + START_Y) / 2.0

FRAME_TIME = 10

# Image assets
# Characters
SPEEDSTER = "./assets/img/Characters/Speedster_.png"
TANK = "./assets/img/Characters/Tank_.png"
BOMBER = "./assets/img/Characters/Bomber_.png"
BASIC = "./assets/img/Characters/Basic_.png"
HERO = "./assets/img/Characters/Hero_.png"
STAFF = "./assets/img/Characters/Staff_.png"
BUNKER = "./assets/img/Characters/Bunker_faded_.png"
BUNKER_LOW = "./assets/img/Characters/Bunker_Low_faded_.png"

# Powerups
PU_SPEEDUP = "./assets/img/Powerups/powerup_speedup.png"
PU_HEALTH = "./assets/img/Powerups/powerup_health.png"
PU_BUNKER = "./assets/img/Powerups/powerup_bunker.png"
PU_SCATTERSHOT = "./assets/img/Powerups/powerup_scattershot.png"
PU_AREA = "./assets/img/Powerups/powerup_area.png"

# Backgrounds
HOME = "./assets/img/Backgrounds/home.png"
SKY = "./assets/img/Backgrounds/sky.png"
SKY_DEAD = "./assets/img/Backgrounds/dead_sky.png"
LOGO = "./assets/img/Backgrounds/logo.png"

# Projectiles
PROJECTILE = "./assets/img/Projectiles/explosion_blue.png"
P_SCATTERSHOT = "./assets/img/Projectiles/explosion_silver.png"
P_AREA = "./assets/img/Projectiles/explosion_red.png"
P_GREEN = "./assets/img/Projectiles/explosion_green.png"

# Icons
ICON_BULLET = "./assets/img/Icons/icon_bullet.png"
ICON_HEART = "./assets/img/Icons/icon_heart.png"
ICON_RELOAD = "./assets/img/Icons/icon_reload.png"
ICON_PAUSE = "./assets/img/Icons/icon_pause.png"

# Sound assets
S_RELOAD = "./assets/sound/reload"
S_POWERUP = "./assets/sound/powerup"

# Hero constants
H_SPEED = 0.015
H_SIZE = 0.05
H_ANGULAR_SPEED = 0.03
H_DAMAGE = 5
H_HEALTH = H_DAMAGE * 6
H_SPEED_PROJECTILE = 0.015
H_ANGLE = math.pi / 2
H_AMMO = 25
H_SPEED_RELOAD = 1

PLAYER_START_X = CENTER_X
PLAYER_START_Y = START_Y + 0.075 * HEIGHT

# Enemy constants
E_SIZE = 0.04
E_SPEED_X = 0.0025
E_SPEED_Y = 0.0005
E_HEALTH = H_DAMAGE
E_POINTS = 10
E_DAMAGE = H_DAMAGE
E_SPEED_PROJECTILE = H_SPEED_PROJECTILE
E_SPEED_RELOAD = 1.5

# Enemy powerup probs
E_SPEEDSTER_PU = 0.4
E_TANK_PU = 0.2
E_BOMBER_PU = 0.2
E_BASIC_PU = 0.05

# Enemy and Bunker factors
E_ARMOUR_FACTOR = 4
E_SPEED_X_FACTOR = 10
E_SPEED_Y_FACTOR = 5
E_JERK_PROB = 0.2

B_HEALTH_FACTOR = 2
B_SIZE_FACTOR = 3

# Game play constants
MAX_WAVES = 10


# thread allows to play sound
def play_sound(filename):
    t = threading.Thread(target=stdaudio.playFile, args=(filename,), daemon=True)
    t.start()
