from Constants import *
from Shape import *
import math, random


#
# 0 is right, PI/2 is up, PI is left, -PI/2 is down
#

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

  def dx (self): # x component of vector
    return self.magnitude * math.cos (self.direction)

  def dy (self): # y component of vector
    return self.magnitude * math.sin (self.direction)

def dot (v1, v2):
  theta = math.fabs (v1.direction - v2.direction)
  return v1.magnitude * math.cos (theta)

# returns a vector that would connect 'f' to 't'
def vectorDiff (f, t):
  dx = t.dx() - f.dx()
  dy = f.dy() - t.dy()

  m = math.sqrt (dx ** 2 + dy ** 2)

  if m < EFFECTIVE_ZERO:
    d = 0
  else:
    if math.fabs (dx) < EFFECTIVE_ZERO:
      if dy > 0:
        d = -PI / 2
      else:
        d = PI / 2
    elif dx > 0:
      d = math.atan (-dy / dx)
    else:
      d = PI + math.atan (-dy / dx)

  return Vector (m, d)