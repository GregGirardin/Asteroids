from Constants import *
from Shape import *
from Vector import *
from Particles import *
from Utils import *

class Asteroid (WorldObject):
  def __init__ (self, radius, iron = False):

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
    self.spin = (random.random() - .5) / 10
    self.iron = iron

  def update (self, e):

    if self.collisionObj:
      c = self.collisionObj

      if self.iron is True:
        # Newtonian billiard ball
        self.collisionObj = None
        dirToUs = c.p.directionTo (self.p)
        colSpeed = c.v.dot (dirToUs) + self.v.dot (dirToUs + PI) # velocity towards each other.
        mag = colSpeed * c.mass / self.mass
        self.v.add (Vector (mag, dirToUs), mod = True)
        if self.v.magnitude > SPEED_HI:
          self.v.magnitude = SPEED_HI
        # is the collision object also solid
        if (c.type == OBJECT_TYPE_ASTEROID and c.iron is True) or c.type == OBJECT_TYPE_TORPEDO:
          c.collisionObj = None
          mag = colSpeed * self.mass / c.mass
          c.v.add (Vector (mag, dirToUs + PI), mod = True)
          if c.v.magnitude > SPEED_HI:
            c.v.magnitude = SPEED_HI
          # We handled both collisions here

          # move them away from each other if necessary
          minDistance = self.collisionRadius + c.collisionRadius + 2 # colSpeed * 2
          actDistance = self.p.distanceTo (c.p)
          if actDistance < minDistance:
            adjustment = minDistance - actDistance
            if self.mass < c.mass: # move the lighter one
              self.p.move (Vector (adjustment, dirToUs))
            else:
              c.p.move (Vector (adjustment, dirToUs - PI))
      else:
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

        t = c.type
        if t == OBJECT_TYPE_CANNON or t == OBJECT_TYPE_T_CANNON or t == OBJECT_TYPE_TORPEDO:
          e.score += ASTEROID_POINTS

    if self.offScreen() or self.collisionObj:
      return False

    WorldObject.update (self, e)
    return True

  def draw (self, canvas, p, a):
    width = 3 if self.iron is True else 1
    self.shape.draw (canvas, p, a, width = width)
