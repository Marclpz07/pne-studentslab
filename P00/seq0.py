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
    bases = []
    for x in seq:
        genes = seq_read_fasta(x)
        a = len(genes)
        print("Genes", x, "--> Length:", len(genes))


def seq_count_base(seq, bases):
    for x in seq:
        genes = seq_read_fasta(x)
        print(x)
        for base in bases:
            print("Base:", base,"->" ,genes.count(base), "times")

def seq_count(seq, bases):
    basis = {}
    for x in seq:
        genes = seq_read_fasta(x)
        print(x)
        for base in bases:
            basis[base] = genes.count(base)
        print(basis)







