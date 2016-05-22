import pygame


class Map(object):
    def __init__(self):
        pass

    @staticmethod
    def render(lines, screen, width, height, map_size):
        scale = height / map_size

        for line in lines:
            x0 = int(line[0]["x"] * scale) + width // 2
            y0 = - int(line[0]["y"] * scale) + height // 2
            x1 = int(line[1]["x"] * scale) + width // 2
            y1 = - int(line[1]["y"] * scale) + height // 2
            pygame.draw.lines(screen, (200, 200, 200), False, [(x0, y0), (x1, y1)], 2)
