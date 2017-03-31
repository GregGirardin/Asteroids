from Constants import *
from Shape import *
import math

class Point():
  def __init__ (self, x, y):
    self.x = x
    self.y = y

  def distanceTo (self, p): # p is another Point
     return math.sqrt ((self.x - p.x) ** 2 + (self.y - p.y) ** 2)

  def directionTo (self, p): # p is another point
    cx = p.x - self.x
    cy = p.y - self.y

    magnitude = math.sqrt (cx ** 2 + cy ** 2)

    if magnitude < EFFECTIVE_ZERO:
      direction = 0
    else:
      if math.fabs (cx) < EFFECTIVE_ZERO:
        if cy > 0:
          direction = -PI / 2
        else:
          direction = PI / 2
      elif cx > 0:
        direction = math.atan (-cy / cx)
      else:
        direction = PI + math.atan (-cy / cx)

    return direction

  def move (self, v): # v is a Vector PI/2 is up (-y)
    self.x += v.magnitude * math.cos (v.direction)
    self.y -= v.magnitude * math.sin (v.direction)
    return self

  def translate (self, p, theta): # p is location, theta is orientation.
    xr = self.x * math.cos (theta) - self.y * math.sin (theta) + p.x
    yr = -self.y * math.cos (theta) - self.x * math.sin (theta) + p.y
    return Point (xr, yr)

# 0 is right, PI/2 is up, PI is left, -PI/2 is down
class Vector ():
  def __init__ (self, m, d):
    self.magnitude = m
    self.direction = d

  # add vector v
  def add (self, v, mod = True, factor = 1.0):
    cx = self.dx() + v.magnitude * math.cos (v.direction) * factor
    cy = self.dy() - v.magnitude * math.sin (v.direction) * factor
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

  def dot (self, angle):
    theta = math.fabs (self.direction - angle)
    return self.magnitude * math.cos (theta)

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