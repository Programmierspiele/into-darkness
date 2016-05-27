import json
import sys

MIN_PLAYERS = 2
MAX_PLAYERS = 16
INIT_TIMEOUT = 1 * 15  # ~ 30 seconds lobby


class Lobby(object):
    def __init__(self, parent):
        self.parent = parent
        self.players = {}
        self.observers = []
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
                try:
                    if "name" in event["packet"]:
                        name = event["packet"]["name"]
                        if name not in self.names:
                            self.players[event["sock"]] = name
                            self.names.append(name)
                            event["sock"].send(json.dumps({"name": name}) + "\n")
                        elif event["sock"] in self.players:
                            event["sock"].send(json.dumps({"name": None}) + "\n")
                        else:
                            event["sock"].send(json.dumps({"name": None}) + "\n")
                    if "observer" in event["packet"]:
                        pw = event["packet"]["observer"]
                        if pw == self.parent.pw:
                            self.observers.append(event["sock"])
                except:
                    try:
                        event["sock"].send(str(sys.exc_info()[0]) + "\n")
                    except:
                        pass
    
        if len(self.players) >= MIN_PLAYERS:
          self.timeout -= 1
          if len(self.players) >= MAX_PLAYERS:
            self.timeout = 0
        else:
          self.timeout = INIT_TIMEOUT
        
        if self.timeout <= 0:
          self.parent.start_game(self.players, self.observers)

        mark_for_deletion = []
        for player in self.players:
            try:
                player.send(json.dumps({"lobby": {"players": self.names, "timeout": self.timeout}}) + "\n")
            except:
                mark_for_deletion.append(player)

        for sock in mark_for_deletion:
            del self.players[sock]

        mark_for_deletion = []
        for observer in self.observers:
            try:
                observer.send(json.dumps({"lobby": {"players": self.names, "timeout": self.timeout}}) + "\n")
            except:
                mark_for_deletion.append(observer)

        for sock in mark_for_deletion:
            self.observers.remove(sock)
    
    def quit(self):
        pass
