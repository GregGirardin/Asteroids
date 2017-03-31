from Constants import *
from Vector import *
from Shape import *
from Utils import *
from Particles import *
from Tkinter import *

class Ship (WorldObject):
  def __init__ (self):
    s = [(-5, 5, 10, 0, None),
         (-5,-5, 10, 0, None),
         (-5,-5, -5, 5, None)]
    self.shape = Shape (s)
    self.fireCannon = False
    self.fireTorpedo = False
    self.rounds = 50.0
    self.fuel = 50.0
    self.torpedos = 50.0
    self.torpedoDelay = 0
    WorldObject.__init__ (self,
                          OBJECT_TYPE_SHIP,
                          Point (SCREEN_WIDTH * .75, SCREEN_HEIGHT / 2),
                          PI,
                          None,
                          7,
                          SHIP_MASS)

  def update (self, e):
    WorldObject.update (self, e)

    if self.accel > 0:
      if self.accel > THRUST_MAX:
        self.accel = THRUST_MAX
      if self.fuel < 0:
        self.fuel = 0
        if self.accel > 0:
          self.accel = THRUST_LOW
      self.fuel -= self.accel * 2

    # bounce off walls
    if self.p.x < 0 and self.v.dx() < 0 or self.p.x > SCREEN_WIDTH and self.v.dx() > 0:
      self.v.flipx()
      self.v.magnitude *= .9
    if self.p.y < 0 and self.v.dy() < 0 or self.p.y > SCREEN_HEIGHT and self.v.dy() > 0:
      self.v.flipy()
      self.v.magnitude *= .9

    if self.accel > 0:
      p = SmokeParticle (Point (self.p.x, self.p.y).move (Vector (3, self.a + PI)),
                         Vector (3, self.a + PI + random.uniform (-.3, .3)),
                         random.randrange (5, 12),
                         self.accel * random.uniform (15, 30))
      e.addObj (p)

    if self.fireCannon is True and self.rounds > 0:
      p = CanonParticle (Point (self.p.x + 10 * math.cos (self.a),
                                self.p.y - 10 * math.sin (self.a)),
                         Vector (7, self.a).add (self.v), 120)
      e.addObj (p)
      self.fireCannon = False
      self.rounds -= .5
      if e.score > CANNON_COST:
        e.score -= CANNON_COST

    if self.torpedoDelay > 0:
      self.torpedoDelay -= 1
      self.fireTorpedo = False

    if self.fireTorpedo is True:
      if self.torpedos > 0:
        p = Torpedo (Point (self.p.x + 20 * math.cos (self.a),
                            self.p.y - 20 * math.sin (self.a)),
                            Vector (7, self.a).add (self.v),
                            150)
        e.addObj (p)
        self.torpedos -= 10
        self.torpedoDelay = TORPEDO_DELAY
        if e.score > TORPEDO_COST:
          e.score -= TORPEDO_COST
      self.fireTorpedo = False

    while self.colList:
      c = self.colList.pop()

      if c.o.type == OBJECT_TYPE_TANKER:
        # transfer resources
        t = c.o
        if t.fuel > 0 and self.fuel < 100.0:
          self.fuel += 1
          t.fuel -= 1
        else:
          t.transferComplete |= TX_RESOURCE_FUEL

        if t.rounds > 0 and self.rounds < 100.0:
          self.rounds += 1
          t.rounds -= 1
        else:
          t.transferComplete |= TX_RESOURCE_ROUNDS

        if t.torpedos > 0 and self.torpedos < 100.0:
          self.torpedos += 1
          t.torpedos -= 1
        else:
          t.transferComplete |= TX_RESOURCE_TORPEDOS
      elif c.i.magnitude < SMALL_IMPULSE and c.o.weapon is False:
        self.v.add (c.i, mod = True)
        if self.v.magnitude > SPEED_HI:
          self.v.magnitude = SPEED_HI
        # self.p.move (Vector (c.d / 2, c.i.direction))
      else:
        e.numShips -= 1
        if e.numShips < 0:
          e.events.newEvent ("You have failed fuckhead.", EVENT_DISPLAY_COUNT * 2, e.gameOver)

        for _ in range (1, random.randrange (30,40)):
          p = SmokeParticle (Point (self.p.x, self.p.y),
                             Vector (random.uniform (0, 2), TAU * random.random ()).add (self.v),
                             random.uniform (20, 50),
                             random.uniform (3, 3.5))
          e.addObj (p)
        return False
    return True

  def draw (self, canvas, p, a):
    self.shape.draw (canvas, p, a)
    canvas.create_rectangle (100,  5, 100 + 200, 7)
    fill = "red" if self.fuel < 20.0 else "black"
    canvas.create_rectangle (100, 10, 100 + 2 * self.fuel, 12, fill=fill)
    fill = "red" if self.rounds < 20.0 else "black"
    canvas.create_rectangle (100, 20, 100 + 2 * self.rounds, 22, fill=fill)
    fill = "red" if self.torpedos < 20.0 else "black"
    canvas.create_rectangle (100, 30, 100 + 2 * self.torpedos, 32, fill=fill)