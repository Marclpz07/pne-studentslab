import socket
from P00.seq0 import seq_complement
from P01.Seq1 import Seq


class Client:
    def __init__(self, IP, PORT):
        self.ip = IP
        self.port = PORT

    def ping(self):
        print("OK")

    def __str__(self):
        return f"Connection to SERVER at {self.ip}, PORT: {self.port}"

    def talk(self, msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        s.send(str.encode(msg))
        response = s.recv(2048).decode("utf-8")
        s.close()

        return response




# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Configure the Server's IP and PORT
PORT = 8080
IP = "127.0.0.1"

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# -- Step 2: Bind the socket to server's IP and PORT
ls.bind((IP, PORT))

# -- Step 3: Configure the socket for listening
ls.listen()

print("The server is configured!")

while True:
    # -- Waits for a client to connect
    print("Waiting for Clients to connect")

    try:
        (cs, client_ip_port) = ls.accept()

    # -- Server stopped manually
    except KeyboardInterrupt:
        print("Server stopped by the user")

        # -- Close the listenning socket
        ls.close()

        # -- Exit!
        exit()

    # -- Execute this part if there are no errors
    else:

        print("A client has connected to the server!")

        # -- Read the message from the client
        # -- The received message is in raw bytes
        msg_raw = cs.recv(2048)

        # -- We decode it for converting it
        # -- into a human-redeable string
        msg = msg_raw.decode()
        x = msg.split(" ")
        if x[0] == "PING":
            print(f"PING Command!")
            response = "OK\n"

        if x[0] == "GET":
            if x[1] == "0":
                response = "AAAGGGTTTCCCAAAAA"
            elif x[1] == "1":
                response = "AAAGGGTTTCCCAGGGG"
            elif x[1] == "2":
                response = "AAAGGGTTTCCCAAGGG"
            elif x[1] == "3":
                response = "AAAGGGTTTCCCAAAGG"
            elif x[1] == "4":
                response = "AAAGGGTTTCCCAAAAG"

        elif x[0] == "INFO":
            seq1 = x[1]
            s = Seq(seq1)
            dict_result = s.count_bases2()

            response = ""
            response += f"Sequence: {seq1}\n"
            response += f"Total length: {len(seq1)}\n"
            for base in ["A", "C", "G", "T"]:
                response += f"{base}: {dict_result[base]['times']} ({dict_result[base]['percentage']}%)\n"

        elif x[0] == "COMP":
            seq1 = x[1]
            print(seq1)
            s = Seq(seq1)
            result = s.seq_complement()
            response = result

        elif x[0] == "REV":
            seq1 = x[1]
            print(seq1)
            s = Seq(seq1)
            result = s.reverse()
            response = result

        elif x[0] == "GENE":
            if x[1] == "U5":
                U5 = "../sequences/U5.txt"
                s1 = Seq()
                s11 = s1.seq_read_fasta(U5)

                response = s11
            elif x[1] == "ADA":
                ADA = "../sequences/ADA.txt"
                s1 = Seq()
                s11 = s1.seq_read_fasta(ADA)

                response = s11
            elif x[1] == "FRAT1":
                FRAT1 = "../sequences/FRAT1.txt"
                s1 = Seq()
                s11 = s1.seq_read_fasta(FRAT1)

                response = s11
            elif x[1] == "FXN":
                FXN = "../sequences/FXN.txt"
                s1 = Seq()
                s11 = s1.seq_read_fasta(FXN)

                response = s11
            elif x[1] == "RNU6_269P":
                RNU6_269P = "../sequences/RNU6_269P.txt"
                s1 = Seq()
                s11 = s1.seq_read_fasta(RNU6_269P)

                response = s11

        cs.send(response.encode())

        # -- Close the data socket
        cs.close()