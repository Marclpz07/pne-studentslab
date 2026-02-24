from seq0 import seq_len

genes = ["U5", "ADA", "FRAT1", "FXN"]

for g in genes:
    filename = "sequences/" + g + ".txt"
    length = seq_len(filename)
    print(f"Gene {g} -> Length: {length}")