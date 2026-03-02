from Seq1 import Seq

s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")

print(f"Sequence 1: (Length: {len(s1)}) {s1}\n" f"Bases:{s1.count_dict()}")
print(f"Sequence 2: (Length: {len(s2)}) {s2}\n" f"Bases:{s2.count_dict()}")
print(f"Sequence 3: (Length: {len(s3)}) {s3}\n" f"Bases:{s3.count_dict()}")