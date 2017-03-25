from Constants import *
from Shape import *
from Vector import *
from Utils import *
from Particles import *
from Tkinter import *

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
    self.fuel = 100.0
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
      self.fuel -= self.accel * 2

    # bounce off walls
    if self.p.x < 0 or self.p.x > SCREEN_WIDTH:
      self.v.flipx()
      self.v.magnitude *= .8
    if self.p.y < 0 or self.p.y > SCREEN_HEIGHT:
      self.v.flipy()
      self.v.magnitude *= .8

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
      self.rounds -= .5
    else:
      self.cannon = 0

    # collisions
    if self.collision == OBJECT_TYPE_TANKER:
      self.fuel = 100.0
      self.rounds = 100.0
      self.collision = OBJECT_TYPE_NONE
    elif self.collision != OBJECT_TYPE_NONE:
      e.numShips -= 1
      for _ in  range (1, int (30 + random.random() * 10)):
        p = SmokeParticle (Point (self.p.x, self.p.y),
                           Vector (2 * random.random(), TAU * random.random ()).impulse (self.v),
                           random.uniform (20, 50),
                           random.uniform (3, 3.5))
        e.addObj (p)
      return False
    return True

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)

    canvas.create_rectangle (100,  5, 100 + 200, 7)
    fill = "red" if self.fuel < 20.0 else "black"
    canvas.create_rectangle (100, 10, 100 + 200 * self.fuel / 100, 15, fill=fill)
    fill = "red" if self.rounds < 20.0 else "black"
    canvas.create_rectangle (100, 20, 100 + 200 * self.rounds / 100, 25, fill=fill)
