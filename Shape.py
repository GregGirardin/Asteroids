import random, math
from Vector import *
from Constants import *

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

class Line ():
  # a line is two verticies and a color
  def __init__ (self, p1, p2, color = None):
    self.p1 = p1
    self.p2 = p2
    self.color = color

  def translate (self, p, theta):
    p1r = self.p1.translate (p, theta)
    p2r = self.p2.translate (p, theta)
    return Line (p1r, p2r, self.color)

class Shape ():
  # a shape is a list of lines, x,y position, and a rotational angle
  def __init__ (self, s):
    # Create a shape from a list of coordinates
    # Each pair of coords forms a vertex
    # Each pair of vertices forms a line
    # Worry about color later
    self.lines = []

    for (x1, y1, x2, y2, c) in s:
      v1 = Point (x1, y1)
      v2 = Point (x2, y2)
      l = Line (v1, v2, c)
      self.lines.append (l)

  def translate (self, p, a):
    # make a list of translated Lines
    tlines = []

    for line in self.lines:
      tlines.append (line.translate (p, a))
    return tlines

  def draw (self, canvas, p, a, color = "black", width = 1):
    tlines = self.translate (p, a)

    for tline in tlines:
      canvas.create_line (tline.p1.x, tline.p1.y, tline.p2.x, tline.p2.y, fill = color, width = width)


  def move (self, v): # v is a vector
    self.p.x += v.magnitude * math.cos (v.direction)
    self.p.y -= v.magnitude * math.sin (v.direction)