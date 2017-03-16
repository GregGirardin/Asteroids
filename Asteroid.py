from Constants import *
from Shape import *
from Vector import *
from Particles import *

class Asteroid ():
  def __init__ (self, radius):

    radii = 5 + int (random.random() * 5)
    r = []
    for _ in range (0, radii):
      r.append (radius + random.random() * 5 - 2)
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

    if random.random() < .5:
      initY = 0
    else:
      initY = SCREEN_HEIGHT


    self.shape = Shape (s, Point (random.random () * SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4, initY), 0)
    if initY <= 0:
      self.velocity = Vector (random.random() / 2, PI + PI * random.random())
    else:
      self.velocity = Vector (random.random() / 2, PI * random.random())

    self.spin = (random.random() - .5) / 10
    self.thrust = 0
    self.shape.angle = (random.random() - .5) / 8
    self.collision = OBJECT_TYPE_NONE
    self.collisionRadius = radius
    self.type = OBJECT_TYPE_ASTEROID

  def update (self, e):
    self.shape.angle += self.spin

    self.shape.p.move (self.velocity)

    if self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int (30 + random.random() * 10)):

        p = SmokeParticle (Point (self.shape.p.x, self.shape.p.y),
                           Vector (2 * random.random(), TAU * random.random()),
                           20 + random.random() * 10,
                           (random.random() / 2 + 3))
        e.addObj (p)

      if self.collisionRadius > 15:
        vector = random.random() * 2 * PI

        a = Asteroid (self.collisionRadius / 2)
        a.shape.p.x = self.shape.p.x + self.collisionRadius * math.cos (vector)
        a.shape.p.y = self.shape.p.y + self.collisionRadius * math.sin (vector)
        a.velocity = Vector (self.velocity.magnitude * 1.5, self.velocity.direction)
        e.addObj (a)

        a = Asteroid (self.collisionRadius / 2)
        a.shape.p.x = self.shape.p.x + self.collisionRadius * math.cos (vector + PI)
        a.shape.p.y = self.shape.p.y + self.collisionRadius * math.sin (vector + PI)
        a.velocity = Vector (self.velocity.magnitude * 1.5, self.velocity.direction + PI)
        e.addObj (a)
      if self.collision == OBJECT_TYPE_CANNON:
        e.score += ASTEROID_POINTS

    if self.shape.offScreen() or self.collision != OBJECT_TYPE_NONE:
      return False

    return True

  def draw (self, canvas):
    self.shape.draw (canvas)
