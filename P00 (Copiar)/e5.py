from seq0 import seq_count



genes = ["U5", "ADA", "FRAT1", "FXN"]

for g in genes:
    filename = "sequences/" + g + ".txt"
    counts = seq_count(filename)
    print(f"Gene {g}: {counts}")