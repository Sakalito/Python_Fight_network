import socket
import signal #identifie les signaux pour kill le programme
import sys #utilisé pour sortir du programme
import time
from ClientThread import ClientListener


class Server():

    def __init__(self, port):
        self.listener= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        print("Ecoute sur le port", port)
        self.clients_sockets= []
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signal, frame):
        self.listener.close()
        self.echo("QUIT")

    def run(self):
        while True:
            print("En écoute")
            try:
                (clients_sockets, client_adress) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
            self.clients_sockets.append(clients_sockets)
            print("Start the thread for client:", client_adress)
            client_thread= ClientListener(self, clients_sockets, client_adress)
            client_thread.start()
            time.sleep(0.1)

    def remove_socket(self, socket):
        self.clients_sockets.remove(socket)

    def echo(self, data):
        print(data)
        for sock in self.clients_sockets:
            try:
                sock.sendall(data.encode("UTF-8"))
            except socket.error:
                print("Cannot send the message")


if __name__ == "__main__":
    server= Server(59001)
    server.run()
