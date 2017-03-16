from Constants import *
from Shape import *
import math, random

########################
# 0 is right, PI/2 is up, PI is left, -PI/2 is down
class Vector ():
  def __init__ (self, m, d):
    self.magnitude = m
    self.direction = d

  def impulse (self, v):
    cx = self.magnitude * math.cos (self.direction)
    cy = -self.magnitude * math.sin (self.direction)
    cx += v.magnitude * math.cos (v.direction)
    cy -= v.magnitude * math.sin (v.direction)

    self.magnitude = math.sqrt (cx ** 2 + cy ** 2)

    if self.magnitude < EFFECTIVE_ZERO:
      self.direction = 0
    else:
      if math.fabs (cx) < EFFECTIVE_ZERO:
        if cy > 0:
          self.direction = -PI / 2
        else:
          self.direction = PI / 2
      elif cx > 0:
        self.direction = math.atan (-cy / cx)
      else:
        self.direction = PI + math.atan (-cy / cx)

    return self

  #def randomize (self):
  #  return Vector (self.magnitude * (1 + random.random () / 10 - .1),
  #                 self.direction * random.random() / 10 - .1)

  def dx (self): # x component of vector
    return self.magnitude * math.cos (self.direction)

  def dy (self): # y component of vector
    return self.magnitude * math.sin (self.direction)
