
from Seq1 import Seq

s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")

print(f"Sequence 1: (Length: {len(s1)}) {s1}\n" f" A: {s1.count_base('A')}, C: {s1.count_base('C')}, T: {s1.count_base('T')}, G: {s1.count_base('G')}")
print(f"Sequence 2: (Length: {len(s2)}) {s2}\n" f" A: {s2.count_base('A')}, C: {s2.count_base('C')}, T: {s2.count_base('T')}, G: {s2.count_base('G')}")
print(f"Sequence 3: (Length: {len(s3)}) {s3}\n" f" A: {s3.count_base('A')}, C: {s3.count_base('C')}, T: {s3.count_base('T')}, G: {s3.count_base('G')}")