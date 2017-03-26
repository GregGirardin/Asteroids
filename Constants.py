SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_BUFFER = 20

NUM_SHIPS = 3
NUM_WAVES = 3

TANKER_SAFE_POINTS  = 300
SMALL_ALIEN_POINTS  = 200
BIG_ALIEN_POINTS    = 100
ASTEROID_POINTS     = 20

OBJECT_TYPE_NONE = 0
OBJECT_TYPE_SHIP = 1
OBJECT_TYPE_ALIEN = 2
OBJECT_TYPE_TANKER = 3
OBJECT_TYPE_ASTEROID = 4
OBJECT_TYPE_CANNON = 5
OBJECT_TYPE_AL_CANNON = 6
OBJECT_TYPE_TORPEDO = 7
OBJECT_TYPE_T_CANNON = 8

PI = 3.14159
TAU = 2 * PI
EFFECTIVE_ZERO = .00001

THRUST_LOW = .01 # adjust based on FPS, etc.
THRUST_MED = THRUST_LOW * 2
THRUST_HI  = THRUST_LOW * 3
THRUST_MAX = THRUST_LOW * 8

MAX_SPIN = .3
SPIN_DELTA = .025

HEUR_GO     = 1
HEUR_FACE   = 2
HEUR_STOP   = 3
HEUR_GOTO   = 4
HEUR_WAIT   = 5
HEUR_ATTACK = 6

OBJECT_DIST_FAR  = SCREEN_WIDTH / 3
OBJECT_DIST_MED  = SCREEN_WIDTH / 6
OBJECT_DIST_NEAR = SCREEN_WIDTH / 20

SPEED_SLOW  = .5
SPEED_MED   = 1.0
SPEED_HI    = 2.5

APPROACH_TYPE_SLOW = 1
APPROACH_TYPE_FAST = 2

EVENT_DISPLAY_COUNT = 100

ATTACK_INIT = 1
ATTACK_ALIGN = 2
ATTACK_SHOOT = 3

TX_RESOURCE_FUEL = 1 << 0
TX_RESOURCE_ROUNDS = 1 << 1
TX_RESOURCE_TORPEDOS = 1 << 2
TX_RESOURCE_ALL = 0x7


TORPEDO_DELAY = 50 # lots of particles, need to limit how fast we send these