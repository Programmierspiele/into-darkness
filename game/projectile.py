import math

SECONDARY_RADIUS = 10
PRIMARY_ANIMATION_TIME = 0.1 * 30
SECONDARY_ANIMATION_TIME = 0.4 * 30


class Projectile(object):
    def __init__(self, raycaster, type, pose, owner):
        self.raycaster = raycaster
        self.type = type
        self.damage = 110
        self.pose = pose
        self.owner = owner
        self.dead = 0
        
        self.speed = 10
        if type == 2:
            self.speed = 2 # 4 times quicker than a player

    def get_state(self):
        return {"x": self.pose["x"], "y": self.pose["y"], "theta": self.pose["theta"], "owner": self.owner,
                "speed": self.speed, "damage": self.damage, "type": self.type}

    def update(self, players, projectiles):
        if self.dead > 0:
            self.dead += 1
            if self.dead > PRIMARY_ANIMATION_TIME and not self.type == 2:
                projectiles.remove(self)
            if self.dead > SECONDARY_ANIMATION_TIME and self.type == 2:
                projectiles.remove(self)
            return
        # Calculate motion
        dx = math.cos(self.pose["theta"]) * self.speed
        dy = math.sin(self.pose["theta"]) * self.speed
        
        # Check how far the robot can move.
        tx, ty, obj = self.raycaster.cast({"x": self.pose["x"], "y": self.pose["y"], "theta": self.pose["theta"]}, self.owner)
        if tx is None:
            projectiles.remove(self)
            return
        dtx = tx - self.pose["x"]
        dty = ty - self.pose["y"]
        
        # Crop movement if nescesarry
        hit = False
        if dx > 0 and dx > dtx:
            hit = True
        if dx < 0 and dx < dtx:
            hit = True
        if dy > 0 and dy > dty:
            hit = True
        if dy < 0 and dy < dty:
            hit = True
            
        if hit:
            self.pose["x"] = tx
            self.pose["y"] = ty
            self.dead = 1
            self.apply_damage(obj, players)
        else:
            self.pose["x"] += dx
            self.pose["y"] += dy
    
    def apply_damage(self, obj, players):
        if self.type == 1:  # direct damage
            if hasattr(obj, "damage") and callable(getattr(obj, "damage")):
                obj.damage(self.damage, self.pose["theta"], self.owner)
        if self.type == 2:  # explosive damage
            for key in players:
                p = players[key]
                pose = p.get_pose()
                dx = pose["x"] - self.pose["x"]
                dy = pose["y"] - self.pose["y"]
                dist = math.sqrt(dx * dx + dy * dy)
                
                if dist < SECONDARY_RADIUS:
                    dtheta = math.atan2(dy, dx)
                    if dist < 1:
                        dist = 1
                    if dist < 0.001:
                        dtheta = 0
                    p.damage(self.damage * SECONDARY_RADIUS / dist, dtheta, self.owner)
