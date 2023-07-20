import socket
from _thread import *
import pickle
from game import Game
import json

# Load server configuration from config.json
with open('config.json', 'r') as file:
    config = json.load(file)

server = config['server']
port = config['port']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

#stores IP address of connected clients
connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    #sends player number [0,1] to client
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            #constantly receives string data from client
            data = conn.recv(4096).decode()

            #if game exists
            if gameId in games:
                game = games[gameId]

                #Checks if received data is to 'reset', 'get', or 'move'
                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    #sends game object back to client
                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break


    #If breaking from while loop:
    print("Lost Connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2

    #if odd # of players, creates new game
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    #else, assigns you to open game with 1 player
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
