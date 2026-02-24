filename = "sequences/U5.txt"

from seq0 import seq_read_fasta

print("DNA file: U5.txt", "\nFirst 20 basaes:", seq_read_fasta(filename)[0 : 20])

