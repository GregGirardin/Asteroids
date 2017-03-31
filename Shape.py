import random, math
from Vector import *
from Constants import *



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