from Constants import *
import math
from Utils import *
from Shape import *

class SmokeParticle (WorldObject):
  def __init__ (self, p, v, ttl, size):
    self.ttl = ttl
    s = [(-size,-size, size, size, None),
         (-size, size, size,-size, None)]
    self.shape = Shape (s)
    WorldObject.__init__ (self, OBJECT_TYPE_NONE, p, 0, v, 0)
    if random.random() < .5:
      self.spin = 5
    else:
      self.spin = -5

  def update (self, e):
    WorldObject.update (self, e)

    if self.ttl > 0:
      self.ttl -= 1
      return True
    else:
      return False

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)

class CanonParticle (WorldObject):
  def __init__ (self, p, v, ttl, type = OBJECT_TYPE_CANNON):
    self.ttl = ttl
    size = 1
    s = [(-size,-size, size, size, None),
         (-size, size, size,-size, None)]
    self.shape = Shape (s)
    WorldObject.__init__ (self, type, p, 0, v, 2)

  def update (self, e):
    WorldObject.update (self, e)

    if self.ttl > 0:
      self.ttl -= 1
    if self.ttl <= 0:
      return False

    if self.collisionObj:
      t = self.collisionObj.type
      if t == OBJECT_TYPE_TORPEDO or t == OBJECT_TYPE_NONE or t == OBJECT_TYPE_T_CANNON:
        return True
      return False

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)

class Torpedo (WorldObject):
  def __init__ (self, p, v, ttl, radius = 5):
    self.ttl = ttl
    self.radius = radius
    self.age = 0
    WorldObject.__init__ (self, OBJECT_TYPE_TORPEDO, p, 0, v, radius)

  def update (self, e):
    WorldObject.update (self, e)

    self.age += 1

    if self.age > 20:
      p = CanonParticle (Point (self.p.x, self.p.y),
                         Vector (1 + 2 * random.random(), TAU * random.random ()).add (self.v),
                         random.uniform (20, 30),
                         type = OBJECT_TYPE_T_CANNON)
      e.addObj (p)

    if self.ttl > 0: # Torpedos go forever.
      self.ttl -= 1
      return True
    else:
      return False

  def draw (self, canvas, p, a):
    r = self.radius + random.uniform (-1, 1)
    canvas.create_oval (p.x - r, p.y - r, p.x + r, p.y + r)