import socket
import json
import sys
from threading import Thread


class Network(object):
    def __init__(self, host, port, parent):
        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(5)
        self.parent = parent
        self.running = True
        self.connections = []
        self.threads = []
        t = Thread(target=self.accept)
        t.setDaemon(True)
        t.start()
        # self.parent.add_event(event)
        
    def accept(self):
        while self.running:
            #try:
                (sock, addr) = self.server.accept()
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.connections.append(sock)
                t = Thread(target=self.connection, args=(sock,))
                t.setDaemon(True)
                t.start()
            #except:
            #    print("Unexpected error:", sys.exc_info()[0])
            
    def connection(self, sock):
        sf = sock.makefile()
        while self.running:
            try:
                line = sf.readline().rstrip('\n')
                event = {"packet": json.loads(line), "sock": sock}
                self.parent.add_event(event)
            except:
                #print("Unexpected error:", sys.exc_info()[0])
                break
        try:
            sock.close()
        except:
            print("Cannot close socket.", sys.exc_info()[0])
        
        self.parent.add_event({"disconnected": True, "sock": sock})
        self.connections.remove(sock)
        
    def quit(self):
        self.running = False
        self.server.close()
        for conn in self.connections:
            conn.close()
    