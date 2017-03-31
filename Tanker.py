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
    p = Point (SCREEN_WIDTH + SCREEN_BUFFER - 1, random.uniform (SCREEN_HEIGHT * .1, SCREEN_HEIGHT * .9))
    self.shape = Shape (s)

    # resources available if ship contacts
    self.fuel = random.uniform (30.0, 70.0)
    self.rounds = random.uniform (30.0, 70.0)
    self.torpedos = random.uniform (20.0, 50.0)

    self.refuelComplete = False
    self.transferComplete = 0
    self.tPoint = None # Tractor point

    hList = [
      Heuristic ("f",  "g",  HeuristicFace (PI)),
      Heuristic ("g",  "s",  HeuristicGo (SPEED_MED, 100)),
      Heuristic ("s",  "w",  HeuristicStop ()),
      Heuristic ("w",  "f2", HeuristicWait (500)),
      Heuristic ("f2", "d",  HeuristicFace (0)),
      Heuristic ("d",  None, HeuristicGo (SPEED_HI, 1000))
      ]

    Pilot.__init__ (self, hList)
    WorldObject.__init__ (self, OBJECT_TYPE_TANKER, p, 0, None, 12, mass = TANKER_MASS)

  def update (self, e):
    Pilot.pilot (self, e)
    WorldObject.update (self, e)

    if self.offScreen():
      return False

    self.tPoint = None
    if self.refuelComplete == False:
      # check for tractor.
      for obj in e.objects:
        if obj.type == OBJECT_TYPE_SHIP:
          d = self.p.distanceTo (obj.p)
          if d < OBJECT_DIST_NEAR:
            at = angleTo (obj.a, self.a)
            obj.a += at / 10 # line it up

            # ideal velocity vector is matching the tanker + towards the tanker.
            vIdeal = self.v.add (Vector (d / 10, obj.p.directionTo (self.p)), mod=False)
            obj.v.adjust (vIdeal, .05)
            self.tPoint = obj.p
          break

    if self.accel > 0:
      p = SmokeParticle (Point (self.p.x, self.p.y).move (Vector (3, self.a + PI)),
                         Vector (2, self.a + PI + random.uniform (-.25, .25)),
                         random.uniform (5, 10),
                         self.accel * random.uniform (15, 30))
      e.addObj (p)

    if (self.transferComplete & TX_RESOURCE_ALL == TX_RESOURCE_ALL) and self.refuelComplete is False:
      self.refuelComplete = True
      e.events.newEvent ("Refuel Complete", EVENT_DISPLAY_COUNT / 2, None)
      hList = [ Heuristic ("Depart", None, HeuristicGoto (Point (SCREEN_WIDTH * 1.1, SCREEN_HEIGHT * random.random()), OBJECT_DIST_NEAR)) ]
      self.setHlist (hList)

    while self.colList:
      c = self.colList.pop(0)
      t = c.o.type
      if t != OBJECT_TYPE_SHIP:
        if c.i.magnitude < SMALL_IMPULSE and c.o.weapon is False:
          self.v.add (c.i, mod = True)
          if self.v.magnitude > SPEED_HI:
            self.v.magnitude = SPEED_HI
          # self.p.move (Vector (c.d / 2, c.i.direction))
        elif c.o.type != OBJECT_TYPE_NONE:
          for _ in range (1, int (random.uniform (20, 30))):
            p = SmokeParticle (Point (self.p.x, self.p.y),
                               Vector (random.random(), random.uniform (0, TAU)).add (self.v),
                               random.uniform (30, 50),
                               random.uniform (3, 3.5))
            e.addObj (p)

          if t == OBJECT_TYPE_CANNON or t == OBJECT_TYPE_TORPEDO or t == OBJECT_TYPE_T_CANNON:
            e.events.newEvent ("You destroyed the SS Vinoski! LOL", EVENT_DISPLAY_COUNT, None)
          else:
            e.events.newEvent ("Tanker destroyed", EVENT_DISPLAY_COUNT / 2, None)

          if e.score > TANKER_DESTROYED_COST:
            e.score -= TANKER_DESTROYED_COST
          else:
            e.score = 0
          return False

    return True

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)
    if self.tPoint:
      canvas.create_line (p.x, p.y,
                          self.tPoint.x + random.uniform (-2, 2),
                          self.tPoint.y + random.uniform (-2, 2), fill = "green")

def newTanker ():
  return Tanker()