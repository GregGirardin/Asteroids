from Constants import *
from Shape import *
from Vector import *
from Particles import *

class Ship ():
  def __init__ (self):

    s = [(-5, 5, 10, 0, None),
         (-5,-5, 10, 0, None),
         (-5,-5, -5, 5, None)]

    self.shape = Shape (s, Point (SCREEN_WIDTH * .75, SCREEN_HEIGHT / 2))
    self.shape.angle = PI

    self.spin = 0.0
    self.thrust = 0.0
    self.cannon = 0
    self.collision = OBJECT_TYPE_NONE
    self.collisionRadius = 7
    self.numRounds = 1
    self.fuel = 100.0
    self.type = OBJECT_TYPE_SHIP

    self.velocity = Vector (0, 0)

  def update (self, e):
    self.fuel -= self.thrust
    self.shape.angle += self.spin

    if self.shape.angle < 0:
      self.shape.angle += TAU
    elif self.shape.angle > TAU:
      self.shape.angle -= TAU

    self.velocity.impulse (Vector (self.thrust, self.shape.angle))
    self.shape.p.move (self.velocity)

    # bounce off walls
    if self.shape.p.x < 0:
      self.shape.p.x = 0
      self.velocity.direction += PI # TBD
    elif self.shape.p.x > SCREEN_WIDTH:
      self.shape.p.x = SCREEN_WIDTH
    if self.shape.p.y < 0:
      self.shape.y = 0
      self.velocity.direction += PI # TBD
    elif self.shape.p.y > SCREEN_HEIGHT:
      self.shape.p.y = SCREEN_HEIGHT
      self.velocity.direction += PI # TBD

    if self.thrust > 0:
      p = SmokeParticle (Point (self.shape.p.x, self.shape.p.y),
                         Vector (3, self.shape.angle + PI + random.random() / 2 - .25),
                         10 + random.random() * 10,
                         self.thrust * 30 * (random.random() / 2 + .5))
      e.addObj (p)

    if self.cannon > 0:
      p = CanonParticle (Point (self.shape.p.x + 10 * math.cos (self.shape.angle),
                                self.shape.p.y - 10 * math.sin (self.shape.angle)),
                         Vector (7, self.shape.angle), 120)
      e.addObj (p)
      self.cannon -= 1

    if self.collision != OBJECT_TYPE_NONE:
      e.numShips -= 1
      for _ in  range (1, int (30 + random.random() * 10)):
        p = SmokeParticle (Point (self.shape.p.x, self.shape.p.y),
                           Vector (2 * random.random(), TAU * random.random ()).impulse (self.velocity),
                           30 + random.random() * 20,
                           (random.random() / 2 + 3))
        e.addObj (p)
      return False
    return True

  def draw (self, canvas):
    self.shape.draw (canvas)
