import math
from projectile import Projectile
import random

PRIMARY_RELOAD = 1 * 30
SECONDARY_RELOAD = 3 * PRIMARY_RELOAD

BLOOM_MAX = math.radians(20)
BLOOM_MIN = math.radians(0.5)
BLOOM_DECAY = math.radians(20) / SECONDARY_RELOAD
BLOOM_PRIMARY = BLOOM_MAX / (SECONDARY_RELOAD / PRIMARY_RELOAD)
BLOOM_SECONDARY = BLOOM_MAX

RESPAWN_TICKS = 5 * 30

AIMSPEED_PER_TICK = 0.1
TURNSPEED_PER_TICK = 0.1
MOVESPEED_PER_TICK = 1.0

FOV_IN_DEGREE = 120
FOV = math.radians(FOV_IN_DEGREE)


class Player(object):
    def __init__(self, raycaster, name, game):
        self.game = game
        self.raycaster = raycaster
        self.pose = {"x": 0.0, "y": 0.0, "theta": 0.0, "aim": 0.0}
        self.name = name
        self.movespeed = 0.0
        self.turnspeed = 0.0
        self.aimspeed = 0.0
        self.shootstate = 0.0
        self.health = 100.0
        self.respawn = 0.0
        self.bloom = BLOOM_MIN
        
        self.primary_reload = 0.0
        self.secondary_reload = 0.0
        self.spawn()

    def get_size(self):
        return 1.0

    def get_state(self):
        return {"x": self.pose["x"], "y": self.pose["y"], "theta": self.pose["theta"], "aim": self.pose["aim"],
                "health": self.health, "shootstate": self.shootstate, "respawn": self.respawn,
                "reload_primary": self.primary_reload, "reload_secondary": self.secondary_reload, "name": self.name,
                "movespeed": self.movespeed, "turnspeed": self.turnspeed, "aimspeed": self.aimspeed,
                "size": self.get_size(), "bloom": self.bloom}

    def damage(self, damage, dmg_heading, owner):
        dh = self.pose["theta"] - dmg_heading
        while dh <= math.pi:
            dh += 2 * math.pi
        while dh > math.pi:
            dh -= 2 * math.pi
        dh = abs(dh) / math.pi
        modifier = (1-dh) * 0.5 + 0.5
        self.health -= damage * modifier

        if self.health <= 0:
            if owner != self.name:
                self.game.score(owner, 1)
            else:
                self.game.score(owner, -1)
            self.respawn = RESPAWN_TICKS
            return

    def spawn(self):
        self.health = 100.0
        spawn_x = random.random() * self.game.map.get_map_size() - self.game.map.get_map_size() / 2
        spawn_y = random.random() * self.game.map.get_map_size() - self.game.map.get_map_size() / 2
        d = random.random() * math.pi * 2 - math.pi
        self.pose = {"x": spawn_x, "y": spawn_y, "theta": d, "aim": d}

    def get_pose(self):
        return {"x": self.pose["x"], "y": self.pose["y"], "theta": self.pose["theta"]}
        
    def update(self, players, projectiles):
        if self.respawn > 0:
            self.respawn -= 1
            if self.respawn == 0:
                self.spawn()
            return

        if self.health <= 0:
            self.game.score(self.name, -1)
            self.respawn = RESPAWN_TICKS
            return
            
        # Handle shooting
        if self.primary_reload > 0:
            self.primary_reload -= 1
            
        if self.secondary_reload > 0:
            self.secondary_reload -= 1
            
        if self.shootstate == 1 and self.primary_reload <= 0:
            berr = random.random() * self.bloom * 2 - self.bloom
            projectiles.append(Projectile(self.raycaster, 1, {"x": self.pose["x"], "y": self.pose["y"], "theta": self.pose["aim"] + berr}, self.name))
            self.primary_reload = PRIMARY_RELOAD
            self.bloom += BLOOM_PRIMARY
            
        if self.shootstate == 2 and self.secondary_reload <= 0:
            berr = random.random() * self.bloom * 2 - self.bloom
            projectiles.append(Projectile(self.raycaster, 2, {"x": self.pose["x"], "y": self.pose["y"], "theta": self.pose["aim"] + berr}, self.name))
            self.secondary_reload = SECONDARY_RELOAD
            self.bloom += BLOOM_SECONDARY

        self.bloom = min(BLOOM_MAX, self.bloom)
        self.bloom -= BLOOM_DECAY * (1.0-abs(self.movespeed))
        self.bloom = max(0, self.bloom)
        
        self.shootstate = 0
        
        # Move robot
        dx = math.cos(self.pose["theta"]) * self.movespeed * MOVESPEED_PER_TICK
        dy = math.sin(self.pose["theta"]) * self.movespeed * MOVESPEED_PER_TICK
        
        # Check how far the robot can move.
        tx, ty, obj = self.raycaster.cast({"x": self.pose["x"], "y": self.pose["y"], "theta": self.pose["theta"]}, self.name)

        # Only if there is an obstacle do something about it...
        if tx is not None and ty is not None and obj is not None:
            dtx = tx - self.pose["x"]
            dty = ty - self.pose["y"]
        
            # Crop movement if nescesarry
            if dx > 0 and dx > dtx - self.get_size() / 2:
                dx = 0
                dy = 0
            elif dx < 0 and dx < dtx + self.get_size() / 2:
                dx = 0
                dy = 0
            if dy > 0 and dy > dty - self.get_size() / 2:
                dx = 0
                dy = 0
            elif dy < 0 and dy < dty + self.get_size() / 2:
                dx = 0
                dy = 0
            
        # Apply motion
        self.pose["x"] += dx
        self.pose["y"] += dy
        self.pose["theta"] += self.turnspeed * TURNSPEED_PER_TICK
        self.pose["aim"] += self.aimspeed * AIMSPEED_PER_TICK + self.turnspeed * TURNSPEED_PER_TICK

        while self.pose["theta"] <= -math.pi:
            self.pose["theta"] += 2 * math.pi
        while self.pose["theta"] > math.pi:
            self.pose["theta"] -= 2 * math.pi

        while self.pose["aim"] <= -math.pi:
            self.pose["aim"] += 2 * math.pi
        while self.pose["aim"] > math.pi:
            self.pose["aim"] -= 2 * math.pi
        
    def speed(self, movespeed):
        if movespeed < 0:
            movespeed = 0
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
