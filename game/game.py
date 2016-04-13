import pygame
import math

class Game(object):
    def __init__(self, parent, players):
        self.players = players
        self.parent = parent
    
    def update(self, events):
        for event in events:
            if event["sock"] not in self.players:
                continue
            if "disconnected" in event:
                del self.players[event["sock"]]
            if "packet" in event:
                packet = event["packet"]
                sock = event["sock"]
                # handle the actual packet.
    
        self.parent.end_game()
     
    def render(self):
        pass
    
    def quit(self):
        pass