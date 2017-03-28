from Constants import *
from Shape import *
from Vector import *
from Utils import *
from Particles import *
from Pilot import *
import Tkinter as tk # debug

class SmallAlien (WorldObject, Pilot):
  def __init__ (self):

    s = [(-2, 3, 10, 0, None),
         (-2,-3, 10, 0, None),
         (-2,-3, -2, 3, None)]

    self.shape = Shape (s)
    self.cannon = 0

    hLists = [
        [ # randomly flys among a few points, stopping to shoot.
          Heuristic ("1", HEUR_GOTO, "1a", HeuristicGotoRandom()),
          Heuristic ("1a", HEUR_ATTACK, "2", HeuristicAttack (100)),
          Heuristic ("2", HEUR_GOTO, "2a", HeuristicGotoRandom()),
          Heuristic ("2a", HEUR_ATTACK, "3", HeuristicAttack (random.uniform (100, 400))),
          Heuristic ("3", HEUR_GOTO, "3a", HeuristicGotoRandom()),
          Heuristic ("3a", HEUR_ATTACK, "1", HeuristicAttack (100)),
        ],
        [ # this one flys around clockwise forever and shoots at you
          Heuristic ("1", HEUR_GOTO, "1a",
                     HeuristicGoto (Point (SCREEN_WIDTH * .25, SCREEN_HEIGHT * .25),
                                    OBJECT_DIST_MED)),
          Heuristic ("1a", HEUR_ATTACK, "2", HeuristicAttack (100)),
          Heuristic ("2", HEUR_GOTO, "2a",
                     HeuristicGoto (Point (SCREEN_WIDTH * .75, SCREEN_HEIGHT * .25),
                                    OBJECT_DIST_MED)),
          Heuristic ("2a", HEUR_ATTACK, "3", HeuristicAttack (100)),
          Heuristic ("3", HEUR_GOTO, "3a",
                     HeuristicGoto (Point (SCREEN_WIDTH * .75, SCREEN_HEIGHT * .75),
                                    OBJECT_DIST_MED)),
          Heuristic ("3a", HEUR_ATTACK, "4", HeuristicAttack (100)),
          Heuristic ("4", HEUR_GOTO, "4a",
                     HeuristicGoto (Point (SCREEN_WIDTH * .25, SCREEN_HEIGHT * .75),
                                    OBJECT_DIST_MED)),
          Heuristic ("4a", HEUR_ATTACK, "1", HeuristicAttack (100)),
        ],
        [ # This one flys across this screen but shoots at you at a couple points.
          Heuristic ("1", HEUR_GOTO, "2",
                     HeuristicGoto (Point (SCREEN_WIDTH * .25, random.uniform (SCREEN_HEIGHT * .25, SCREEN_HEIGHT * .75)),
                                    OBJECT_DIST_MED)),
          Heuristic ("2", HEUR_GOTO, "2a",
                     HeuristicGoto (Point (SCREEN_WIDTH * .5, random.uniform (SCREEN_HEIGHT * .25, SCREEN_HEIGHT * .75)),
                                    OBJECT_DIST_MED)),
          Heuristic ("2a", HEUR_ATTACK, "3", HeuristicAttack (300)),
          Heuristic ("3", HEUR_GOTO, "3a",
                     HeuristicGoto (Point (SCREEN_WIDTH * .75, random.uniform (SCREEN_HEIGHT * .25, SCREEN_HEIGHT * .75)),
                                    OBJECT_DIST_MED)),
          Heuristic ("3a", HEUR_ATTACK, "4", HeuristicAttack (300)),
          Heuristic ("4", HEUR_GOTO, None,
                     HeuristicGoto (Point (SCREEN_WIDTH * 1.5, random.uniform (0, SCREEN_HEIGHT)), OBJECT_DIST_FAR))
          ]
    ]
    p = Point (-SCREEN_BUFFER + 1, SCREEN_HEIGHT * random.random())
    Pilot.__init__ (self, hLists [random.randint(0, 2)])
    WorldObject.__init__ (self, OBJECT_TYPE_ALIEN, p, (random.random() - .5) / 4, None, 5)

  def update (self, e):
    Pilot.pilot (self, e)
    WorldObject.update (self, e)

    if self.cannon > 0:
      self.cannon -= 1
      p = CanonParticle (Point (self.p.x + 10 * math.cos (self.a),
                                self.p.y - 10 * math.sin (self.a)),
                         Vector (7, self.a), 120, type = OBJECT_TYPE_AL_CANNON)
      e.addObj (p)

    if self.collisionObj:
      for _ in  range (1, int (10 + random.random() * 10)):
        p = SmokeParticle (Point (self.p.x, self.p.y),
                           Vector (random.random(), TAU * random.random ()).add (self.v),
                           20 + random.random() * 20,
                           (random.random() / 2 + 2))
        e.addObj (p)
      t = self.collisionObj.type
      if t == OBJECT_TYPE_CANNON or t == OBJECT_TYPE_TORPEDO or t == OBJECT_TYPE_T_CANNON:
        e.score += SMALL_ALIEN_POINTS

    if self.accel > 0:
      p = SmokeParticle (Point (self.p.x, self.p.y).move (Vector (3, self.a + PI)),
                         Vector (2, self.a + PI + random.uniform (-.25, .25)),
                         random.uniform (5, 10),
                         self.accel * random.uniform (15, 30))
      e.addObj (p)

    if self.offScreen() or self.collisionObj:
      return False

    return True

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)

    if debugVectors:
      canvas.create_line (p.x, p.y, p.x + self.v.dx()  * 20, p.y + self.v.dy()  * 20, arrow = tk.LAST, fill = "green")
      canvas.create_line (p.x, p.y, p.x + self.tv.dx() * 20, p.y + self.tv.dy() * 20, arrow = tk.LAST)
      canvas.create_line (p.x, p.y, p.x + self.cv.dx() * 20, p.y + self.cv.dy() * 20, arrow = tk.LAST, fill = "red")
      canvas.create_oval (self.target.x - 2, self.target.y - 2, self.target.x + 2, self.target.y + 2)

class BigAlien (WorldObject, Pilot):
  def __init__ (self):

    s = [(-10, 8, 15, 0, None),
         (-10,-8, 15, 0, None),
         (-10,-8,-10, 8, None)]

    self.shape = Shape (s)

    hLists = [
      [
        Heuristic ("i", HEUR_GOTO, "x",
                   HeuristicGoto (Point (SCREEN_WIDTH * random.uniform (.3, .7),
                                         random.uniform (SCREEN_HEIGHT * .25, SCREEN_HEIGHT * .75)),
                                  OBJECT_DIST_NEAR)),
        Heuristic ("x", HEUR_GOTO, None,
                   HeuristicGoto (Point (SCREEN_WIDTH * 1.1, random.uniform (-200, SCREEN_HEIGHT + 200)),
                                  OBJECT_DIST_MED))
      ],
      [
        Heuristic ("i", HEUR_GOTO, "b",
                   HeuristicGoto (Point (SCREEN_WIDTH / 4, random.uniform (SCREEN_HEIGHT * .25, SCREEN_HEIGHT * .75)),
                                  OBJECT_DIST_NEAR)),
        Heuristic ("b", HEUR_GOTO, "c",
                   HeuristicGoto (Point (SCREEN_WIDTH / 2, random.uniform (SCREEN_HEIGHT * .1, SCREEN_HEIGHT * .9)),
                                  OBJECT_DIST_MED)),
        Heuristic ("c", HEUR_GOTO, None,
                   HeuristicGoto (Point (SCREEN_WIDTH * 1.5, random.uniform (SCREEN_HEIGHT * .25, SCREEN_HEIGHT * .75)),
                                  OBJECT_DIST_MED))
      ],
      [
        Heuristic ("Face", HEUR_FACE, "Go", HeuristicFace (random.uniform (-.4, .4))), # face right ish
        Heuristic ("Go", HEUR_GO, "Depart", HeuristicGo (SPEED_HI, random.uniform (200, 700))),
       # Heuristic ("Stop", HEUR_STOP, "Wait", HeuristicStop ()),
       # Heuristic ("Wait", HEUR_WAIT, "Depart", HeuristicWait (100)),
        Heuristic ("Depart", HEUR_GOTO, None,
                   HeuristicGoto (Point (SCREEN_WIDTH * 1.2, SCREEN_HEIGHT * random.random()), OBJECT_DIST_NEAR))
      ]]

    p = Point (-SCREEN_BUFFER + 1, SCREEN_HEIGHT * random.random())

    Pilot.__init__ (self, hLists [random.randint (0, 2)])
    WorldObject.__init__ (self, OBJECT_TYPE_ALIEN, p, (random.random() - .5) / 4, None, 12)

  def update (self, e):
    Pilot.pilot (self, e)
    WorldObject.update (self, e)

    if self.collisionObj:
      for _ in  range (1, int (30 + random.random() * 10)):
        p = SmokeParticle (Point (self.p.x, self.p.y),
                           Vector (random.random(), TAU * random.random ()).add (self.v),
                           30 + random.random() * 20,
                           (random.random() / 2 + 2))
        e.addObj (p)
      t = self.collisionObj.type
      if t == OBJECT_TYPE_CANNON or t == OBJECT_TYPE_TORPEDO or t == OBJECT_TYPE_T_CANNON:
        e.score += BIG_ALIEN_POINTS

    if self.accel > 0:
      p = SmokeParticle (Point (self.p.x, self.p.y).move (Vector (7, self.a + PI)),
                         Vector (2, self.a + PI + random.uniform (-.25, .25)),
                         random.uniform (5, 10),
                         self.accel * random.uniform (15, 30))
      e.addObj (p)

    if self.offScreen() or self.collisionObj:
      return False

    return True

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)

    if debugVectors:
      canvas.create_line (p.x, p.y, p.x + self.v.dx()  * 20, p.y + self.v.dy()  * 20, arrow = tk.LAST, fill = "green")
      canvas.create_line (p.x, p.y, p.x + self.tv.dx() * 20, p.y + self.tv.dy() * 20, arrow = tk.LAST)
      canvas.create_line (p.x, p.y, p.x + self.cv.dx() * 20, p.y + self.cv.dy() * 20, arrow = tk.LAST, fill = "red")
      canvas.create_oval (self.target.x - 2, self.target.y - 2, self.target.x + 2, self.target.y + 2)