from Seq1 import Seq

s = Seq()
FILENAME = "sequences/U5.txt"

s.read_fasta("sequences/U5.txt")

print(f"Sequence : (Length: {len(s)}) {s}\n" f"Bases:{s.count_dict()}\n" f"Rev:{s.reverse()}\n" f"Comp:{s.complement()}")


