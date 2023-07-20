import socket
import pickle
import json


class Network:
    def __init__(self):
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
            self.server = config['server']
            self.port = config['port']
        except (FileNotFoundError, KeyError) as e:
            print(
                "Could not load server configuration. Please ensure that 'config.json' exists and is correctly formatted.")
            exit(1)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)


