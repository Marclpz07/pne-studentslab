seq = "sequences/U5.txt"
from seq0 import seq_read_fasta
from seq0 import  seq_complement

print("Gene U5", "\nFrag:", seq_read_fasta(seq)[0 : 20], "\nComp:",seq_complement(seq))