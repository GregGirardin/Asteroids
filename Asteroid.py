from Constants import *
from Shape import *
from Vector import *
from Particles import *
from Utils import *

class Asteroid (WorldObject):
  def __init__ (self, radius):

    radii = 6 + int (random.random() * 5)
    r = []
    for _ in range (0, radii):
      r.append (radius + random.random() * 5)
    r.append (r [0])

    s = []
    theta = 0
    delTheta = 2 * PI / (len (r) - 1)
    for i in range (0, len (r) - 1):
      s.append ((r [i] * math.cos (theta),
                 r [i] * math.sin (theta),
                 r [i + 1] * math.cos (theta + delTheta),
                 r [i + 1] * math.sin (theta + delTheta),
                 0))
      theta += delTheta
    self.shape = Shape (s)

    if random.random() < .5:
      v = Vector (random.uniform (.2, 2), random.uniform (PI + PI * .2, PI + PI * .8))
      initY = -SCREEN_BUFFER + 1
    else:
      v = Vector (random.uniform (.2, 2), random.uniform (PI * .2, PI * .8))
      initY = SCREEN_HEIGHT + SCREEN_BUFFER - 1

    self.collision = OBJECT_TYPE_NONE
    WorldObject.__init__ (self, OBJECT_TYPE_ASTEROID,
                          Point (random.randrange (SCREEN_WIDTH * .1, SCREEN_WIDTH * .8), initY),
                          0, v, radius)
    self.spin = (random.random() - .5) / 10

  def update (self, e):
    WorldObject.update (self, e)

    if self.collisionObj:
      for _ in  range (1, int (10 + random.random() * 10)):
        p = SmokeParticle (Point (self.p.x, self.p.y),
                           Vector (2 * random.random(), random.uniform (0, TAU)),
                           random.randrange (10, 20),
                           random.uniform (3, 4))
        e.addObj (p)

      if self.collisionRadius > 15:
        vector = random.uniform (0, TAU)
        for v in (0, PI):
          a = Asteroid (self.collisionRadius / 2)
          a.p.x = self.p.x + self.collisionRadius * math.cos (vector + v)
          a.p.y = self.p.y + self.collisionRadius * math.sin (vector + v)
          a.velocity = Vector (self.v.magnitude * 1.5, self.v.direction + v)
          e.addObj (a)

      t = self.collisionObj.type
      if t == OBJECT_TYPE_CANNON or t == OBJECT_TYPE_T_CANNON or t == OBJECT_TYPE_TORPEDO:
        e.score += ASTEROID_POINTS

    if self.offScreen() or self.collisionObj:
      return False

    return True

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)
