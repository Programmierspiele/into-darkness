import pygame
import math
from lobby.lobby import Lobby
from game.game import Game
from network import Network

HOST = "0.0.0.0"
PORT = 1337

class GameManager(object):
    def __init__(self):
        self.events = []
        self.network = Network(HOST, PORT, self)
        self.state = Lobby(self)
        
    def add_event(self, event):
        self.events.append(event)
        
    def get_server(self):
        return self.server
        
    def start_game(self, players):
        self.state.quit()
        self.state = Game(self, players)
        
    def end_game(self):
        self.state.quit()
        self.state = Lobby(self)
    
    def update(self):
        events = self.events
        self.events = []
        self.state.update(events)
     
    def render(self):
        self.state.render()
    
    def quit(self):
        self.network.quit()
        self.state.quit()