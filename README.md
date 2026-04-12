_______________________________________________________________________________        
                                                                              
# Computer Science 214 Project: Space Invaders equivalent           
_______________________________________________________________________________

This is a group project for the module **Computer Science 214**

The group members are:
    - Adriaan Mostert (28897722) <br/>
    - (Enter details) <br/>
    - (Enter details) <br/>

<br/>
---------------------------------------------------------------------------------
## Arcane Invaders                                 
---------------------------------------------------------------------------------

This project emulates the classic space invaders game, but with a different theme

The minimum deliverables have been completed.

Beyond that, we have implemented the following possible extensions:
1. Graphics: Implemented sprites for the player, enemies, projectiles and powerups. Backgrounds are also included with a few icons aswell. The game follows a magical medieval theme, with a wizard player and monster enemies.
2. Sound: Created a sound function that plays a sound when certain actions happen. This includes reloading and collecting powerups
3. Highscore: A highscore function is created, which is stored in a txt file.
4. Enemie types: There are four different enemy types in total: <br/>
    - Basic: normal enemy that does nothing special <br/>
    - Bomber: an enemy that can shoot projectiles <br/>
    - Tank: an enemy with armour that can take extra projectile hits <br/>
    - Speedster: an enemy that moves extra fast and randomly changes direction. (Reaches bottom faster) <br/>
5. Missile types: There are four different projectile types: <br/>
    - Projectile: normal basic projectile <br/>
    - GreenProjectile: same as Projectile, but green, used for enemies <br/>
    - Scattershot: projectile splits up into multiple projectiles in 5 differrent directions (powerup) <br/>
    - Area: projectile creates a blast radius that can hit multiple enemies (powerup). <br/>
6. Powerups: There are 5 different powerup types that can be collected by the user: <br/>
    - Bunker: Provides the user with  a bunker<br/>
    - Area: Temporarily gives the user an area projectile<br/>
    - Scatter: Temporarily gives the user a scattershot projectile<br/>
    - Speedup: Temporarily decreases the player's shoot delay and increases the player's ammo<br/>
    - Health: Increases the player's health<br/>
7. Hitpoints/Extra lives: The player dies when its health gets depleted. The player starts with health that decrease as it gets hit with projectiles. The player's health increases again when the health powerup is collected. However, the player dies instantly when the enemies touches the player or reaches the bottom.
8. Bunkers: Bunkers can be achieved with a powerup. When the bunker spawns, it blocks enemy projectiles and protects the player. When the bunker hitpoints/health gets depleted, it gets destroyed.
9. Wave progression (Progressively harder levels): Each wave represents a level. The first four waves introduce the different kind of enemies. From there each wave gets progressively harder as the enemies present gets more and a combination of enemy types have to be faced.
10. Enemies counterattack: The enemies can counterattack the player by also shooting projectiles in the form of the bomber enemy.


The files/folders in this game belong in the following categories:
1. Python scripts
2. Assets
3. TXT file

<br/>
### Python Scripts

1. **game.py**: Handles the game functions and game loop
2. **globals.py**: Contains all global variables and functions
3. **main.py**: creates game object
4. **player.py**: Character classes (player and enemies)
5. **powerups.py**: Powerup classes that buffs the player
6. **projectile.py**: Projectiles used for attack
7. **swarm.py**: Swarm class that manages formation of units (enemies)

<br/>
### Assets

Assets are split up into images and sound:

**Images**:
1. Background
2. Characters
3. Icons
4. Powerups
5. Projectiles

**Sound**: all sounds in same folder

<br/>
### TXT file

The only txt file is the highscore.txt file that contains the highscore

