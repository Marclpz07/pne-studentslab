from Client0 import Client
from Client0 import Seq

PRACTICE = 2
EXERCISE = 5

print(f"------| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.1.45"
PORT = 8080

c = Client(IP, PORT)
print(c)

s = Seq()
s.read_fasta("sequences/FRAT1.txt")

sequence = str(s)
print("Gene FRAT1:", sequence)

fragments = [
    sequence[0:10],
    sequence[10:20],
    sequence[20:30],
    sequence[30:40],
    sequence[40:50]
]

msg = "Sending FRAT1 Gene to the server, in fragments of 10 bases..."
print("To Server:", msg)
print("From Server:", c.talk(msg))


for i, frag in enumerate(fragments, start=1):
    print(f"Fragment {i}: {frag}")
    print("From Server:", c.talk(f"Fragment {i}: {frag}"))