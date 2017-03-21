from Constants import *
from Shape import *
from Vector import *
from Utils import *
from Particles import *

class Ship (WorldObject):
  def __init__ (self):

    s = [(-5, 5, 10, 0, None),
         (-5,-5, 10, 0, None),
         (-5,-5, -5, 5, None)]
    self.shape = Shape (s)
    self.cannon = 0
    self.collision = OBJECT_TYPE_NONE
    self.numRoundsPF = 1
    self.rounds = 100.0
    self.fuel = 10.0
    WorldObject.__init__ (self,
                          OBJECT_TYPE_SHIP,
                          Point (SCREEN_WIDTH * .75, SCREEN_HEIGHT / 2),
                          PI,
                          None,
                          7)
  def update (self, e):
    WorldObject.update (self, e)

    if self.accel > 0:
      if self.accel > THRUST_MAX:
        self.accel = THRUST_MAX
      if self.fuel < 0:
        self.fuel = 0
        if self.accel > 0:
          self.accel = THRUST_LOW
      self.fuel -= self.accel

    # bounce off walls
    if self.p.x < 0:
      self.p.x = 0
      self.v.direction += PI # TBD
    elif self.p.x > SCREEN_WIDTH:
      self.p.x = SCREEN_WIDTH
    if self.p.y < 0:
      self.p.y = 0
      self.v.direction += PI # TBD
    elif self.p.y > SCREEN_HEIGHT:
      self.p.y = SCREEN_HEIGHT
      self.v.direction += PI # TBD

    if self.accel > 0:
      p = SmokeParticle (Point (self.p.x, self.p.y),
                         Vector (3, self.a + PI + random.uniform (-.25, .25)),
                         random.randrange (10, 20),
                         self.accel * 30 * random.uniform (.5, 1))
      e.addObj (p)
    if self.cannon > 0 and self.rounds > 0:
      p = CanonParticle (Point (self.p.x + 10 * math.cos (self.a),
                                self.p.y - 10 * math.sin (self.a)),
                         Vector (7, self.a), 120)
      e.addObj (p)
      self.cannon -= 1
      self.rounds -= .2
    else:
      self.cannon = 0

    # collisions
    if self.collision == OBJECT_TYPE_TANKER:
      self.fuel = 100.0
      self.numRounds = 1000
      self.collision = OBJECT_TYPE_NONE
    elif self.collision != OBJECT_TYPE_NONE:
      e.numShips -= 1
      for _ in  range (1, int (30 + random.random() * 10)):
        p = SmokeParticle (Point (self.p.x, self.p.y),
                           Vector (2 * random.random(), TAU * random.random ()).impulse (self.v),
                           30 + random.random() * 20,
                           (random.random() / 2 + 3))
        e.addObj (p)
      return False
    return True

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)
