import pygame
import math

MIN_PLAYERS = 2
MAX_PLAYERS = 16
INIT_TIMEOUT = 10 * 60
PACKET_SIZE = 4048

class Lobby(object):
    def __init__(self, parent):
        self.parent = parent
        self.players = {}
        self.names = []
        self.timeout = INIT_TIMEOUT
        
    def update(self, events):
        for event in events:
            if "disconnected" in event and event["sock"] in self.players:
                self.names.remove(self.players[event["sock"]])
                del self.players[event["sock"]]
            if "packet" in event:
                if "name" in event["packet"]:
                    name = event["packet"]["name"]
                    if name not in self.names:
                        self.players[event["sock"]] = name
                        self.names.append(name)
                        event["sock"].send(json.dumps({"name": name}))
                    elif event["sock"] in self.players:
                        event["sock"].send(json.dumps({"name": self.players[event["sock"]]}))
                    else:
                        event["sock"].send(json.dumps({"name": None}))
    
        if len(self.players) > MIN_PLAYERS:
          self.timeout -= 1
          if len(self.players) >= MAX_PLAYERS:
            self.timeout = 0
        else:
          self.timeout = INIT_TIMEOUT
        
        if self.timeout <= 0:
          self.parent.start_game(self.players)
    
    def render(self):
        pass
    
    def quit(self):
        pass