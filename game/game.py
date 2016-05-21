import pygame
import math
from player import Player
from raycaster import Raycaster
from map import Map

class Game(object):
    def __init__(self, parent, players):
        self.players = players
        self.player_entities = {}
        self.map = Map(len(self.players))
        self.raycaster = Raycaster(self.player_entities, self.map)
        self.projectile_entities = []
        for key in self.players:
            self.player_entities[self.players["key"]] = Player(raycaster)
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
                player = self.player_entities[self.players[sock]]
                if "speed" in packet:
                    player.speed(packet["speed"])
                if "turn" in packet:
                    player.turn(packet["turn"])
                if "aim" in packet:
                    player.aim(packet["aim"])
                if "shoot" in packet:
                    player.shoot(packet["shoot"])
                
        for key in self.player_entities:
            self.player_entities[key].update(self.player_entities, self.projectile_entities)
        for key in self.projectile_entities:
            self.projectile_entities[key].update(self.player_entities, self.projectile_entities)
        #self.parent.end_game()
     
    def render(self):
        for key in self.player_entities:
            self.player_entities[key].render()
        for key in self.projectile_entities:
            self.projectile_entities[key].render()
    
    def quit(self):
        pass