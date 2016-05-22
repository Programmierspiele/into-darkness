import pygame

INIT_TIMEOUT = 30 * 30


class Lobby(object):
    def __init__(self):
        pass

    @staticmethod
    def render(screen, width, height, packet, host, port):
        timeout = packet["timeout"]
        players = packet["players"]

        centerX = width // 2

        myfont = pygame.font.SysFont("Arial", 76)
        label = myfont.render("Into Darkness", 1, (255, 255, 255))
        screen.blit(label, (centerX - label.get_width() // 2, height // 4 - label.get_height() // 2))

        myfont = pygame.font.SysFont("Arial", 56)
        label = myfont.render(host + ":" + str(port), 1, (255, 255, 0))
        screen.blit(label, (centerX - label.get_width() // 2, 3 * height // 4 - label.get_height() // 2))

        myfont = pygame.font.SysFont("Arial", 32)
        label = myfont.render("Players: " + str(len(players)), 1, (255, 255, 255))
        screen.blit(label, (centerX - label.get_width() // 2, height // 2 - label.get_height() // 2))

        myfont = pygame.font.SysFont("Arial", 22)
        if timeout < INIT_TIMEOUT:
            label = myfont.render("Start in: " + str(timeout) + " ticks", 1, (0, 255, 0))
            screen.blit(label, (centerX - label.get_width() // 2, height - 5 - label.get_height()))
        else:
            label = myfont.render("Waiting for more players...", 1, (255, 0, 0))
            screen.blit(label, (centerX - label.get_width() // 2, height - 5 - label.get_height()))
