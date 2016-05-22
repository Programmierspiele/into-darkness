import pygame
import json

MIN_PLAYERS = 2
MAX_PLAYERS = 16
INIT_TIMEOUT = 1 * 60
PACKET_SIZE = 4048


class Lobby(object):
    def __init__(self, parent):
        self.parent = parent
        self.players = {}
        self.names = []
        self.timeout = INIT_TIMEOUT

    def select_player(self, number):
        pass

    def update(self, events):
        for event in events:
            if "disconnected" in event and event["sock"] in self.players:
                self.names.remove(self.players[event["sock"]])
                del self.players[event["sock"]]
            if "packet" in event:
                print(json.dumps(event["packet"]))
                if "name" in event["packet"]:
                    name = event["packet"]["name"]
                    if name not in self.names:
                        self.players[event["sock"]] = name
                        self.names.append(name)
                        event["sock"].send(json.dumps({"name": name}) + "\n")
                    elif event["sock"] in self.players:
                        event["sock"].send(json.dumps({"name": self.players[event["sock"]]}) + "\n")
                    else:
                        event["sock"].send(json.dumps({"name": None}) + "\n")
    
        if len(self.players) > MIN_PLAYERS:
          self.timeout -= 1
          if len(self.players) >= MAX_PLAYERS:
            self.timeout = 0
        else:
          self.timeout = INIT_TIMEOUT
        
        if self.timeout <= 0:
          self.parent.start_game(self.players)
    
    def render(self, screen, width, height):
        centerX = width // 2

        myfont = pygame.font.SysFont("Arial", 56)
        label = myfont.render("Lobby", 1, (255, 255, 255))
        screen.blit(label, (centerX - label.get_width() // 2, height // 4 - label.get_height() // 2))

        myfont = pygame.font.SysFont("Arial", 32)
        label = myfont.render("Players: " + str(len(self.players)), 1, (255, 255, 255))
        screen.blit(label, (centerX - label.get_width() // 2, height // 2 - label.get_height() // 2))

        if self.timeout < INIT_TIMEOUT:
            label = myfont.render("Start in: " + str(self.timeout) + "t", 1, (255, 255, 255))
            screen.blit(label, (centerX - label.get_width() // 2, height - 50 - label.get_height() // 2))
        else:
            label = myfont.render("Waiting for more players...", 1, (255, 255, 255))
            screen.blit(label, (centerX - label.get_width() // 2, height - 50 - label.get_height() // 2))

    
    def quit(self):
        pass