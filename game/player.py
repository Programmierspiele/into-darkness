import math

PRIMARY_RELOAD = 1 * 60
SECONDARY_RELOAD = 3 * 60

RESPAWN_TICKS = 10 * 60

AIMSPEED_PER_TICK = 0.2
TURNSPEED_PER_TICK = 0.1
MOVESPEED_PER_TICK = 1.0

class Player(object):
    def __init__(self, raycaster):
        self.raycaster = raycaster
        # TODO clever spawn positions
        self.pose = {x: 0, y: 0, theta: 0, aim: 0}
        self.movespeed = 0
        self.turnspeed = 0
        self.aimspeed = 0
        self.shootstate = 0
        self.health = 100
        self.respawn = 0
        
        self.primary_reload = 0
        self.secondary_reload = 0
        
    def damage(self, damage, dmg_heading):
        dh = math.abs(self.pose.theta - dmg_heading) / math.pi
        modifier = (1-dh) * 0.5 + 0.5
        self.health -= damage * modifier
        
    def get_pose(self):
        return {x: self.pose.x, y: self.pose.y, theta: self.pose.theta}
        
    def update(self, players, projectiles):
        if self.respawn > 0:
            self.respawn -= 1
            if self.respawn == 0:
                # TODO Clever spawn positions
                self.pose = {x: 0, y: 0, theta: 0, aim: 0}
            return
        if self.health <= 0:
            self.respawn = RESPAWN_TICKS
            return
            
        # Handle shooting
        if self.primary_reload > 0:
            self.primary_reload -= 1
            
        if self.secondary_reload > 0:
            self.secondary_reload -= 1
            
        if self.shootstate == 1 and self.primary_reload <= 0:
            projectiles.append(Projectile(self.raycaster, 1, {x: self.pose.x, y: self.pose.y, theta: self.pose.aim}))
            self.primary_reload = PRIMARY_RELOAD
            
        if self.shootstate == 2 and self.secondary_reload <= 0:
            projectiles.append(Projectile(self.raycaster, 2, {x: self.pose.x, y: self.pose.y, theta: self.pose.aim}))
            self.secondary_reload = SECONDARY_RELOAD
        
        self.shootstate = 0
        
        # Move robot
        dx = cos(self.pose.theta) * self.movespeed * MOVESPEED_PER_TICK
        dy = sin(self.pose.theta) * self.movespeed * MOVESPEED_PER_TICK
        
        # Check how far the robot can move.
        tx, ty, obj = self.raycaster.cast({x: self.pose.x, y: self.pose.y, theta: self.pose.theta})
        dtx = tx - self.pose.x
        dty = ty - self.pose.y
        
        # Crop movement if nescesarry
        if dx > 0 and dx > dtx:
            dx = dtx
        if dx < 0 and dx < dtx:
            dx = dtx
        if dy > 0 and dy > dty:
            dy = dty
        if dy < 0 and dy < dty:
            dy = dty
            
        # Apply motion
        self.pose.x += dx
        self.pose.y += dy
        self.pose.theta += self.turnspeed * TURNSPEED_PER_TICK
        self.pose.aim += self.aimspeed * AIMSPEED_PER_TICK
        
        # Calculate vision
        
    def render(self):
        if self.respawn > 0:
            return
        # TODO render stuff
        
    def speed(self, movespeed):
        if movespeed < -0.5:
            movespeed = -0.5
        if movespeed > 1:
            movespeed = 1
        self.movespeed = movespeed
    
    def turn(self, turnspeed):
        if turnspeed < -1:
            turnspeed = -1
        if turnspeed > 1:
            turnspeed = 1
        self.turnspeed = turnspeed
        
    def aim(self, aimspeed):
        if aimspeed < -1:
            aimspeed = -1
        if aimspeed > 1:
            aimspeed = 1
        self.aimspeed = aimspeed
    
    def shoot(self, cannon):
        self.shootstate = cannon
    