import pygame

INIT_TIMEOUT = 1 * 60


class NoServer(object):
    def __init__(self):
        pass

    @staticmethod
    def render(screen, width, height):
        centerX = width // 2

        myfont = pygame.font.SysFont("Arial", 56)
        label = myfont.render("No Server", 1, (255, 255, 255))
        screen.blit(label, (centerX - label.get_width() // 2, height // 3 - label.get_height() // 2))

        myfont = pygame.font.SysFont("Arial", 32)
        label = myfont.render("Waiting for server", 1, (255, 255, 255))
        screen.blit(label, (centerX - label.get_width() // 2, 2 * height // 3 - label.get_height() // 2))

    @staticmethod
    def render_pw_error(screen, width, height):
        centerX = width // 2

        myfont = pygame.font.SysFont("Arial", 56)
        label = myfont.render("Incorrect Password", 1, (255, 30, 30))
        screen.blit(label, (centerX - label.get_width() // 2, height // 3 - label.get_height() // 2))

        myfont = pygame.font.SysFont("Arial", 32)
        label = myfont.render("Server was found", 1, (255, 255, 255))
        screen.blit(label, (centerX - label.get_width() // 2, 2 * height // 3 - label.get_height() // 2))
