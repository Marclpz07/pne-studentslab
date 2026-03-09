from Client0 import Client

PRACTICE = 2
EXERCISE = 3

print(f"------| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.1.45"
PORT = 8080

c = Client(IP, PORT)

print(c)

# -- Send a message to the server
print("Sending a message to the server...")
response = c.talk("Testing!!!")
print(f"Response: {response}")