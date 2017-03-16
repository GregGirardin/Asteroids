__author__ = 'ggirardin'
from Constants import *
from Shape import *
from Vector import *
from Particles import *

class SmallAlien ():
  def __init__ (self):

    s = [(-2, 3, 10, 0, None),
         (-2,-3, 10, 0, None),
         (-2,-3, -2, 3, None)]

    self.shape = Shape (s, Point (0, random.random () * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 4), 0)
    self.spin = (random.random() - .5) / 100
    self.thrust = .01 + random.random() / 20
    self.shape.angle = (random.random() - .5) / 4
    self.collision = OBJECT_TYPE_NONE
    self.collisionRadius = 5
    self.velocity = Vector (0, 0)
    self.type = OBJECT_TYPE_ALIEN

  def pilot (self):
    if self.velocity.magnitude > 1:
      self.thrust = 0

  def update (self, e):
    self.pilot()

    self.shape.angle += self.spin
    self.velocity.impulse (Vector (self.thrust, self.shape.angle))
    self.shape.move (self.velocity)

    if self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int (10 + random.random() * 10)):
        p = SmokeParticle (Point (self.shape.p.x, self.shape.p.y),
                           Vector (random.random(), TAU * random.random ()).impulse (self.velocity),
                           20 + random.random() * 20,
                           (random.random() / 2 + 2))
        e.addObj (p)
      if self.collision == OBJECT_TYPE_CANNON:
        e.score += SMALL_ALIEN_POINTS

    if self.shape.offScreen() or self.collision != OBJECT_TYPE_NONE:
      return False

    return True

  def draw (self, canvas):
    self.shape.draw (canvas)

class BigAlien ():
  def __init__ (self):

    s = [(-10, 8, 15, 0, None),
         (-10,-8, 15, 0, None),
         (-10,-8,-10, 8, None)]

    self.shape = Shape (s, Point (0, random.random () * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 4), 0)
    self.spin = (random.random() - .5) / 200
    self.thrust = .01 + random.random() / 50
    self.shape.angle = (random.random() - .5) / 8
    self.collision = OBJECT_TYPE_NONE
    self.collisionRadius = 12
    self.velocity = Vector (0, 0)
    self.type = OBJECT_TYPE_ALIEN

  def pilot (self):
    if self.velocity.magnitude > 2:
      self.thrust = 0
      self.spin = 0

  def update (self, e):
    self.pilot()

    self.shape.angle += self.spin
    self.velocity.impulse (Vector (self.thrust, self.shape.angle))
    self.shape.move (self.velocity)

    if self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int (30 + random.random() * 10)):
        p = SmokeParticle (Point (self.shape.p.x, self.shape.p.y),
                           Vector (random.random(), TAU * random.random ()).impulse (self.velocity),
                           30 + random.random() * 20,
                           (random.random() / 2 + 2))
        e.addObj (p)
      if self.collision == OBJECT_TYPE_CANNON:
        e.score += BIG_ALIEN_POINTS

    if self.shape.offScreen() or self.collision != OBJECT_TYPE_NONE:
      return False

    return True

  def draw (self, canvas):
    self.shape.draw (canvas)