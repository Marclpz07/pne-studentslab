from Client0 import Client
from Client0 import Seq

PRACTICE = 2
EXERCISE = 6

print(f"------| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.1.45"
PORT1 = 8080
PORT2 = 8081

# Crear dos clientes
c1 = Client(IP, PORT1)
c2 = Client(IP, PORT2)

print(c1)
print(c2)

# Cargar FRAT1
s = Seq()
s.read_fasta("sequences/FRAT1.txt")

sequence = str(s)
print("Gene FRAT1:", sequence)

# Obtener 10 fragmentos de 10 bases
fragments = [sequence[i:i+10] for i in range(0, 100, 10)]

# Enviar fragmentos alternos.
for i, frag in enumerate(fragments, start=1):
    print(f"Fragment {i}: {frag}")
    if i % 2 == 1:
        print("From Server1:", c1.talk(f"Fragment {i}: {frag}"))
    else:
        print("From Server2:", c2.talk(f"Fragment {i}: {frag}"))