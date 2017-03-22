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
  def __init__ (self, p, v, ttl):
    self.ttl = ttl
    size = 1
    s = [(-size,-size, size, size, None),
         (-size, size, size,-size, None)]
    self.shape = Shape (s)
    self.collision = OBJECT_TYPE_NONE
    WorldObject.__init__ (self, OBJECT_TYPE_CANNON, p, 0, v, 0)

  def update (self, e):
    WorldObject.update (self, e)

    if self.ttl > 0 and self.collision == OBJECT_TYPE_NONE:
      self.ttl -= 1
      return True
    else:
      return False

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)
