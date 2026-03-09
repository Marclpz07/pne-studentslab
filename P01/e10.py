from Seq1 import Seq

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
    base = s.most_frequent_base()
    print(f"Gene {name}: Most frequent Base: {base}")