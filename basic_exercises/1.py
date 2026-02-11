


dna = "ATGCGATCGATCGATCGATCGA"
subsequence = dna.count("ATC")

print("LENGTH:",len(dna))
print("FIRST 5:", dna[0], dna[1],dna[2], dna[3], dna[4])
print("LAST 3:", dna[-3],dna[-2], dna[-1])
print("LOWERACSE:",dna.lower())
print("ATC COUNT:", subsequence)
print("RNA:", dna.replace("T","U"))

