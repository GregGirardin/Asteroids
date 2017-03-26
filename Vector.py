from Constants import *
from Shape import *
import math

# 0 is right, PI/2 is up, PI is left, -PI/2 is down

class Vector ():
  def __init__ (self, m, d):
    self.magnitude = m
    self.direction = d

  # add vector v
  def add (self, v, mod = True):
    cx = self.dx() + v.magnitude * math.cos (v.direction)
    cy = self.dy() - v.magnitude * math.sin (v.direction)
    magnitude = math.sqrt (cx ** 2 + cy ** 2)
    direction = dir (cx, cy)
    if mod:
      self.magnitude = magnitude
      self.direction = direction
    return Vector (magnitude, direction)

  # make vector a bit closer to aVec
  def adjust (self, aVec, weight = .1):
    assert weight <= 1.0

    adx = (aVec.dx() - self.dx()) * weight
    ady = (aVec.dy() - self.dy()) * weight

    cx = self.dx() + adx
    cy = self.dy() + ady

    self.magnitude = math.sqrt (cx ** 2 + cy ** 2)
    self.direction = dir (cx, cy)

  def dx (self): # x component of vector
    return self.magnitude * math.cos (self.direction)
  def dy (self): # y component of vector
    return -self.magnitude * math.sin (self.direction)

  def flipx (self):
    self.direction = dir (-self.dx(), self.dy())
  def flipy (self):
    self.direction = dir (self.dx(), -self.dy())

# compute direction from dx/dy
def dir (dx, dy):
  magnitude = math.sqrt (dx ** 2 + dy ** 2)

  if magnitude < EFFECTIVE_ZERO:
    direction = 0
  else:
    if math.fabs (dx) < EFFECTIVE_ZERO:
      if dy > 0:
        direction = -PI / 2
      else:
        direction = PI / 2
    elif dx > 0:
      direction = math.atan (-dy / dx)
    else:
      direction = PI + math.atan (-dy / dx)

  return direction

def dot (v1, v2):
  theta = math.fabs (v1.direction - v2.direction)
  return v1.magnitude * math.cos (theta)

# returns a vector that would connect 'f' to 't'
def vectorDiff (f, t):
  dx = t.dx() - f.dx()
  dy = t.dy() - f.dy()

  m = math.sqrt (dx ** 2 + dy ** 2)
  d = dir (dx, dy)
  return Vector (m, d)