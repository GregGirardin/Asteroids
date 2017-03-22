from Constants import *
from Shape import *
from Vector import *
from Utils import *
from Particles import *
from Pilot import *

class SmallAlien (WorldObject, Pilot):
  def __init__ (self):

    s = [(-2, 3, 10, 0, None),
         (-2,-3, 10, 0, None),
         (-2,-3, -2, 3, None)]

    self.shape = Shape (s)
    self.collision = OBJECT_TYPE_NONE

    hList = [
      Heuristic ("Init", HEUR_GOTO, "Midway",
                 HeuristicGoto (Point (SCREEN_WIDTH / 2, SCREEN_HEIGHT * random.random()), OBJECT_DIST_FAR, 0)),
      Heuristic ("Midway", HEUR_GOTO, None,
                 HeuristicGoto (Point (SCREEN_WIDTH, SCREEN_HEIGHT * random.random()), OBJECT_DIST_FAR, 0))
      ]

    p = Point (0, SCREEN_HEIGHT * random.random())
    Pilot.__init__ (self, hList)
    WorldObject.__init__ (self, OBJECT_TYPE_ALIEN, p, (random.random() - .5) / 4, None, 5)

  def update (self, e):
    Pilot.pilot (self, e)
    WorldObject.update (self, e)

    if self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int (10 + random.random() * 10)):
        p = SmokeParticle (Point (self.p.x, self.p.y),
                           Vector (random.random(), TAU * random.random ()).impulse (self.v),
                           20 + random.random() * 20,
                           (random.random() / 2 + 2))
        e.addObj (p)
      if self.collision == OBJECT_TYPE_CANNON:
        e.score += SMALL_ALIEN_POINTS

    if self.offScreen() or self.collision != OBJECT_TYPE_NONE:
      return False

    return True

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)

class BigAlien (WorldObject, Pilot):
  def __init__ (self):

    s = [(-10, 8, 15, 0, None),
         (-10,-8, 15, 0, None),
         (-10,-8,-10, 8, None)]

    self.shape = Shape (s)
    self.collision = OBJECT_TYPE_NONE

    hList = [
      Heuristic ("Init", HEUR_GOTO, "Midway",
                 HeuristicGoto (Point (SCREEN_WIDTH / 2, SCREEN_HEIGHT * random.random()), OBJECT_DIST_FAR, 0)),
      Heuristic ("Midway", HEUR_GOTO, None,
                 HeuristicGoto (Point (SCREEN_WIDTH * 2, SCREEN_HEIGHT * random.random()), OBJECT_DIST_FAR, 0))
      ]
    p = Point (0, SCREEN_HEIGHT * random.random())

    Pilot.__init__ (self, hList)
    WorldObject.__init__ (self, OBJECT_TYPE_ALIEN, p, (random.random() - .5) / 4, None, 12)

  def update (self, e):
    Pilot.pilot (self, e)
    WorldObject.update (self, e)

    if self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int (30 + random.random() * 10)):
        p = SmokeParticle (Point (self.p.x, self.p.y),
                           Vector (random.random(), TAU * random.random ()).impulse (self.v),
                           30 + random.random() * 20,
                           (random.random() / 2 + 2))
        e.addObj (p)
      if self.collision == OBJECT_TYPE_CANNON:
        e.score += BIG_ALIEN_POINTS

    if self.offScreen() or self.collision != OBJECT_TYPE_NONE:
      return False

    return True

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)