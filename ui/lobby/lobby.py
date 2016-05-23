import pygame
import operator

INIT_TIMEOUT = 30 * 30


class Lobby(object):
    def __init__(self):
        pass

    @staticmethod
    def render(screen, width, height, packet, host, port, ranking):
        timeout = packet["timeout"]
        players = packet["players"]
        centerX = width // 2
        centerY = height// 2

        if ranking is not None and timeout > INIT_TIMEOUT / 4:
            myfont = pygame.font.SysFont("Arial", 44)
            label = myfont.render("Into Darkness", 1, (255, 255, 255))
            screen.blit(label, (centerX - label.get_width() // 2, 10))

            panelHeight = 42 + 22 * 1.1 * len(ranking.items())
            myfont = pygame.font.SysFont("Arial", 32)
            label = myfont.render("Game Over", 1, (255, 255, 255))
            screen.blit(label, (centerX - label.get_width() // 2, centerY - panelHeight))
            myfont = pygame.font.SysFont("Arial", 22)
            sorted_x = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)

            label = myfont.render(sorted_x[0][0], 1, (255, 255, 255))
            label2 = myfont.render(str(sorted_x[0][1]), 1, (255, 255, 255))
            panelWidth = label.get_width() + 40 + label2.get_width()

            i = 0
            label = myfont.render("Player", 1, (255, 255, 255))
            label2 = myfont.render("Points", 1, (255, 255, 255))
            screen.blit(label,
                        (centerX - 20 - panelWidth / 2, centerY - panelHeight + 56 + label.get_height() * 1.1 * i))
            screen.blit(label2, (centerX + 20 + panelWidth / 2 - label2.get_width(),
                                 centerY - panelHeight + 56 + label.get_height() * 1.1 * i))
            i += 1
            for key, value in sorted_x:
                label = myfont.render(key, 1, (255, 255, 255))
                label2 = myfont.render(str(value), 1, (255, 255, 255))
                screen.blit(label, (centerX - 20 - panelWidth / 2, centerY - panelHeight + 64 + label.get_height() * 1.1 * i))
                screen.blit(label2, (centerX + 20 + panelWidth / 2 - label2.get_width(), centerY - panelHeight + 64 + label.get_height() * 1.1 * i))
                i += 1

            myfont = pygame.font.SysFont("Arial", 32)
            label = myfont.render(host + ":" + str(port), 1, (255, 255, 0))
            screen.blit(label, (centerX - label.get_width() // 2, height - 30 - label.get_height()))
        else:
            myfont = pygame.font.SysFont("Arial", 76)
            label = myfont.render("Into Darkness", 1, (255, 255, 255))
            screen.blit(label, (centerX - label.get_width() // 2, height // 4 - label.get_height() // 2))

            myfont = pygame.font.SysFont("Arial", 32)
            label = myfont.render("Players: " + str(len(players)), 1, (255, 255, 255))
            screen.blit(label, (centerX - label.get_width() // 2, height // 2 - label.get_height() // 2))

            myfont = pygame.font.SysFont("Arial", 56)
            label = myfont.render(host + ":" + str(port), 1, (255, 255, 0))
            screen.blit(label, (centerX - label.get_width() // 2, 3 * height // 4 - label.get_height() // 2))

        myfont = pygame.font.SysFont("Arial", 22)
        if timeout < INIT_TIMEOUT:
            label = myfont.render("Start in: " + str(timeout) + " ticks", 1, (0, 255, 0))
            screen.blit(label, (centerX - label.get_width() // 2, height - 5 - label.get_height()))
        else:
            label = myfont.render("Waiting for more players...", 1, (255, 0, 0))
            screen.blit(label, (centerX - label.get_width() // 2, height - 5 - label.get_height()))
