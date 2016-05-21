import math

class Projectile(object):
    def __init__(self, raycaster, type, pose):
        self.raycaster = raycaster
        self.type = type
        self.damage = 110
        self.pose = pose
        
        self.speed = 1000
        if type == 2:
            self.speed = 4 # 4 times quicker than a player
        
    def update(self, players, projectiles):
        # Calculate motion
        dx = math.cos(self.pose.theta) * self.speed
        dy = math.sin(self.pose.theta) * self.speed
        
        # Check how far the robot can move.
        tx, ty, obj = self.raycaster.cast({x: self.pose.x, y: self.pose.y, theta: self.pose.theta})
        dtx = tx - self.pose.x
        dty = ty - self.pose.y
        
        # Crop movement if nescesarry
        if dx > 0 and dx > dtx:
            hit = True
        if dx < 0 and dx < dtx:
            hit = True
        if dy > 0 and dy > dty:
            hit = True
        if dy < 0 and dy < dty:
            hit = True
            
        if hit == True:
            self.pose.x = tx
            self.pose.y = ty
            projectiles.remove(self)
            self.damage(obj, players)
        else:
            self.pose.x += dx
            self.pose.y += dy
    
    def damage(self, obj, players):
        if self.type == 1: # direct damage
            if callable(getattr(obj, "damage")):
                obj.damage(self.damage, self.pose.theta)
        if self.type == 2: # explosive damage
            for key in players:
                p = players[key]
                pose = p.get_pose()
                dx = pose.x - self.pose.x
                dy = pose.y - self.pose.y
                dist = math.sqrt(dx * dx + dy * dy)
                
                if dist < SECONDARY_RADIUS:
                    dtheta = math.atan2(dy, dx)
                    p.damage(self.damage * SECONDARY_RADIUS / dist, dtheta)
            
    
    def render(self):
        pass