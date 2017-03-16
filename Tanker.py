from Constants import *
from Shape import *
from Vector import *
from Particles import *



MAJ_OBJ_GET_TO_RENDEVOUS   = 1
MAJ_OBJ_WAIT_FOR_REFUELING = 2
MAJ_OBJ_DEPART             = 3

MIN_OBJ_ESTABLISH_VECTOR = 1
MIN_OBJ_ACCEL = 2
MIN_OBJ_DECEL = 3


'''
                   |
        2   ->3    |
                   |
             1<-   |
                   |
'''

class Tanker ():
  def __init__ (self):
    '''
    ******
     *      *
      *  T    *
     *     *
    ******
    '''

    s = [(-10,-10, 0,-10, None),
         (-10, 10, 0, 10, None),
         (  0,-10, 10, 0, None),
         (  0, 10, 10, 0, None),
         (-10,-10 ,-5, 0, None),
         (-10, 10 ,-5, 0, None)]

    # start from the right side, going left.
    self.shape = Shape (s, Point (SCREEN_WIDTH, random.random () * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 4), 0)
    self.velocity = Vector (0, 0) # The direction you're going (not facing)
    self.spin = 0
    self.thrust = .02
    self.shape.angle = PI + (random.random() - .5) / 8
    self.collision = OBJECT_TYPE_NONE
    self.collisionRadius = 12
    self.refueled = False
    # target x,y middle right of screen.. ship comes from right side.
    self.rendevous = Point (SCREEN_WIDTH / 2 + random.random() * SCREEN_WIDTH / 2,
                            SCREEN_HEIGHT / 2 + random.random() * SCREEN_HEIGHT / 4)

    self.maj_goal = None
    self.min_goal = None

    self.sleep = SHIP_SLEEP_CYCLES

    self.type = OBJECT_TYPE_TANKER

  def pilot (self):

    '''
    Goal
    '''
    # change spin and thrust based on goal

    if self.sleep > 0:
      self.sleep -= 1
      return


    if self.velocity.magnitude > 1:
      self.thrust = 0
      self.sleep = 100

  def update (self, e):
    self.pilot()

    self.shape.angle += self.spin
    self.velocity.impulse (Vector (self.thrust, self.shape.angle))
    self.shape.p.move (self.velocity)

    if self.thrust > 0:
      p = SmokeParticle (Point (self.shape.p.x, self.shape.p.y),
                         Vector (2, self.shape.angle + PI + random.random() / 2 - .25),
                         5 + random.random() * 5,
                         self.thrust * 30 * (random.random() / 2 + .5))
      e.addObj (p)

    if self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int (50 + random.random() * 10)):
        p = SmokeParticle (Point (self.shape.p.x, self.shape.p.y),
                           Vector (random.random(), TAU * random.random ()).impulse (self.velocity),
                           30 + random.random() * 20,
                           (random.random() / 2 + 3))
        e.addObj (p)

    if self.shape.offScreen() or self.collision != OBJECT_TYPE_NONE:
      return False

    return True

  def draw (self, canvas):
    self.shape.draw (canvas)

