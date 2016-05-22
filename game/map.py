import pygame
import math

class Map(object):
    def __init__(self, playercount):
        # TODO Load map dependant on playercount
        self.lines = []
        self.create_rect(0, 0, 200, 200, math.radians(20))
        self.create_rect(15, 15, 20, 5, math.radians(30))
        self.create_rect(1.9, 2.8, 22, 5, math.radians(55))
        self.create_rect(-5, -15, 20, 5, math.radians(90))
        self.map_size = 0
        for line in self.lines:
            self.map_size = max(self.map_size, 2 * abs(line[0]["x"]))
            self.map_size = max(self.map_size, 2 * abs(line[0]["y"]))
            self.map_size = max(self.map_size, 2 * abs(line[1]["x"]))
            self.map_size = max(self.map_size, 2 * abs(line[1]["y"]))

    def create_rect(self, x, y, width, height, theta):
        dx_width = math.cos(theta) * width
        dy_width = math.sin(theta) * width
        dx_height = math.sin(theta) * height
        dy_height = math.cos(theta) * height

        ul = {"x": x + dx_width/2 - dx_height / 2, "y": y + dy_height / 2 + dy_width / 2}
        ur = {"x": x - dx_width/2 - dx_height / 2, "y": y + dy_height / 2 - dy_width / 2}
        bl = {"x": x + dx_width/2 + dx_height / 2, "y": y - dy_height / 2 + dy_width / 2}
        br = {"x": x - dx_width/2 + dx_height / 2, "y": y - dy_height / 2 - dy_width / 2}

        self.lines.append([ul, ur])
        self.lines.append([ur, br])
        self.lines.append([br, bl])
        self.lines.append([bl, ul])

    def get_map_size(self):
        return self.map_size
        
    def get_lines(self):
        return self.lines

    def render(self, screen, width, height, map_size):
        scale = height / map_size

        for line in self.lines:
            x0 = int(line[0]["x"] * scale) + width // 2
            y0 = - int(line[0]["y"] * scale) + height // 2
            x1 = int(line[1]["x"] * scale) + width // 2
            y1 = - int(line[1]["y"] * scale) + height // 2
            pygame.draw.lines(screen, (200, 200, 200), False, [(x0, y0), (x1, y1)], 2)
