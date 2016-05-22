import socket
import json
import sys
from threading import Thread

OBSERVER_PW = "wasdwasd1234"


class Network(object):
    def __init__(self, host, port, parent):
        self.socket = socket.socket()
        self.socket.connect((host, port))
        self.socket.send(json.dumps({"observer": OBSERVER_PW}) + "\n")
        self.parent = parent
        self.running = True
        self.threads = []
        t = Thread(target=self.connection, args=(self.socket,))
        t.setDaemon(True)
        t.start()
            
    def connection(self, sock):
        sf = sock.makefile()
        while self.running:
            try:
                line = sf.readline().rstrip('\n')
                if line == "":
                    self.running = False
                    continue
                event = {"packet": json.loads(line), "sock": sock}
                self.parent.add_event(event)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                self.running = False
        try:
            sock.close()
        except:
            print("Cannot close socket.", sys.exc_info()[0])
        
        self.parent.add_event({"disconnected": True, "sock": sock})
        
    def quit(self):
        self.running = False
        self.socket.close()
