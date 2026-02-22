from seq0 import seq_count_base

genes = ["U5", "ADA", "FRAT1", "FXN"]
bases = ["A", "C", "T", "G"]

for g in genes:
    seq = "sequences/" + g + ".txt"
    print(f"\nGene {g}:")
    for b in bases:
        count = seq_count_base(seq, b)
        print(f"{b}: {count}")