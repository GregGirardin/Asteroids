'''
A base class to handle piloting ships / AI stuff.

hList is a list of heuristics
Initially we choose the first element.


Identifier # a string to ID
Next ID
  Type (Goto, Delay, Attack)
    Goto
      Point
      ApproachType (Slow, fast)
        Slow # Try to stop at point
        Fast # Just blow past point.

    Delay
      duration
      Next

    Attack
      duration
'''
import time, math, random
from Constants import *
from Shape import *
from Ship import *
from Vector import *

class HeuristicGo ():
  def __init__(self, velocity, duration):
    self.hVelocity = velocity
    self.hDuration = duration

  def update (self, s, e):
    if self.hDuration > 0:
      self.hDuration -= 1
      if s.v.magnitude < self.hVelocity:
        s.accel = THRUST_MED
      else:
        s.accel = 0
      return False
    else:
      return True

class HeuristicFace():
  def __init__(self, angle):
    self.hAngle = angle

  def update (self, s, e):
    dirTo = angleTo (s.a, self.hAngle)
    if math.fabs (dirTo) > .05:
      s.spin = dirTo / 20
      return False
    else:
      s.spin = 0
      return True

class HeuristicStop():
  def update (self, s, e):
    if s.v.magnitude > SPEED_SLOW / 20:
      # turn around
      targetDir = angleNorm (s.v.direction + PI)
      dirTo = angleTo (s.a, targetDir)
      if math.fabs (dirTo) > .05:
        s.accel = 0
        s.spin = dirTo / 20
      else:
        s.accel = THRUST_HI
        s.spin = 0
      return False

    s.accel = 0
    s.spin = 0
    return True

class HeuristicGoto ():
  def __init__ (self, target, distance):
    self.target = target
    self.distance = distance # close do we need to get for success
    self.targetReached = False

  def update (self, s, e):
    # determine ideal vector based on distance
    distToTarget = s.p.distanceTo (self.target)

    s.accel = 0
    s.spin = 0

    if ((distToTarget < OBJECT_DIST_FAR) and
        ((self.distance == OBJECT_DIST_FAR) or
         ((distToTarget > OBJECT_DIST_MED and self.distance == OBJECT_DIST_MED) or
         (distToTarget < OBJECT_DIST_NEAR)))):
      return True

    dirToTarget = s.p.directionTo (self.target)
    targetVector = Vector (SPEED_HI * 1.5, dirToTarget) # hack. Long vector and drag smooth out ship.
    correctionVec = vectorDiff (s.v, targetVector) # vector to make our velocity approach targetVector

    da = angleTo (s.a, correctionVec.direction)

    s.spin = da / 20
    dp = s.v.dot (correctionVec.direction)
    if dp < SPEED_HI:
      s.accel = THRUST_HI
    elif dp < SPEED_MED:
      s.accel = THRUST_LOW

    # Cheating. Drag allows us to stay behind target vector. Tricky to fix and this works.
    # otherwise you have to deal with turning around to slow down if you're too fast.
    s.v.magnitude *= .99

    if debugVectors:
      s.tv = targetVector
      s.cv = desiredVec
      s.target = target

    return False

def HeuristicGotoRandom():
  return HeuristicGoto (Point (SCREEN_WIDTH  * random.random (), SCREEN_HEIGHT * random.random ()), OBJECT_DIST_MED)

class HeuristicWait ():
  def __init__ (self, duration):
    self.hDuration = duration

  def update (self, s, e):
    s.accel = 0
    s.spin = 0

    self.hDuration -= 1
    if self.hDuration < 0:
      return True
    return False

class HeuristicAttack ():
  def __init__ (self, duration = 50):
    self.duration = duration
    self.durationCounter = duration
    self.attackState = ATTACK_INIT
    self.aangleOffset = 0
    self.ttNextAttack = 1

  def update (self, s, e):
    self.durationCounter -= 1
    if self.durationCounter <= 0:
      self.durationCounter = self.duration
      return True

    if self.attackState == ATTACK_INIT:
      if self.ttNextAttack == 0:
        self.attackState = ATTACK_ALIGN
        self.aangleOffset = random.uniform (-.2, .2) # shoot a bit randomly
      else:
        self.ttNextAttack -= 1

    if self.attackState == ATTACK_ALIGN:
      sh = None
      for obj in e.objects:
        if obj.type == OBJECT_TYPE_SHIP:
          sh = obj
          break
      if not sh:
        return True

      goalDir = dir (sh.p.x - s.p.x, sh.p.y - s.p.y) + self.aangleOffset
      aToGoal = angleTo (s.a, goalDir)

      if math.fabs (aToGoal) < .1:
        s.cannon = 1 # cannon handled in update
        self.attackState = ATTACK_INIT
        self.ttNextAttack = random.randrange (20, 70)
      else:
        s.spin = aToGoal / 10

    return False

class Heuristic ():
  def __init__ (self, id, next, heuristic):
    self.id = id
    self.next = next
    self.heuristic = heuristic

# Auto piloted things inherit from this class. They are also "WorldObject"s
class Pilot ():
  def __init__ (self, hList):
    self.hList = hList

    if self.hList:
      self.currentH = hList [0]
    else:
      self.currentH = None

    if debugVectors:
      self.tv = Vector (0,0)
      self.cv = Vector (0,0)
      self.target = Point (0,0)

  def setHlist (self, hList):
    self.hList = hList
    self.currentH = hList [0]

  def pilot (self, e):
    # Adjust, thrust, direction, and cannon based on heuristics.
    if self.hList == None or self.currentH == None:
      return

    s = self.currentH.heuristic.update (self, e)

    if s == True:
      for h in self.hList:
        if h.id == self.currentH.next:
          self.currentH = h
          break