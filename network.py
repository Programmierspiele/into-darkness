import socket
import json
from threading import Thread

class Network(object):
    def __init__(self, host, port, parent):
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.listen(5)
        self.parent = parent
        self.running = True
        self.connections = []
        t = Thread(target=self.accept, args=(self.server,))
        t.start()
        # self.parent.add_event(event)
        
    def accept(self):
        while self.running:
            try:
                (sock, addr) = self.server.accept()
                self.connections.append(sock)
                t = Thread(target=self.connection, args=(sock,))
                t.start()
            except:
                print("Unexpected error:", sys.exc_info()[0])
            
    def connection(self, sock):
        sf = sock.makefile()
        while self.running:
            try:
                line = sf.readline().rstrip('\n')
                event = {"packet": json.loads(line), "sock": sock}
                self.server.add_event(event)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                break
        try:
            sock.close()
        except:
            print("Cannot close socket.", sys.exc_info()[0])
        
        self.server.add_event({"disconnected": True, "sock": sock})
        self.connections.remove(sock)
        
    def quit(self):
        self.running = False
        self.server.close()
        for conn in self.connections:
            conn.close()
    