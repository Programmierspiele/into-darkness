import pygame


class Projectile(object):
    def __init__(self):
        pass

    @staticmethod
    def render(projectile, screen, width, height, map_size):
        scale = height / map_size

        x = int(projectile["x"] * scale)
        y = int(projectile["y"] * scale)
        pygame.draw.circle(screen, (255, 255, 255), (x + width // 2, -y + height // 2), max(1, int(0.3 * scale)), 1)

        if projectile["dead"] > 0:
            if projectile["type"] == 2:
                pygame.draw.circle(screen, (255, 180, 100), (x + width // 2, -y + height // 2),
                                   max(1, int(projectile["dead"] * scale)), max(1, int(projectile["dead"] * scale)))
            else:
                pygame.draw.circle(screen, (255, 100, 100), (x + width // 2, -y + height // 2),
                                   max(1, int(projectile["dead"] * scale)), max(1, int(projectile["dead"] * scale)))
