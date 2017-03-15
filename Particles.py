from Constants import *
import math
from Shape import *

class SmokeParticle ():
  def __init__ (self, p, v, ttl, size):
    self.velocity = v
    self.ttl = ttl
    self.spin = random.random() * 2 - 1
    s = [(-size,-size, size, size, None),
         (-size, size, size,-size, None)]
    self.shape = Shape (s, p)
    self.type = OBJECT_TYPE_NONE

  def update (self, e):
    self.shape.p.move (self.velocity)
    self.shape.angle += self.spin
    if self.ttl > 0:
      self.ttl -= 1
      return True
    else:
      return False

  def draw (self, canvas):
    self.shape.draw (canvas)

class CanonParticle ():
  def __init__ (self, p, v, ttl):
    self.velocity = v
    self.ttl = ttl
    self.spin = 0
    self.collisionRadius = 0
    size = 1
    s = [(-size,-size, size, size, None),
         (-size, size, size,-size, None)]
    self.shape = Shape (s, p)
    self.collision = OBJECT_TYPE_NONE
    self.type = OBJECT_TYPE_CANNON

  def update (self, e):
    self.shape.p.move (self.velocity)
    self.shape.angle += self.spin
    if self.ttl > 0 and self.collision == OBJECT_TYPE_NONE:
      self.ttl -= 1
      return True
    else:
      return False

  def draw (self, canvas):
    self.shape.draw (canvas)
