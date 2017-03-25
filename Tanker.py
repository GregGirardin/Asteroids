from Constants import *
from Shape import *
from Vector import *
from Pilot import *
from Particles import *
from Utils import *
import Tkinter as tk # debug

class Tanker (WorldObject, Pilot):
  def __init__ (self):
    '''
    ******
     *      *
      *  T    *
     *     *
    ******
    '''

    s = [(-10,-10, 0,-10, None),
         (-10, 10, 0, 10, None),
         (  0,-10, 10, 0, None),
         (  0, 10, 10, 0, None),
         (-10,-10 ,-5, 0, None),
         (-10, 10 ,-5, 0, None)]

    # start from the right side, going left.
    p = Point (SCREEN_WIDTH + SCREEN_BUFFER / 2, random.uniform(SCREEN_HEIGHT * .25, SCREEN_HEIGHT * .75))
    self.shape = Shape (s)
    self.collision = OBJECT_TYPE_NONE
    self.rendesvousComplete = False

    self.waitTime = 0

    hList = [
      Heuristic ("Init", HEUR_GOTO, "Wait",
                 HeuristicGoto (Point (SCREEN_WIDTH * random.uniform (.5, .8), SCREEN_HEIGHT * random.uniform (.2, .8)),
                                OBJECT_DIST_NEAR, 200, APPROACH_TYPE_SLOW)),
      Heuristic ("Wait", HEUR_WAIT, "Depart", HeuristicWait (500)),
      Heuristic ("Depart", HEUR_GOTO, None,
                 HeuristicGoto (Point (SCREEN_WIDTH * 2, SCREEN_HEIGHT / 2), OBJECT_DIST_NEAR, 0, APPROACH_TYPE_FAST))
      ]

    Pilot.__init__ (self, hList)
    WorldObject.__init__ (self, OBJECT_TYPE_TANKER, p, 0, None, 12)

  def update (self, e):
    Pilot.pilot (self, e)
    WorldObject.update (self, e)

    if self.accel > 0:
      p = SmokeParticle (Point (self.p.x, self.p.y),
                         Vector (2, self.a + PI + random.uniform (-.25, .25)),
                         random.uniform (5, 10),
                         self.accel * random.uniform (15, 30))
      e.addObj (p)

    if self.collision == OBJECT_TYPE_SHIP:
       self.collision = OBJECT_TYPE_NONE
    elif self.collision != OBJECT_TYPE_NONE:
      for _ in  range (1, int (random.uniform (20, 40))):
        p = SmokeParticle (Point (self.p.x, self.p.y),
                           Vector (random.random(), random.uniform (0, TAU)).impulse (self.v),
                           random.uniform (30, 50),
                           random.uniform (3, 3.5))
        e.addObj (p)

    if self.offScreen():
      e.events.newEvent ("Tanker safe bonus", EVENT_DISPLAY_COUNT / 2, None)
      e.score += TANKER_SAFE_POINTS
      return False
    if self.collision != OBJECT_TYPE_NONE:
      if self.collision == OBJECT_TYPE_CANNON:
        e.events.newEvent ("You destroyed the SS Vinoski! LOL", EVENT_DISPLAY_COUNT, None)
      return False

    return True

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)

    if debugVectors:
      canvas.create_line (p.x, p.y, p.x + self.v.dx()  * 20, p.y - self.v.dy()  * 20, arrow=tk.LAST, fill="green")
      canvas.create_line (p.x, p.y, p.x + self.tv.dx() * 20, p.y - self.tv.dy() * 20, arrow=tk.LAST)
      canvas.create_line (p.x, p.y, p.x + self.cv.dx() * 20, p.y - self.cv.dy() * 20, arrow=tk.LAST, fill="red")
      canvas.create_oval (self.target.x - 2, self.target.y - 2, self.target.x + 2, self.target.y + 2)
