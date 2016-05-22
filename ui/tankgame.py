from lobby.lobby import Lobby
from game.game import Game
from default.noserver import NoServer
from network import Network

HOST = "localhost"
PORT = 2016


class GameManager(object):
    def __init__(self):
        self.event = None
        self.selected_player = -1
        self.network = None
        
    def add_event(self, event):
        if "disconnected" in event:
            self.network = None
            return
        self.event = event["packet"]

    def select_player(self, number):
        self.selected_player = number
     
    def render(self, screen, width, height):
        if self.network is None:
            try:
                self.network = Network(HOST, PORT, self)
            except:
                self.event = None

        if self.event is None:
            NoServer.render(screen, width, height)
            return

        if "gamestate" in self.event:
            Game.render(screen, width, height, self.event["gamestate"], self.selected_player)
        elif "lobby" in self.event:
            Lobby.render(screen, width, height, self.event["lobby"], HOST, PORT)
        else:
            print("unknown state")
            print(self.event)
    
    def quit(self):
        if self.network is not None:
            self.network.quit()