import pygame
import math
from player import Player
from raycaster import Raycaster
from map import Map
import json
import operator

FOV_IN_DEGREE = 120
FOV = math.radians(FOV_IN_DEGREE)
EPSILON = math.radians(0.001)


class Game(object):
    def __init__(self, parent, players):
        self.players = players
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
        #self.parent.end_game()

        for sock in self.players:
            key = self.players[sock]
            sock.send(json.dumps({"gamestate": self.gamestate(self.player_entities[key])}) + "\n")

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
                dth -= 2*math.pi
            while dth < -math.pi:
                dth += 2*math.pi

            if abs(dth) > FOV / 2.0:
                continue
            tx, ty, obj = self.raycaster.cast({"x": player.pose["x"], "y": player.pose["y"], "theta": d}, player.name)
            if obj == p:
                gamestate["players"].append(p.get_state())

        for projectile in self.projectile_entities:
            gamestate["projectiles"].append(projectile.get_state())

        return gamestate

    def render_vision(self, player, screen, width, height, map_size, detail_reduction):
        if player.respawn > 0:
            return

        scale = height / map_size

        x = int(player.pose["x"] * scale)
        y = int(player.pose["y"] * scale)
        offset_x = width // 2
        offset_y = height // 2

        points = [(x + offset_x, -y + offset_y)]
        helper_points = []

        lines = self.raycaster.get_lines()

        tx, ty, _ = self.raycaster.cast(
            {"x": player.pose["x"], "y": player.pose["y"], "theta": player.pose["aim"] - FOV / 2}, player.name)
        if tx is not None:
            points.append((int(tx * scale) + offset_x, - int(ty * scale) + offset_y))
        for line in lines:
            for i in range(2):
                p = line[i]
                dx = p["x"] - player.pose["x"]
                dy = p["y"] - player.pose["y"]
                d = math.atan2(dy, dx)
                dth = d - player.pose["aim"]
                while dth > math.pi:
                    dth -= 2 * math.pi
                while dth < -math.pi:
                    dth += 2 * math.pi

                if abs(dth) > FOV / 2.0:
                    continue

                for j in range(3):
                    tx, ty, _ = self.raycaster.cast(
                        {"x": player.pose["x"], "y": player.pose["y"], "theta": d + (j-1) * EPSILON}, player.name)
                    if tx is not None and ty is not None:
                        helper_points.append((int(tx * scale) + offset_x, - int(ty * scale) + offset_y,
                                              dth + (j-1) * EPSILON))

        helper_points = sorted(helper_points, key=lambda tup: tup[2])
        for i in range(len(helper_points)):
            points.append((helper_points[i][0], helper_points[i][1]))

        tx, ty, _ = self.raycaster.cast(
            {"x": player.pose["x"], "y": player.pose["y"], "theta": player.pose["aim"] + FOV / 2}, player.name)
        if tx is not None:
            points.append((int(tx * scale) + offset_x, - int(ty * scale) + offset_y))

        if len(points) > 2:
            s = pygame.Surface((width, height), pygame.SRCALPHA)  # per-pixel alpha
            pygame.draw.polygon(s, (250, 250, 200, 128), points, 0)
            screen.blit(s, (0, 0))

    def render(self, screen, width, height):
        self.raycaster.update()
        map_size = self.map.get_map_size() + 1.0

        if self.selected_player is not None:
            self.render_vision(self.selected_player, screen, width, height, map_size, 1)
        else:
            for p in self.player_entities:
                player = self.player_entities[p]
                self.render_vision(player, screen, width, height, map_size, len(self.player_entities))

        self.map.render(screen, width, height, map_size)
        for key in self.player_entities:
            self.player_entities[key].render(screen, width, height, map_size)
        for projectile in self.projectile_entities:
            projectile.render(screen, width, height, map_size)

        myfont = pygame.font.SysFont("Arial", 32)
        label = myfont.render("Ranking", 1, (255, 255, 255))
        screen.blit(label, (10, 10))
        myfont = pygame.font.SysFont("Arial", 16)
        i = 2
        sorted_x = sorted(self.scores.items(), key=operator.itemgetter(1), reverse=True)
        for key, value in sorted_x:
            label = myfont.render(key + ": " + str(value), 1, (255, 255, 255))
            screen.blit(label, (10, 10 + label.get_height() * 1.1 * i))
            i += 1
    
    def quit(self):
        pass