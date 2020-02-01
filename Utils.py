from Constants import *
from Shape import *
from Vector import *

class WorldObject():
  # Attributes every object has.
  def __init__( self, type, p, a = 0.0, v= None, colRadius = 0, mass = 1.0, weapon = False ):
    if not v:
      v = Vector( 0, 0 )
    self.v = v
    self.spin = 0.0
    self.p = p # position
    self.a = a # angle
    self.type = type
    self.accel = 0.0
    self.weapon = weapon # Explode even on slow contact
    self.colRadius = colRadius
    self.colList = [] # a list of CollisionObject
    self.mass = mass

  def offScreen( self ):
    if self.p.x < -SCREEN_BUFFER or self.p.x > SCREEN_WIDTH + SCREEN_BUFFER or \
       self.p.y < -SCREEN_BUFFER or self.p.y > SCREEN_HEIGHT + SCREEN_BUFFER:
      return True
    else:
      return False

  def update( self, e ):
    self.a += self.spin
    if self.a < 0:
      self.a += TAU
    elif self.a > TAU:
      self.a -= TAU
    self.p.move( self.v )
    self.v.add( Vector( self.accel, self.a ) )

class CollisionObject():
  def __init__( self, o, i, d ):
    self.o = o # the object
    self.i = i # impulse = speed * their mass / my mass, dir
    self.d = d # distance between objects.

class Event ():
  def __init__( self, msg, dur, action ):
    self.msg = msg
    self.dur = dur
    self.action = action # callback

class gameEvents():
  def __init__( self ):
    self.eventList = []

  def newEvent( self, msg, dur, action ):
    ev = Event( msg, dur, action )
    self.eventList.append( ev )

  def update( self ):
    if len( self.eventList ) > 0:
      e = self.eventList[ 0 ]
      e.dur -= 1
      if e.dur < 0:
        if e.action:
          e.action()
        del self.eventList[ 0 ]
    return True # Event object is always here

  def draw( self, e ):
    if len( self.eventList ) > 0:
      ev = self.eventList[ 0 ]
      if ev.msg:
        e.canvas.create_text( SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, text = ev.msg )

class spawnAble():
  def __init__( self, min, max, num, ict, newFunc ):
    self.min = min
    self.max = max
    self.num = num
    self.newFunc = newFunc
    self.spawnCountdown = ict

  def update( self, e ):
    if self.num > 0 or self.num == -1:
      self.spawnCountdown -= 1
      if self.spawnCountdown <= 0:
        self.spawnCountdown = random.randrange( self.min, self.max )
        s = self.newFunc()
        e.addObj( s )
        if self.num > 0:
          self.num -= 1

class spawnList():
  def __init__( self, l ):
    self.spawnAbles = []
    for s in l:
      self.spawnAbles.append( spawnAble( *s ) )

  def update( self, e ):
    if self.spawnAbles:
      for s in self.spawnAbles:
        s.update( e )
    done = True
    for s in self.spawnAbles:
      if s.num > 0:
        done = False
        break
    return done

# if you're facing dir and want to go goalDir, return the delta. -PI to PI
def angleTo( dir, goalDir ):
  dif = goalDir - dir
  if dif > PI:
    dif -= TAU
  elif dif < -PI:
    dif += TAU
  return dif

def angleNorm( dir ):
  if dir > PI:
    dir -= TAU
  elif dir < -PI:
    dir += TAU
  return dir