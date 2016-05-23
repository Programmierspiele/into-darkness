from lobby.lobby import Lobby
from game.game import Game
from network import Network

HOST = "0.0.0.0"
PORT = 2016


class GameManager(object):
    def __init__(self, pw):
        self.pw = pw
        self.events = []
        self.network = Network(HOST, PORT, self)
        self.state = Lobby(self)
        
    def add_event(self, event):
        self.events.append(event)

    def start_game(self, players, observers):
        self.state.quit()
        self.state = Game(self, players, observers)
        
    def end_game(self):
        tmp = self.state
        self.state = Lobby(self)
        tmp.quit()

    def select_player(self, number):
        self.state.select_player(number)

    def update(self):
        events = self.events
        self.events = []
        self.state.update(events)
    
    def quit(self):
        self.network.quit()
        self.state.quit()
