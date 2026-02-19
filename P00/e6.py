seq = "sequences/U5.txt"
n = 20
from seq0 import seq_reverse
from seq0 import seq_read_fasta

print("Gene U5", "\nfragment:", seq_read_fasta(seq)[0 : 20], "\nReverse:",seq_reverse(seq, n))