import math
from player import Player
from raycaster import Raycaster
from map import Map
import json
import time

TICKS_PER_GAME = 5 * 60 * 30  # 5 Minuten
FOV_IN_DEGREE = 120
FOV = math.radians(FOV_IN_DEGREE)
EPSILON = math.radians(0.001)


class Game(object):
    def __init__(self, parent, players, observers):
        self.remaining_ticks = TICKS_PER_GAME
        self.players = players
        self.player_writestreams = {}
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

        self.last_time = time.time()

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
        self.remaining_ticks -= 1
        if self.remaining_ticks < 0:
            self.parent.end_game()
            return
        self.raycaster.update()

        for event in events:
            if event["sock"] not in self.players:
                if "packet" in event and "observer" in event["packet"]:
                    pw = event["packet"]["observer"]
                    if pw == self.parent.pw:
                        self.observers.append(event["sock"])
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

        mark_for_deletion = []
        for sock in self.players:
            key = self.players[sock]
            if not sock in self.player_writestreams:
                self.player_writestreams[sock] = sock.makefile(mode='w')
            try:
                # seems to be a bit more stable in the actual rate it writes that the sock.send method
                self.player_writestreams[sock].write(json.dumps({"gamestate": self.gamestate(self.player_entities[key])}))
                self.player_writestreams[sock].write("\n")
                self.player_writestreams[sock].flush()
                #sock.send(json.dumps({"gamestate": self.gamestate(self.player_entities[key])}))
                #sock.send("\n")
            except:
                mark_for_deletion.append(sock)

        for sock in mark_for_deletion:
            del self.players[sock]

        mark_for_deletion = []
        for sock in self.observers:
            try:
                sock.send(json.dumps({"gamestate": self.gamestate_full()}))
                sock.send("\n")
                #sock.flush()
            except:
                mark_for_deletion.append(sock)

        for sock in mark_for_deletion:
            self.observers.remove(sock)

        if len(self.players) == 0:
            self.parent.end_game()

    def gamestate(self, player):
        gamestate = {"remaining_ticks": self.remaining_ticks, "player": player.get_state(), "players": [],
                     "projectiles": [], "walls": self.map.get_lines(),
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
        gamestate = {"remaining_ticks": self.remaining_ticks, "players": [], "projectiles": [],
                     "walls": self.map.get_lines(), "ranking": self.scores}

        for key in self.player_entities:
            p = self.player_entities[key]
            gamestate["players"].append(p.get_state())

        for projectile in self.projectile_entities:
            gamestate["projectiles"].append(projectile.get_state())

        return gamestate
    
    def quit(self):
        for sock in self.players:
            try:
                sock.send("\n")
                sock.close()
            except:
                del self.players[sock]

        for sock in self.observers:
            try:
                sock.send("\n")
                sock.close()
            except:
                self.observers.remove(sock)
