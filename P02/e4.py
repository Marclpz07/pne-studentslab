from Client0 import Seq
from Client0 import Client

IP = "192.168.1.45"
PORT = 8080

c = Client(IP, PORT)
print(c)

genes = [
    ("U5", "sequences/U5.txt"),
    ("ADA", "sequences/ADA.txt"),
    ("FRAT1", "sequences/FRAT1.txt"),
    ("FXN", "sequences/FXN.txt"),
    ("RNU6_269P", "sequences/RNU6_269P.txt")
]

for name, path in genes:
    s = Seq()
    s.read_fasta(path)

    msg = f"Sending the {name} Gene to the server..."
    print("To Server:", msg)
    print("From Server:", c.talk(msg))

    print("To Server:", str(s))
    print("From Server:", c.talk(str(s)))
