import math
from projectile import Projectile
import pygame
import random


FOV_IN_DEGREE = 120
FOV = math.radians(FOV_IN_DEGREE)


class Player(object):
    def __init__(self, raycaster, name, game):
        pass

    #def get_state(self):
    #    return {"x": self.pose["x"], "y": self.pose["y"], "theta": self.pose["theta"], "aim": self.pose["aim"],
    #            "health": self.health, "shootstate": self.shootstate, "respawn": self.respawn,
    #            "reload_primary": self.primary_reload, "reload_secondary": self.secondary_reload, "name": self.name,
    #            "movespeed": self.movespeed, "turnspeed": self.turnspeed, "aimspeed": self.aimspeed}


    @staticmethod
    def render(player, raycaster, screen, width, height, map_size):
        scale = height / map_size

        x = int(player["x"] * scale)
        y = int(player["y"] * scale)
        pygame.draw.circle(screen, (255, 255, 255), (x + width // 2, -y + height // 2), max(1, int(1.0 * scale)), 1)

        pygame.draw.lines(screen, (255, 128, 128), False, [(x + width // 2, -y + height // 2),
                (x + math.cos(player["aim"]) * scale * 3 + width // 2, -y -math.sin(player["aim"]) * scale * 3 + height // 2)], 5)
        pygame.draw.lines(screen, (255, 255, 128), False, [(x + width // 2, -y + height // 2),
                (x + math.cos(player["theta"]) * scale * 5 + width // 2, -y -math.sin(player["theta"]) * scale * 5 + height // 2)], 2)

        if player["respawn"] > 0:
            return

        tx, ty, _ = raycaster.cast(
            {"x": player["x"], "y": player["y"], "theta": player["aim"]}, player["name"])
        if tx is not None and ty is not None:
            x0 = x + width // 2
            y0 = - y + height // 2
            x1 = int(tx * scale) + width // 2
            y1 = - int(ty * scale) + height // 2
            pygame.draw.lines(screen, (255, 128, 128), False, [(x0, y0), (x1, y1)], 1)

        tx, ty, _ = raycaster.cast(
            {"x": player["x"], "y": player["y"], "theta": player["aim"] - player["bloom"]}, player["name"])
        if tx is not None and ty is not None:
            x0 = x + width // 2
            y0 = - y + height // 2
            x1 = int(tx * scale) + width // 2
            y1 = - int(ty * scale) + height // 2
            pygame.draw.lines(screen, (255, 200, 128), False, [(x0, y0), (x1, y1)], 1)

        tx, ty, _ = raycaster.cast(
            {"x": player["x"], "y": player["y"], "theta": player["aim"] + player["bloom"]}, player["name"])
        if tx is not None and ty is not None:
            x0 = x + width // 2
            y0 = - y + height // 2
            x1 = int(tx * scale) + width // 2
            y1 = - int(ty * scale) + height // 2
            pygame.draw.lines(screen, (255, 200, 128), False, [(x0, y0), (x1, y1)], 1)

    @staticmethod
    def render_font(player, screen, width, height, map_size):
        scale = height / map_size

        tx = int(player["x"] * scale)
        ty = int((player["y"] + 1.1) * scale)
        myfont = pygame.font.SysFont("Arial", 12)

        label = myfont.render("(" + str(math.floor(player["health"])) + ") " + player["name"], 1, (128, 128, 128))
        if player["respawn"] > 0:
            label = myfont.render("(" + str(player["respawn"]) + ") " + player["name"], 1, (128, 128, 128))
        s = pygame.Surface((label.get_width() + 4, label.get_height() + 4), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((45, 45, 45, 200))
        screen.blit(s, (tx + width // 2 - label.get_width() // 2 - 2, -ty + height // 2 - label.get_height() - 2))
        screen.blit(label, (tx + width // 2 - label.get_width() // 2, -ty + height // 2 - label.get_height()))