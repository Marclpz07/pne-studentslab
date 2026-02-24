from seq0 import most_frequent_base

genes = [
    ("U5", "sequences/U5.txt"),
    ("ADA", "sequences/ADA.txt"),
    ("FRAT1", "sequences/FRAT1.txt"),
    ("FXN", "sequences/FXN.txt")
]

for name, path in genes:
    base = most_frequent_base(path)
    print(f"Gene {name}: Most frequent Base: {base}")