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
        self.last_score = None
        
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
                self.network = Network(self.host, self.port, self.pw, self)
            except:
                self.event = None
                self.network = None

        if self.event is None and self.network is None:
            NoServer.render(screen, width, height)
            return
        if self.event is None:
            NoServer.render_pw_error(screen, width, height)
            return

        if "gamestate" in self.event:
            self.last_score = self.event["gamestate"]["ranking"]
            Game.render(screen, width, height, self.event["gamestate"], self.selected_player, self.host, self.port)
        elif "lobby" in self.event:
            Lobby.render(screen, width, height, self.event["lobby"], self.host, self.port, self.last_score)
        else:
            print("unknown state")
            print(self.event)
    
    def quit(self):
        if self.network is not None:
            self.network.quit()
