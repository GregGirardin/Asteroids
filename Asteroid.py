from Particles import *
from Utils import *

class Asteroid (WorldObject):
  def __init__ (self, radius, iron = False):
    radii = 6 + random.randrange (0, 5)
    r = []
    for _ in range (0, radii):
      r.append (radius + random.uniform (0, 5))
    r.append (r [0])

    s = []
    theta = 0
    delTheta = 2 * PI / (len (r) - 1)
    for i in range (0, len (r) - 1):
      s.append ((r [i] * math.cos (theta), r [i] * math.sin (theta),
                 r [i + 1] * math.cos (theta + delTheta), r [i + 1] * math.sin (theta + delTheta),
                 0))
      theta += delTheta
    self.shape = Shape (s)

    if random.random() < .5:
      v = Vector (random.uniform (.2, 2), random.uniform (PI + PI * .2, PI + PI * .8))
      initY = -SCREEN_BUFFER + 1
    else:
      v = Vector (random.uniform (.2, 2), random.uniform (PI * .2, PI * .8))
      initY = SCREEN_HEIGHT + SCREEN_BUFFER - 1

    if iron == True:
      m = IRON_ASTEROID_MASS * radius
    else:
      m = ASTEROID_MASS * radius

    self.collision = OBJECT_TYPE_NONE
    WorldObject.__init__ (self,
                          OBJECT_TYPE_ASTEROID,
                          Point (random.randrange (SCREEN_WIDTH * .1, SCREEN_WIDTH * .8), initY),
                          0,
                          v,
                          radius,
                          mass = m)
    self.spin = random.uniform (-.05, .05)
    self.iron = iron

  def update (self, e):
    if self.offScreen():
      return False

    while self.colList:
      c = self.colList.pop(0)

      if c.o.type == OBJECT_TYPE_NONE:
        continue

      if (self.iron is True or (c.i.magnitude < SMALL_IMPULSE and c.o.weapon is False)) and c.o.type != OBJECT_TYPE_BH:
        # Newtonian billiard ball
        self.v.add (c.i, mod = True)
        if self.v.magnitude > SPEED_HI:
          self.v.magnitude = SPEED_HI
      else:
        for _ in range (1, random.randrange (10, 20)):
          p = SmokeParticle (Point (self.p.x, self.p.y), Vector (2 * random.random (), random.uniform (0, TAU)),
                             random.randrange (10, 20), random.uniform (3, 4))
          e.addObj (p)

        if self.colRadius > MIN_ASTEROID_RADIUS * 2:
          vector = random.uniform (0, TAU)
          r = self.colRadius / 2
          for v in (0, PI):
            a = Asteroid (r)
            a.p.x = self.p.x + r * math.cos (vector + v)
            a.p.y = self.p.y + r * math.sin (vector + v)
            a.velocity = Vector (self.v.magnitude * 1.5, self.v.direction + v)
            e.addObj (a)

        t = c.o.type
        if t == OBJECT_TYPE_CANNON or t == OBJECT_TYPE_T_CANNON or t == OBJECT_TYPE_TORPEDO:
          e.score += ASTEROID_POINTS
        return False

    WorldObject.update (self, e)
    return True

  def draw (self, canvas, p, a):
    width = 3 if self.iron is True else 1
    self.shape.draw (canvas, p, a, width = width)

def newAsteroid ():
  return Asteroid (random.uniform (10, 50), iron = True if random.random() < .2 else False)

class BlackHole (WorldObject):
  def __init__(self):
    self.radius = random.uniform (20, 50)
    self.collision = OBJECT_TYPE_NONE

    WorldObject.__init__ (self, OBJECT_TYPE_BH,
                          Point (-5, random.randrange (SCREEN_HEIGHT * .2, SCREEN_HEIGHT * .8)),
                          0, Vector (random.uniform (1.4, 3), random.uniform (-.5, .5)),
                          self.radius, mass = BH_MASS * self.radius, weapon = True)  # BH's destory everything.

  def update (self, e):
    if self.offScreen():
      return False

    WorldObject.update (self, e)

    for obj in e.objects:
      if obj is not self:
        dis = obj.p.distanceTo (self.p)
        dir = obj.p.directionTo (self.p)
        m = self.mass / (dis ** 2)
        obj.v.add (Vector (m, dir))
        if obj.v.magnitude > SPEED_VHI:
           obj.v.magnitude = SPEED_VHI

    return True

  def draw (self, canvas, p, a):
    canvas.create_oval (p.x - self.radius, p.y - self.radius, p.x + self.radius, p.y + self.radius, fill = "black")

def newBlackHole():
  return BlackHole()