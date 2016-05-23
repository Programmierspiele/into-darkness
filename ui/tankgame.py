from lobby.lobby import Lobby
from game.game import Game
from default.noserver import NoServer
from network import Network


class GameManager(object):
    def __init__(self, host, port, pw):
        self.event = None
        self.selected_player = -1
        self.network = None
        self.host = host
        self.port = port
        self.pw = pw
        
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
                self.network = Network(host, port, pw, self)
            except:
                self.event = None

        if self.event is None:
            NoServer.render(screen, width, height)
            return

        if "gamestate" in self.event:
            Game.render(screen, width, height, self.event["gamestate"], self.selected_player)
        elif "lobby" in self.event:
            Lobby.render(screen, width, height, self.event["lobby"], host, port)
        else:
            print("unknown state")
            print(self.event)
    
    def quit(self):
        if self.network is not None:
            self.network.quit()
