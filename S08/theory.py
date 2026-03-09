import socket


PORT = 8080
IP = "192.168.124.179"
MAX_OPEN_REQUESTS = 5


number_con = 0


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
