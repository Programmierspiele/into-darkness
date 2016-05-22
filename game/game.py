import math
from player import Player
from raycaster import Raycaster
from map import Map
import json

FOV_IN_DEGREE = 120
FOV = math.radians(FOV_IN_DEGREE)
EPSILON = math.radians(0.001)


class Game(object):
    def __init__(self, parent, players, observers):
        self.players = players
        self.observers = observers
        self.scores = {}
        self.player_entities = {}
        self.map = Map(len(self.players))
        self.raycaster = Raycaster(self.player_entities, self.map)
        self.projectile_entities = []
        for key in self.players:
            self.player_entities[self.players[key]] = Player(self.raycaster, self.players[key], self)
            self.scores[self.players[key]] = 0
        self.parent = parent
        self.selected_player = None
        self.select_player(0)

    def select_player(self, number):
        i = 1
        self.selected_player = None
        if number > len(self.player_entities):
            return
        for key in self.player_entities:
            if i > number:
                return
            self.selected_player = self.player_entities[key]
            i += 1

    def score(self, name, score):
        self.scores[name] = self.scores[name] + score

    def update(self, events):
        self.raycaster.update()

        for event in events:
            if event["sock"] not in self.players:
                continue
            if "disconnected" in event:
                del self.players[event["sock"]]
            if "packet" in event:
                packet = event["packet"]
                sock = event["sock"]
                player = self.player_entities[self.players[sock]]
                if "speed" in packet:
                    player.speed(packet["speed"])
                if "turn" in packet:
                    player.turn(packet["turn"])
                if "aim" in packet:
                    player.aim(packet["aim"])
                if "shoot" in packet:
                    player.shoot(packet["shoot"])

        for key in self.player_entities:
            self.player_entities[key].update(self.player_entities, self.projectile_entities)
        for projectile in self.projectile_entities:
            projectile.update(self.player_entities, self.projectile_entities)

        for sock in self.players:
            key = self.players[sock]
            sock.send(json.dumps({"gamestate": self.gamestate(self.player_entities[key])}) + "\n")

        for sock in self.observers:
            sock.send(json.dumps({"gamestate": self.gamestate_full()}) + "\n")

    def gamestate(self, player):
        gamestate = {"player": player.get_state(), "players": [], "projectiles": [], "walls": self.map.get_lines(),
                     "ranking": self.scores}

        for key in self.player_entities:
            p = self.player_entities[key]
            pose = p.get_pose()
            dx = pose["x"] - player.pose["x"]
            dy = pose["y"] - player.pose["y"]
            d = math.atan2(dy, dx)
            dth = d - player.pose["aim"]
            while dth > math.pi:
                dth -= 2 * math.pi
            while dth < -math.pi:
                dth += 2 * math.pi

            if abs(dth) > FOV / 2.0:
                continue
            tx, ty, obj = self.raycaster.cast({"x": player.pose["x"], "y": player.pose["y"], "theta": d}, player.name)
            if obj == p:
                gamestate["players"].append(p.get_state())

        for projectile in self.projectile_entities:
            gamestate["projectiles"].append(projectile.get_state())

        return gamestate

    def gamestate_full(self):
        gamestate = {"players": [], "projectiles": [], "walls": self.map.get_lines(),
                     "ranking": self.scores}

        for key in self.player_entities:
            p = self.player_entities[key]
            gamestate["players"].append(p.get_state())

        for projectile in self.projectile_entities:
            gamestate["projectiles"].append(projectile.get_state())

        return gamestate
    
    def quit(self):
        pass