class Seq:

    def __init__(self, sequence=None):
        if sequence is None:
            self.sequence = "NULL"
            print("Null sequence created!")
            return

        else:
            bases = ["A", "C", "G", "T"]

            for x in sequence:
                if x not in bases:
                    print("Invalid sequence!")
                    self.sequence = "ERROR"
                    return


            self.sequence = sequence
            print("New sequence created!")





    def __len__(self):

        if self.sequence == "NULL":
            return 0
        elif self.sequence == "ERROR":
            return 0
        else:
            return len(self.sequence)

    def count_base(self, base):
        if self.sequence == "NULL":
            return 0
        elif self.sequence == "ERROR":
            return 0
        return self.sequence.count(base)

    def count_dict(self):

        if self.sequence == "NULL":
            return {"A": 0, "T": 0, "C": 0, "G": 0}
        elif self.sequence == "ERROR":
            return {"A": 0, "T": 0, "C": 0, "G": 0}
        else:

            return {"A": self.sequence.count("A"), "T": self.sequence.count("T"), "C": self.sequence.count("C"), "G": self.sequence.count("G")}

    def reverse(self):
        if self.sequence == "NULL":
            return "NULL"
        elif self.sequence == "ERROR":
            return "ERROR"
        else:
            return self.sequence[::-1]

    def complement(self):
        if self.sequence == "NULL":
            return "NULL"
        elif self.sequence == "ERROR":
            return "ERROR"
        else:
            sequence = self.sequence
            sequence = sequence.replace("A", "X")
            sequence = sequence.replace("T", "A")
            sequence = sequence.replace("X", "T")

            sequence = sequence.replace("C", "Y")
            sequence = sequence.replace("G", "C")
            sequence = sequence.replace("Y", "G")
            return sequence

    def read_fasta(self,file):
        from pathlib import Path
        file_contents = Path(file).read_text()
        file_contents = file_contents.split("\n")
        body = "".join(file_contents[1:])
        self.sequence = body
        return self

    def most_frequent_base(self):
        if self.sequence in ["NULL", "ERROR"]:
            return None

        bases = {"A": 0, "C": 0, "G": 0, "T": 0}

        for b in self.sequence:
            if b in bases:
                bases[b] += 1

        return max(bases, key=bases.get)



    def __str__(self):
        return self.sequence