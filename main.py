#!/usr/bin/python

from Tkinter import *
import time, math, random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
NUM_SHIPS = 3

SMALL_ALIEN_POINTS = 50
BIG_ALIEN_POINTS = 20
ASTEROID_POINTS = 5

OBJECT_TYPE_NONE = 0
OBJECT_TYPE_SHIP = 1
OBJECT_TYPE_ALIEN = 2
OBJECT_TYPE_ASTEROID = 3
OBJECT_TYPE_CANNON = 4
OBJECT_TYPE_TANKER = 5

PI = 3.14159

respawn = False

class Vertex ():
  # a vertex is an x,y offset relative to the center of a shape
  def __init__ (self, x, y):
    self.x = x
    self.y = y
  def translate (self, xpos, ypos, theta):
    xr = self.x * math.cos (theta) - self.y * math.sin (theta) + xpos
    yr = self.y * math.cos (theta) + self.x * math.sin (theta) + ypos
    return Vertex (xr, yr)

class Line ():
  # a line is two verticies and a color
  def __init__ (self, v1, v2, color=None):
    self.v1 = v1
    self.v2 = v2
    self.color = color

  def translate (self, xpos, ypos, theta):
    v1r = self.v1.translate (xpos, ypos, theta)
    v2r = self.v2.translate (xpos, ypos, theta)
    return Line (v1r, v2r, self.color)

class Shape ():
  # a shape is a list of lines, x,y position, and a rotational angle
  def __init__ (self, s, x = 0, y = 0, a = 0):
    # create a shape from a list of coordinates
    # each pair of coords forms a vertex
    # each pair of vertices forms a line
    # worry about color later
    self.lines = []
    self.angle = a
    self.x = x
    self.y = y

    for (x1, y1, x2, y2, c) in s:
      v1 = Vertex (x1, y1)
      v2 = Vertex (x2, y2)
      l = Line (v1, v2, c)
      self.lines.append (l)

  def translate (self):
    # make a list of translated Lines
    tlines = []

    for line in self.lines:
      tlines.append (line.translate (self.x, self.y, self.angle))
    return tlines

  def draw (self, canvas):
    tlines = self.translate ()

    for tline in tlines:
      canvas.create_line (tline.v1.x, tline.v1.y, tline.v2.x, tline.v2.y)

class Ship ():
  def __init__ (self):

    s = [(-5, 5, 10, 0, None),
         (-5,-5, 10, 0, None),
         (-5,-5, -5, 5, None)]

    self.shape = Shape (s, SCREEN_WIDTH * .75, SCREEN_HEIGHT / 2, 0)
    self.shape.angle = PI
    self.dx = 0
    self.dy = 0
    self.spin = 0
    self.thrust = 0.0
    self.cannon = 0
    self.collision = OBJECT_TYPE_NONE
    self.collisionRadius = 7
    self.numRounds = 1
    self.fuel = 100.0
    self.type = OBJECT_TYPE_SHIP

  def update (self, e):
    self.fuel -= self.thrust
    self.shape.angle += self.spin

    if self.shape.angle < 0:
      self.shape.angle = 2 * PI
    elif self.shape.angle > 2 * PI:
      self.shape.angle = 0

    self.dx += self.thrust * math.cos (self.shape.angle)
    self.dy += self.thrust * math.sin (self.shape.angle)

    self.shape.x += self.dx
    self.shape.y += self.dy

    # self.dx *= .99 # resistance
    # self.dy *= .99

    if self.shape.x < 0:
      self.shape.x = 0
      self.dx = -self.dx / 2
    elif self.shape.x > SCREEN_WIDTH:
      self.dx = -self.dx / 2
      self.shape.x = SCREEN_WIDTH
    if self.shape.y < 0:
      self.shape.y = 0
      self.dy = -self.dy / 2
    elif self.shape.y > SCREEN_HEIGHT:
      self.shape.y = SCREEN_HEIGHT
      self.dy = -self.dy / 2

    if self.thrust > 0:
      p = SmokeParticle (self.shape.x,
                         self.shape.y,
                         3 * math.cos (self.shape.angle + PI) + random.random() - .5,
                         3 * math.sin (self.shape.angle + PI) + random.random() - .5,
                         20 + random.random() * 10,
                         self.thrust * 10 * (random.random() / 2 + .5))
      e.addObj (p)

    if self.cannon > 0:
      # spawn canon far enough from ship so we don't collide with it
      p = CanonParticle (self.shape.x + 5 * math.cos (self.shape.angle),
                         self.shape.y + 5 * math.sin (self.shape.angle),
                         self.dx + 7 * math.cos (self.shape.angle),
                         self.dy + 7 * math.sin (self.shape.angle),
                         120)
      e.addObj (p)
      self.cannon -= 1

    if self.collision != OBJECT_TYPE_NONE:
      e.numShips -= 1
      for _ in  range (1, int (40 + random.random() * 10)):
        p = SmokeParticle (self.shape.x,
                           self.shape.y,
                           self.dx + random.random() - .5,
                           self.dy + random.random() - .5,
                           30 + random.random() * 20,
                           (random.random() / 2 + 3))
        e.addObj (p)
      return False
    return True

  def draw (self, canvas):
    self.shape.draw (canvas)

class SmokeParticle ():
  def __init__ (self, x, y, dx, dy, ttl, size):
    self.dx = dx
    self.dy = dy
    self.ttl = ttl
    self.spin = random.random() * 2 - 1
    p = [(-size,-size, size, size, None),
         (-size, size, size,-size, None)]
    self.shape = Shape (p, x, y, 0)
    self.type = OBJECT_TYPE_NONE

  def update (self, e):
    self.shape.x += self.dx
    self.shape.y += self.dy
    self.shape.angle += self.spin
    if self.ttl > 0:
      self.ttl -= 1
      return True
    else:
      return False

  def draw (self, canvas):
    self.shape.draw (canvas)

class CanonParticle ():
  def __init__ (self, x, y, dx, dy, ttl):
    self.dx = dx
    self.dy = dy
    self.ttl = ttl
    self.spin = 0
    self.collisionRadius = 0
    size = 1
    p = [(-size,-size, size, size, None),
         (-size, size, size,-size, None)]
    self.shape = Shape (p, x, y, 0)
    self.collision = OBJECT_TYPE_NONE
    self.type = OBJECT_TYPE_CANNON

  def update (self, e):
    self.shape.x += self.dx
    self.shape.y += self.dy
    self.shape.angle += self.spin
    if self.ttl > 0 and self.collision == OBJECT_TYPE_NONE:
      self.ttl -= 1
      return True
    else:
      return False

  def draw (self, canvas):
    self.shape.draw (canvas)

class SmallAlien ():
  def __init__ (self):

    s = [(-2, 3, 10, 0, None),
         (-2,-3, 10, 0, None),
         (-2,-3, -2, 3, None)]

    self.shape = Shape (s, 0, random.random() * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 4, 0)
    self.dx = 0
    self.dy = 0
    self.spin = (random.random() - .5) / 100
    self.thrust = .01 + random.random() / 20
    self.shape.angle = (random.random() - .5) / 4
    self.collision = OBJECT_TYPE_NONE
    self.collisionRadius = 5
    self.type = OBJECT_TYPE_ALIEN

  def update (self, e):
    self.shape.angle += self.spin
    self.dx += self.thrust * math.cos (self.shape.angle)
    self.dy += self.thrust * math.sin (self.shape.angle)

    self.shape.x += self.dx
    self.shape.y += self.dy

    self.dx *= .99 # resistance
    self.dy *= .99

    if self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int(10 + random.random() * 10)):
        p = SmokeParticle (self.shape.x,
                           self.shape.y,
                           self.dx + random.random() - .5,
                           self.dy + random.random() - .5,
                           20 + random.random() * 20,
                           (random.random() / 2 + 2))
        e.addObj (p)
      if self.collision == OBJECT_TYPE_CANNON:
        e.score += SMALL_ALIEN_POINTS

    if self.shape.x < 0 or self.shape.x > SCREEN_WIDTH + 20 or \
       self.shape.y < 0 or self.shape.y > SCREEN_HEIGHT + 20 or \
       self.collision != OBJECT_TYPE_NONE:
      return False

    return True

  def draw (self, canvas):
    self.shape.draw (canvas)

class BigAlien ():
  def __init__ (self):

    s = [(-10, 8, 15, 0, None),
         (-10,-8, 15, 0, None),
         (-10,-8,-10, 8, None)]

    self.shape = Shape (s, 0, random.random() * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 4, 0)
    self.dx = 0
    self.dy = 0
    self.spin = (random.random() - .5) / 200
    self.thrust = .01 + random.random() / 50
    self.shape.angle = (random.random() - .5) / 8
    self.collision = OBJECT_TYPE_NONE
    self.collisionRadius = 12
    self.type = OBJECT_TYPE_ALIEN

  def update (self, e):
    self.shape.angle += self.spin
    self.dx += self.thrust * math.cos (self.shape.angle)
    self.dy += self.thrust * math.sin (self.shape.angle)

    self.shape.x += self.dx
    self.shape.y += self.dy

    self.dx *= .99 # resistance
    self.dy *= .99

    if self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int(30 + random.random() * 10)):
        p = SmokeParticle (self.shape.x,
                           self.shape.y,
                           self.dx + random.random() - .5,
                           self.dy + random.random() - .5,
                           15 + random.random() * 10,
                           (random.random() / 2 + 2))
        e.addObj (p)
      if self.collision == OBJECT_TYPE_CANNON:
        e.score += BIG_ALIEN_POINTS

    if self.shape.x < 0 or self.shape.x > SCREEN_WIDTH or \
       self.shape.y < 0 or self.shape.y > SCREEN_HEIGHT or \
       self.collision != OBJECT_TYPE_NONE:
      return False

    return True

  def draw (self, canvas):
    self.shape.draw (canvas)

class Tanker ():
  def __init__ (self):

    '''
    ******
    *      *
    *  T    *
    *     *
    ******
    '''

    s = [(-10,-8, 15, 0, None),
         (-10, 8, 15, 0, None),
         (-10,-8,-10, 8, None)]

    self.shape = Shape (s, SCREEN_WIDTH, random.random() * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 4, 0)
    self.dx = 0
    self.dy = 0
    self.spin = 0 # (random.random() - .5) / 200
    self.thrust = .01 + random.random() / 70
    self.shape.angle = PI + (random.random() - .5) / 8
    self.collision = OBJECT_TYPE_NONE
    self.collisionRadius = 12
    self.type = OBJECT_TYPE_TANKER

  def update (self, e):
    self.shape.angle += self.spin
    self.dx += self.thrust * math.cos (self.shape.angle)
    self.dy += self.thrust * math.sin (self.shape.angle)

    self.shape.x += self.dx
    self.shape.y += self.dy

    self.dx *= .99 # resistance
    self.dy *= .99

    if self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int(50 + random.random() * 10)):
        p = SmokeParticle (self.shape.x,
                           self.shape.y,
                           self.dx + random.random() - .5,
                           self.dy + random.random() - .5,
                           15 + random.random() * 10,
                           (random.random() / 2 + 2))
        e.addObj (p)
      if self.collision == OBJECT_TYPE_CANNON:
        e.score += BIG_ALIEN_POINTS

    if self.shape.x < 0 or self.shape.x > SCREEN_WIDTH or \
       self.shape.y < 0 or self.shape.y > SCREEN_HEIGHT or \
       self.collision != OBJECT_TYPE_NONE:
      return False

    return True

  def draw (self, canvas):
    self.shape.draw (canvas)

class Asteroid ():
  def __init__ (self, radius):

    radii = 5 + int (random.random() * 5)
    r = []
    for _ in range (0, radii):
      r.append (radius + random.random() * 5 - 2)
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

    if random.random() < .5:
      top = True
    else:
      top = False

    if top:
      initY = 0
    else:
      initY = SCREEN_HEIGHT

    self.shape = Shape (s, random.random() * SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4, initY, 0)
    self.dx = random.random() / 2
    self.dy = random.random()
    if not top:
      self.dy = -self.dy
    self.spin = (random.random() - .5) / 5
    self.thrust = 0
    self.shape.angle = (random.random() - .5) / 8
    self.collision = OBJECT_TYPE_NONE
    self.collisionRadius = radius
    self.type = OBJECT_TYPE_ASTEROID

  def update (self, e):
    self.shape.angle += self.spin

    self.shape.x += self.dx
    self.shape.y += self.dy

    if self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int(30 + random.random() * 10)):
        p = SmokeParticle (self.shape.x,
                           self.shape.y,
                           self.dx + random.random() - .5,
                           self.dy + random.random() - .5,
                           20 + random.random() * 10,
                           (random.random() / 2 + 3))
        e.addObj (p)

      if self.collisionRadius > 15:
        vector = random.random() * 2 * PI

        a = Asteroid (self.collisionRadius / 2)
        a.shape.x = self.shape.x + self.collisionRadius * math.cos (vector)
        a.shape.y = self.shape.y + self.collisionRadius * math.sin (vector)

        a.dx = self.dx + math.cos (vector)
        a.dy = self.dy + math.sin (vector)
        e.addObj (a)

        a = Asteroid (self.collisionRadius / 2)
        a.shape.x = self.shape.x + self.collisionRadius * math.cos (vector + PI)
        a.shape.y = self.shape.y + self.collisionRadius * math.sin (vector + PI)
        a.dx = self.dx + math.cos (vector + PI)
        a.dy = self.dy + math.sin (vector + PI)
        e.addObj (a)
      if self.collision == OBJECT_TYPE_CANNON:
        e.score += ASTEROID_POINTS

    if self.shape.x < 0 or self.shape.x > SCREEN_WIDTH + 10 or \
       self.shape.y < 0 or self.shape.y > SCREEN_HEIGHT + 10 or \
       self.collision != OBJECT_TYPE_NONE:
      return False

    return True

  def draw (self, canvas):
    self.shape.draw (canvas)

class displayEngine ():
  def __init__(self):
    self.root = Tk()
    self.canvas = Canvas (self.root, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
    self.canvas.pack()
    self.objects = []
    self.numShips = NUM_SHIPS
    self.score = 0

  def update (self):
    # collision detection (fix wasteful checks)
    for obj1 in self.objects:
        for obj2 in self.objects:
          if obj2 is not obj1:
            if obj1.type != OBJECT_TYPE_NONE and obj2.type != OBJECT_TYPE_NONE:
              dist = math.sqrt ((obj1.shape.x - obj2.shape.x) ** 2 + (obj1.shape.y - obj2.shape.y) ** 2)
              rad = obj1.collisionRadius + obj2.collisionRadius
              if dist < rad:
                obj1.collision = obj2.type
                obj2.collision = obj1.type

    # update objects
    for obj in self.objects:
      if obj.update (self) == False:
        self.objects.remove (obj)

  def addObj (self, obj):
    self.objects.append (obj)

  def draw (self, ship):
    self.canvas.delete (ALL)
    for obj in self.objects:
      obj.draw (self.canvas)

    # game status
    # display the remaining ships
    for s in range (0, self.numShips):
       self.canvas.create_line (10 + 20 * s, 20, 15 + 20 * s,  5)
       self.canvas.create_line (15 + 20 * s,  5, 20 + 20 * s, 20)

    score = "%08s" % (self.score)
    self.canvas.create_text (100, 10, text = score)
    self.canvas.create_rectangle (200, 5, 200 + 200, 7)
    self.canvas.create_rectangle (200, 10, 200 + 200 * ship.fuel / 100, 15)

    self.root.update()

MAX_SPIN = .3
SPIN_DELTA = .025
def leftHandler (event):
  if s.spin > 0:
    s.spin = 0
  elif s.spin > -MAX_SPIN:
    s.spin -= SPIN_DELTA

def rightHandler (event):
  if s.spin < 0:
    s.spin = 0
  elif s.spin < MAX_SPIN:
    s.spin += SPIN_DELTA

def upHandler (event):
  if s.thrust < .2:
    s.thrust += .025

def downHandler (event):
  s.thrust = 0
  s.dx *= .8
  s.dy *= .8

def keyHandler (event):
  global respawn

  if event.char == " ":
    if s.collision > 0:
      respawn = True
    else:
      s.cannon = s.numRounds
      if e.score:
        e.score -= 1

e = displayEngine()
s = Ship()
e.addObj (s)

e.root.bind ("<Left>",  leftHandler)
e.root.bind ("<Right>", rightHandler)
e.root.bind ("<Up>",    upHandler)
e.root.bind ("<Down>",  downHandler)
e.root.bind ("<Key>",   keyHandler)

t = Tanker()  # test
e.addObj(t)

nextAlien = 200
nextAsteroid = 400

while True:
  e.update ()
  e.draw (s)
  time.sleep (.02)

  nextAsteroid -= 1
  if nextAsteroid < 0:
    a = Asteroid (20 + random.random() * 10)
    e.addObj (a)
    nextAsteroid = 200 + random.random() * 100

  nextAlien -= 1
  if nextAlien < 0:
    nextAlien = 100 + random.random() * 100
    if random.random() < .25:
      a = SmallAlien()
    else:
      a = BigAlien()
    e.addObj (a)
  if respawn:
    respawn = False
    s = Ship ()
    e.addObj (s)

e.root.mainloop()
