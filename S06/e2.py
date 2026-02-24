from operator import itemgetter


class Seq:
    """A class for representing sequences"""

    def __init__(self, strbases):

        # Initialize the sequence with the value
        # passed as argument when creating the object
        self.strbases = strbases
        bases = ["A", "C", "G", "T"]
        length = len(strbases)
        i = 0
        while i in range(0, length):
            if strbases[i] in bases:
                i += 1

            else:
                print("ERROR")
                break
        print("New sequence created!")

    def __str__(self):
        """Method called when the object is being printed"""
        # -- We just return the string with the sequence
        return self.strbases

    def len(self):
        """Calculate the length of the sequence"""
        return len(self.strbases)

def print_seqs():
    for i in range


seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]

