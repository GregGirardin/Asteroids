SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_BUFFER = 20

NUM_SHIPS = 3
NUM_WAVES = 3

SMALL_ALIEN_POINTS  = 200
BIG_ALIEN_POINTS    = 100
ASTEROID_POINTS     = 20

OBJECT_TYPE_NONE = 0
OBJECT_TYPE_SHIP = 1
OBJECT_TYPE_ALIEN = 2
OBJECT_TYPE_ASTEROID = 3
OBJECT_TYPE_CANNON = 4
OBJECT_TYPE_TANKER = 5

PI = 3.14159
TAU = 2 * PI
EFFECTIVE_ZERO = .00001

THRUST_LOW = .01 # adjust based on FPS, etc.
THRUST_MED = THRUST_LOW * 2
THRUST_HI  = THRUST_LOW * 3
THRUST_MAX = THRUST_LOW * 8

MAX_SPIN = .3
SPIN_DELTA = .025

HEUR_GOTO   = 1
HEUR_WAIT   = 2
HEUR_ATTACK = 3

OBJECT_DIST_FAR  = SCREEN_WIDTH / 3
OBJECT_DIST_MED  = SCREEN_WIDTH / 5
OBJECT_DIST_NEAR = SCREEN_WIDTH / 20

SPEED_SLOW  = 1.0
SPEED_MED   = 2.0
SPEED_HI    = 4.0

APPROACH_TYPE_SLOW = 1
APPROACH_TYPE_FAST = 2

NEW_WAVE_FLAG = 1
GAME_OVER_FLAG = 2
EVENT_DISPLAY_COUNT = 200