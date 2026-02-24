def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    from pathlib import Path

    file_contents = Path(filename).read_text()

    filecontents = file_contents.split("\n")
    bases = " \n".join(filecontents[1: ])

    first_20 = bases[ : 20]
    return bases

def seq_len(seq):
    from pathlib import Path
    gene = seq_read_fasta(seq)
    return len(gene)

def seq_count_base(seq, base):
    gene = seq_read_fasta(seq)
    count = 0

    for b in gene:
        if b == base:
            count += 1

    return count

def seq_count(seq):
    gene = seq_read_fasta(seq)

    counts = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

    for b in gene:
        if b in counts:
            counts[b] += 1

    return counts

def  seq_reverse(seq, n):
    gene = seq_read_fasta(seq)
    fragment = gene[: n]
    return fragment[::-1]

def seq_complement(seq):
    gene = seq_read_fasta(seq)[ : 20]
    gene = gene.replace("A", "X")
    gene = gene.replace("T", "A")
    gene = gene.replace("X", "T")

    gene = gene.replace("C", "Y")
    gene = gene.replace("G", "C")
    gene = gene.replace("Y", "G")
    return gene

def most_frequent_base(seq):
    gene = seq_read_fasta(seq)

    bases = {"A": 0, "C": 0, "G": 0, "T": 0}

    for b in gene:
        if b in bases:
            bases[b] += 1

    # Encontrar la base con mayor frecuencia
    most_base = max(bases, key=bases.get)
    return most_base











