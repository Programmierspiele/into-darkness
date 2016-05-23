import pygame
import math
from player import Player
from raycaster import Raycaster
from projectile import Projectile
from map import Map
import operator

FOV_IN_DEGREE = 120
FOV = math.radians(FOV_IN_DEGREE)
EPSILON = math.radians(0.001)


class Game(object):
    def __init__(self):
        pass

    @staticmethod
    def render_vision(raycaster, player, screen, width, height, map_size, detail_reduction):
        if player["respawn"] > 0:
            return

        scale = height / map_size

        x = int(player["x"] * scale)
        y = int(player["y"] * scale)
        offset_x = width // 2
        offset_y = height // 2

        points = [(x + offset_x, -y + offset_y)]
        helper_points = []

        lines = raycaster.get_lines()

        tx, ty, _ = raycaster.cast(
            {"x": player["x"], "y": player["y"], "theta": player["aim"] - FOV / 2}, player["name"])
        if tx is not None:
            points.append((int(tx * scale) + offset_x, - int(ty * scale) + offset_y))
        for line in lines:
            for i in range(2):
                p = line[i]
                dx = p["x"] - player["x"]
                dy = p["y"] - player["y"]
                d = math.atan2(dy, dx)
                dth = d - player["aim"]
                while dth > math.pi:
                    dth -= 2 * math.pi
                while dth < -math.pi:
                    dth += 2 * math.pi

                if abs(dth) > FOV / 2.0:
                    continue

                for j in range(3):
                    tx, ty, _ = raycaster.cast(
                        {"x": player["x"], "y": player["y"], "theta": d + (j-1) * EPSILON}, player["name"])
                    if tx is not None and ty is not None:
                        helper_points.append((int(tx * scale) + offset_x, - int(ty * scale) + offset_y,
                                              dth + (j-1) * EPSILON))

        helper_points = sorted(helper_points, key=lambda tup: tup[2])
        for i in range(len(helper_points)):
            points.append((helper_points[i][0], helper_points[i][1]))

        tx, ty, _ = raycaster.cast(
            {"x": player["x"], "y": player["y"], "theta": player["aim"] + FOV / 2}, player["name"])
        if tx is not None:
            points.append((int(tx * scale) + offset_x, - int(ty * scale) + offset_y))

        if len(points) > 2:
            s = pygame.Surface((width, height), pygame.SRCALPHA)  # per-pixel alpha
            pygame.draw.polygon(s, (250, 250, 200, 128), points, 0)
            screen.blit(s, (0, 0))

    @staticmethod
    def render(screen, width, height, gamestate, selected_id, host, port):
        raycaster = Raycaster(gamestate["players"], gamestate["walls"])
        raycaster.update()
        map_size = raycaster.get_map_size() + 1.0

        if selected_id == 0:
            for player in gamestate["players"]:
                Game.render_vision(raycaster, player, screen, width, height, map_size, len(gamestate["players"]))
        elif selected_id > 0 and selected_id - 1 < len(gamestate["players"]):
            Game.render_vision(raycaster, gamestate["players"][selected_id - 1], screen, width, height, map_size,
                               len(gamestate["players"]))

        Map.render(gamestate["walls"], screen, width, height, map_size)
        for p in gamestate["players"]:
            Player.render(p, raycaster, screen, width, height, map_size)
        for projectile in gamestate["projectiles"]:
            Projectile.render(projectile, screen, width, height, map_size)
        for p in gamestate["players"]:
            Player.render_font(p, screen, width, height, map_size)


        myfont = pygame.font.SysFont("Arial", 22)
        label = myfont.render("Ticks remaining: " + str(gamestate["remaining_ticks"]), 1, (255, 255, 255))
        s = pygame.Surface((label.get_width() + 20, label.get_height() + 20), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((45, 45, 45, 200))
        screen.blit(s, (width // 2 - label.get_width() // 2 - 10, 0))
        screen.blit(label, (width // 2 - label.get_width() // 2, 10))

        myfont = pygame.font.SysFont("Arial", 16)
        label = myfont.render("test", 1, (255, 255, 255))
        line_height = label.get_height()
        myfont = pygame.font.SysFont("Arial", 32)
        label = myfont.render("Ranking-----", 1, (255, 255, 255))
        line_width = label.get_width()
        s = pygame.Surface((line_width + 20, line_height * (len(gamestate["ranking"]) + 2) + 40), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((45, 45, 45, 200))
        screen.blit(s, (0, 0))

        myfont = pygame.font.SysFont("Arial", 32)
        label = myfont.render("Ranking", 1, (255, 255, 255))
        screen.blit(label, (10, 10))
        myfont = pygame.font.SysFont("Arial", 16)
        i = 2
        sorted_x = sorted(gamestate["ranking"].items(), key=operator.itemgetter(1), reverse=True)
        for key, value in sorted_x:
            label = myfont.render(key + ": " + str(value), 1, (255, 255, 255))
            screen.blit(label, (10, 10 + label.get_height() * 1.1 * i))
            i += 1

        myfont = pygame.font.SysFont("Arial", 32)
        label = myfont.render(host + ":" + str(port), 1, (255, 255, 0))
        s = pygame.Surface((label.get_width() + 20, label.get_height() + 20), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((45, 45, 45, 200))
        screen.blit(s, (width // 2 - label.get_width() // 2 - 10, height - label.get_height() - 20))
        screen.blit(label, (width // 2 - label.get_width() // 2, height - label.get_height() - 10))
    
    def quit(self):
        pass