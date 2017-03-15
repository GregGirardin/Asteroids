from Constants import *
from Shape import *
from Vector import *
from Particles import *

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
    self.shape = Shape (s,
                        Point ( SCREEN_WIDTH, random.random () * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 4),
                        0)
    self.velocity = Vector (0, 0) # The direction you're going (not facing)
    self.spin = 0
    self.thrust = .01 + random.random() / 70
    self.shape.angle = PI + (random.random() - .5) / 8
    self.collision = OBJECT_TYPE_NONE
    self.collisionRadius = 12
    self.type = OBJECT_TYPE_TANKER

  def pilot (self):
    # change spin and thrust based on goal
    pass

  def update (self, e):
    self.shape.angle += self.spin
    self.velocity.impulse (Vector (self.thrust, self.shape.angle))

    self.shape.p.move (self.velocity)

    if self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int (50 + random.random() * 10)):
        p = SmokeParticle (self.shape.p,
                           # speed self.velocity.dx() + random.random() * 2 - 1,
                           # dir  self.velocity.dy() + random.random() * 2 - 1,
                           30 + random.random() * 10, # tanker should be a big explosion
                           (random.random() * 2 + 1))
        e.addObj (p)

    if self.shape.offScreen() or self.collision != OBJECT_TYPE_NONE:
      return False

    return True

  def draw (self, canvas):
    self.shape.draw (canvas)

