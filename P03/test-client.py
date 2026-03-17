from P02.Client0 import *

PRACTICE = 3
EXERCISE = 7

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

i = 0
while i < 6:
    IP = "127.0.0.1"
    PORT = 8080

    c = Client(IP, PORT)
    if i == 0:
        c = Client(IP, PORT)
        print("Sending a message to the server...")
        response = c.talk("PING")
        print(f"Response: {response}")
    elif i == 1:
        c = Client(IP, PORT)
        print("Sending a message to the server...")
        response = c.talk("GET 0")
        print(f"Response: {response}")
        response = c.talk("GET 1")
        print(f"Response: {response}")
        response = c.talk("GET 2")
        print(f"Response: {response}")
        response = c.talk("GET 3")
        print(f"Response: {response}")
        response = c.talk("GET 4")
        print(f"Response: {response}")

    elif i == 2:
        c = Client(IP, PORT)
        print("Sending a message to the server...")
        response = c.talk("INFO AAATTTGGGCCC")
        print(f"Response: {response}")

    elif i == 3:
        c = Client(IP, PORT)
        print("Sending a message to the server...")
        response = c.talk("COMP AAATTTGGGCCC")
        print(f"Response: {response}")

    elif i == 4:
        c = Client(IP, PORT)
        print("Sending a message to the server...")
        response = c.talk("REV AAATTTGGGCCC")
        print(f"Response: {response}")

    elif i == 5:
        c = Client(IP, PORT)
        print("Sending a message to the server...")
        response = c.talk("GENE U5")
        print(f"Response: {response}")
        response = c.talk("GENE ADA")
        print(f"Response: {response}")
        response = c.talk("GENE FRAT1")
        print(f"Response: {response}")
        response = c.talk("GENE FXN")
        print(f"Response: {response}")
        response = c.talk("GENE RNU6_269P")
        print(f"Response: {response}")

    i = i + 1
