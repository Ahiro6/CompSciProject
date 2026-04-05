import math
import threading
import stdaudio

#Game Constants and global functions
#Factor to be modified to scale all globals
#Globals also used to scale positions and speed in game
FACTOR = 1.5

FONT_SIZE =  int(FACTOR*20)

#actual width and height
SCREEN_WIDTH = FACTOR * 512
SCREEN_HEIGHT = FACTOR * 512

END_X = FACTOR * 1.0
END_Y = FACTOR * 1.0

START_X = FACTOR * -1.0
START_Y = FACTOR * -1.0

#relative width and height
WIDTH = END_X - START_X
HEIGHT = END_Y - START_Y

CENTER_X = (END_X + START_X) / 2.0
CENTER_Y = (END_Y + START_Y) / 2.0

FRAME_TIME = 10

#Image assets
#Characters
SPEEDSTER = "./assets/img/Characters/Speedster_.png"
TANK = "./assets/img/Characters/Tank_.png"
BOMBER = "./assets/img/Characters/Bomber_.png"
BASIC = "./assets/img/Basic_.png"
HERO = "./assets/img/Characters/Hero_.png"
STAFF = "./assets/img/Characters/Staff_.png"

#Powerups
PU_SPEEDUP = "./assets/img/Powerups/powerup_speedup.png"
PU_HEALTH = "./assets/img/Powerups/powerup_health.png"
PU_BUNKER = "./assets/img/Powerups/powerup_bunker.png"
PU_SCATTERSHOT = "./assets/img/Powerups/powerup_scattershot.png"
PU_AREA = "./assets/img/Powerups/powerup_area.png"

#Backgrounds
HOME = "./assets/img/Backgrounds/home.png"
SKY = "./assets/img/Backgrounds/sky.png"
SKY_DEAD = "./assets/img/Backgrounds/dead_sky.png"
LOGO = "./assets/img/Backgrounds/logo.png"

#Projectiles
PROJECTILE = "./assets/img/Projectiles/explosion_blue.png"
P_SCATTERSHOT = "./assets/img/Projectiles/explosion_silver.png"
P_AREA = "./assets/img/Projectiles/explosion_red.png"
P_GREEN = "./assets/img/Projectiles/explosion_green.png"

#Icons
ICON_BULLET = "./assets/img/Icons/icon_bullet.png"
ICON_HEART = "./assets/img/Icons/icon_heart.png"
ICON_RELOAD = "./assets/img/Icons/icon_reload.png"

#Sound assets
S_SHOOT = './assets/sound/shoot'
S_RELOAD = './assets/sound/reload'
S_HIT1 = './assets/sound/hit1'
S_HIT2 = './assets/sound/hit2'
S_POWERUP = './assets/sound/powerup'

#Hero constants
SPEED = 0.01
SIZE = 0.05
HEALTH = 30
ANGULAR_SPEED = 0.03
DAMAGE = 5
SPEED_PROJECTILE = 0.01
ANGLE = math.pi / 2
AMMO = 25
SPEED_RELOAD = 1

PLAYER_START_X = CENTER_X
PLAYER_START_Y = START_Y + 0.075 * HEIGHT

#thread allows to play sound
def play_sound(filename):
    t = threading.Thread(target=stdaudio.playFile, args=(filename,), daemon=True)
    t.start()